Platform architecture
=====================

A schematic of the Oasis Platform architecture is shown in the diagram below, and the components are descibed in the following table:

.. figure:: /images/oasis_containers.png
    :alt: Oasis UI and Platform architecture
   
.. csv-table::
    :header: "Component", "Description", "Technology"

    "ShinyProxy", "Provides multi-user support and enterprise integration features on top of a Shiny app.", "ShinyProxy"
    "OasisUI", "The application server for the Oasis user interface, a web app.", "Shiny App"
    "OasisAPI", "The application server for the Oasis API.", "Django Application Server"
    "OasisAPI DB", "The database for the Oasis API. Stores the system meta-data, but not the detailed model data, exposure data or results.", "MySql (or other RDBMS)"
    "Worker monitor", "Monitors the model worker and updates the Oasis API database with the status of tasks.", "Custom Python code"
    "Celery - Message Queue", "Message queue for the celery job management framework.", "Rabbit MQ (other options)"
    "Celery – Backing Store", "Backing store for the celery job management framework.", "MySQL (other options)"
    "Datastore", "File based datastore for exposure data, analysis results and model data.", "Docker volume"
    "Model Worker", "Celery worker that can run a lookup or model execution task for a particular model version. The model data is attached to the container from the datastore at startup.", "Custom Python and C++ code"


hard-Scaling
-------------

the typical computation in oasis follow a split-apply-combine strategy, with the following modules:

- parametrization of eve does the split, indicating to generate a subset of the events
- eve, getmodel, gulcalc and fmcalc (insurance and re-insurance) does the apply,
  performing the computation to determine the different loss outputs for each subset of events.
- aalcalc and leccalc does the combine, computing the final results from the union of all the subsets.

Communication between the different modules are generally done via pipes or files
with fully specified data interfaces.

The basic parallelizable brick is:

 eve -> getmodel -> gulcalc -> fmcalc (insurance) -> fmcalc (re-insurance).

Parallelization is done at the process level and, therefore, can be achieve by using bigger
server with more processors. Scale up for large models and/or large portfolios.

Our performance testing has shown it provides good hard-scaling on single machine from
1 to 16 processors.
However above this, gain from adding processors start to decrease
and are even negative past 32 processors.
This is mainly due to the relative slowness of fmcalc compare to gulcalc that is stopping gulcalc
and slowing fmcalc by having too many context switches.

To overcome those limitation we are putting in place new approach.

- gul-fm load balancer (next realease) that will split events out of the gul further
  and increase fmcalc parallelization.
- Oasis at scale (in test) will provide to the Oasis platform a way to split events
  on a cluster using celery with the ability to auto-scale depending on the workload size.
  (see detail at: https://github.com/OasisLMF/OasisAtScaleEvaluation)


Weak Scaling
------------

All of the components are packaged as Docker images.
Docker-compose can be used to deploy the system on one or more physical servers.
You can therefore increase the throughput of analysis by
provisioning more calculation servers and deploying more Analysis Worker images.
