Distributed Execution and Scaling
===================================

.. _distributed_execution:

:doc:`overview` | :doc:`platform_architecture` | :doc:`container_configuration` | :doc:`rest_api` | :doc:`distributed_execution`

This section details the two primary execution modes – 'Single Server' (``run_mode = v1``) and 'Distributed' (``run_mode = v2``) – for our software's core workflows. Both modes consistently involve two distinct stages: 'file preparation' and 'losses generation'. The fundamental difference between these modes lies in the sophisticated orchestration of tasks using Celery.

Single Server Execution (run_mode = v1)
---------------------------------------

In 'Single Server' execution, the system operates akin to a monolithic application, with each major workflow stage encapsulated within a single, self-contained Celery task. This mode mirrors the direct invocation of OasisLMF command-line interface (CLI) commands, such as ``$ oasislmf model generate-oasis-files`` for file preparation and ``$ oasislmf model generate-losses`` for losses generation. The execution occurs within the isolated Python environment provided by the 'model worker' Docker image.

Celery Task Flow
~~~~~~~~~~~~~~~

Each of these large-grained tasks is dispatched from the central server. A single 'model worker' container then picks up the task, processes it to completion, and subsequently reports its results back to the system via the 'WorkerMonitor' container.

Internal Parallelization for Losses Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While the overall Celery task for losses generation is singular, significant parallelization is achieved internally *within* this task. This is managed by a bash script, run_ktools.sh, which orchestrates the execution of OasisLMF's ktools (Kernel Tools).

By default, run_ktools.sh uses all the available compute resource by creating an "in-memory" losses data pipe for each core on the executing system. This approach maximizes CPU utilization for the computationally intensive loss calculations. The parallelization pattern follows a common design:

``eve <event batch> <total batches> | <group up loss calculation> | <financial modules>``

Here's a breakdown of the components:

* **eve <event batch> <total batches>**: The eve command is responsible for distributing the event data into total batches, with each instance processing a specific event batch.
* **<group up loss calculation> (GUL - Ground Up Loss)**: This stage performs the initial, loss calculations based on the model.
* **<financial modules> (FM)**: This final stage applies financial terms and conditions to the calculated ground-up losses to calculate the final insurable losses.

Example: 8-Core System Utilization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider a system with 8 available CPU cores. The run_ktools.sh script will dynamically generate a series of parallel pipelines, effectively loading each core to its full capacity.

.. code-block:: bash

    eve 1  8 | <gul> | <fm>
    eve 2  8 | <gul> | <fm>
    ...
    eve 8  8 | <gul> | <fm>

In this 'Single Server' mode, due to its internal strategy of loading every core, the assigned 'model worker' can only process a single job at a time. This ensures maximum throughput for that specific job but limits concurrent execution of other, independent jobs on the same worker instance.

Parallel Execution of Multiple Single Server Jobs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While a single 'Single Server Execution' job itself fully utilizes one worker, it is possible to run multiple such jobs in parallel. This is achieved by deploying multiple 'model worker' pods or nodes, each dedicated to a single execution. To ensure optimal isolation and resource allocation, a **1:1 affinity (default)** is typically configured between each node or VM and a worker pod. This means that for every parallel execution initiated, a distinct worker container will be spun up to handle it.

The number of workers available on the ``v1`` worker queue can be scaled in two primary ways to accommodate concurrent 'Single Server Executions':

1. **Fixed Scaling:** The worker fleet can be provisioned to a fixed number of instances, allowing for a predetermined level of concurrent processing.
2. **Dynamic Scaling (Based on Queued Tasks):** For more elastic environments, the worker count can be dynamically adjusted based on the number of pending tasks in the ``v1`` queue. This ensures that resources are scaled up when demand is high and scaled down when tasks are complete, optimizing resource utilization.

Distributed and Scalable Workflows (run_mode = v2)
--------------------------------------------------

The 'Distributed' execution mode (run_mode = v2) represents our system's highly scalable approach to processing. Unlike the 'Single Server' mode, the core workflows (file preparation and losses generation) are no longer treated as monolithic tasks. Instead, they are decomposed into a **collection of sub-tasks**, orchestrated by Celery's canvas primitives into a single **chain**. These sub-tasks execute sequentially, defining the overall flow of the analysis.

Celery Canvas for Distributed Workflows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Part of the chain is a '**distributed section**'. Within it, multiple sub-tasks, each representing an '**analysis chunk**', are processed **concurrently across multiple worker nodes**. This is intentionally designed to be the phase where the bulk of the computationally intensive work is performed, significantly reducing overall execution time compared to a sequential approach.

Chunking for Parallelism (chunks)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The degree of parallelization within a distributed analysis is determined by the number of 'chunks'. Each 'chunk' corresponds to a distinct sub-task that can be processed in parallel. This chunks value is a configurable variable set *before* the Celery workflow (the chain of sub-tasks) is placed onto the queue.

The chunks value can be determined in a few ways:

* **Fixed Integer:** Directly specified as a static integer, providing a predictable level of parallelism.
* **Dynamic Scaling based on Input Size:** The number of chunks can be dynamically scaled based on the size of the input data. For 'file preparation', this is the size of the location file. For 'losses generation', it's the size of an event set.

It's crucial to understand that this chunks value, which defines the internal parallelism of an analysis, is distinct from the scaling value that controls the total number of 'model workers' available on the queue to process these sub-tasks.

Distinction from OasisLMF MDK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The distributed workflow (run_mode = v2) does not have a direct, equivalent command in the standard OasisLMF Model Development Kit (MDK). This is because the fundamental principles of splitting, distributing, and aggregating analyses are intrinsically handled by Celery, which are external to the core oasislmf package. The intelligence for managing this distributed execution resides within OasisPlatform components, such as the TaskController.

However, within each individual sub-task of the v2 workflow, the same or similar functions from the MDK are called. These functions are simply invoked in more atomic, focused steps suitable for distributed processing. As a result, when provided with the same exposure inputs, the final outputs from a v1 (Single Server) run and a v2 (Distributed) run will be **identical**, guaranteeing consistency across execution modes.

Workflow Submission and Execution Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Request Submission:** When an execution request for a v2 workflow is submitted, it is received by the API server.
2. **TaskController Orchestration:** The API server then invokes the TaskController. The TaskController is responsible for:

   * Reading the analysis chunking configuration (i.e., how many chunks the analysis should be split into).
   * Setting the priority level for the execution.
   * Constructing the complete Celery chain of sub-tasks, which includes the chord for the distributed section.
   * Placing *all* these sub-tasks onto the designated 'model worker' queue simultaneously.

3. **Dynamic Worker Scaling:** Concurrently, a WebSocket update is sent to the WorkerController. Based on the configured scaling parameters for the 'model queue', the WorkerController dynamically spins up or scales down the number of 'model workers' to match the demand created by the queued sub-tasks.
4. **Task execution:** Workers will sequentially process the sub-tasks in the chain until they encounter the parallel (chord) section. At this point, multiple workers will simultaneously process different 'analysis chunk' sub-tasks
