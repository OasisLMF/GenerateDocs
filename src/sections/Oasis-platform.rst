Oasis Platform (1&2)
====================

On this page:

* :ref:`introduction_platform`
* :ref:`installing_oasis`
* :ref:`platform_architecture`
* :ref:`hard_scaling`
* :ref:`weak_scaling`
* :ref:`development_approach`
* :ref:`technology_stack`
* :ref:`github_repositories`


|

.. _introduction_platform:

introduction_platform
---------------------

The Oasis Loss Modelling Framework provides an open source platform for developing, deploying and executing catastrophe 
models. It uses a full simulation engine and makes no restrictions on the modelling approach. Models are packaged in a 
standard format and the components can be from any source, such as model vendors, academic and research groups. The 
platform provides:

* A platform for running catastrophe models, including a web based user interface and an API for integration with other 
  systems (Oasis Loss Modelling Framework)

* Core components for executing catastrophe models at scale and standard data formats for hazard and vulnerability (Oasis 
  ktools)

* Toolkit for developing, testing and deploying catastrophe models (Oasis Model Development Toolkit)



|
.. _installing_oasis:

Installing Oasis
****************
|
Oasis Installation Guide: Windows 10 OS
#######################################

..  youtube:: SxRt5E-Y5Sw

|
Oasis Installation Guide: Linux based OS
########################################

..  youtube:: OFLTpGGEM10



|
.. _platform_architecture:

Platform architecture
*********************

A schematic of the Oasis Platform architecture is shown in the diagram below, and the components are described in the following table:

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
    "Model Worker", "Celery worker that can run a lookup or model execution task for a particular model version. The model data is attached to the container from the datastore at start up.", "Custom Python and C++ code"



|
.. _hard_scaling:

hard-Scaling
************

The typical computation in oasis follows a split-apply-combine strategy, with the following modules:

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

- gul-fm load balancer (next release) that will split events out of the gul further
  and increase fmcalc parallelization.
- Oasis at scale (in test) will provide to the Oasis platform a way to split events
  on a cluster using celery with the ability to auto-scale depending on the workload size.
  (see detail at: https://github.com/OasisLMF/OasisAtScaleEvaluation)


|
.. _weak_scaling:

Weak Scaling
************

All of the components are packaged as Docker images.
Docker-compose can be used to deploy the system on one or more physical servers.
You can therefore increase the throughput of analysis by
provisioning more calculation servers and deploying more Analysis Worker images.



..
   From Development approach:


|
.. _development_approach:

Development approach
********************

1. We build open source software. This allows the community to directly
   review and critique our code and methodologies, and to contribute
   code for our review.

2. We use open source technology. We look to build on standard, modern
   technologies that will reduce the operational cost and/or improve the
   operational performance of models, that have solid support options
   for enterprise use, and that are free for general use.

3. We are building a full stack development team. Every team member
   should understand the system and technologies, be able to build and
   test the system and have a working knowledge of catastrophe
   modelling.

4. We use the community to drive development. We have direct access to
   many of the leading practitioners in the catastrophe modelling
   domain, and we get practical input through feature prioritization,
   specification and review of working software.

5. We use partnerships to provide scale, for hosting, support and
   non-core development.



.. 
   From tech stack


|
.. _technology_stack:

Technology stack
****************

**Using**

========================  ===============================================================================
Python 3.6                General system programming and tools.
C++ 11                    Simulation and analytics kernel.
Docker                    Deployment of Oasis Platform and UI.
Ubuntu 18.04 LTS          Development servers and base Docker image.
AWS                       Cloud infrastructure for Oasis Model Library and Oasis Platform deployment.
Jenkins 2 & BlueOcean     Continuous integration.
Django                    Web service framework.
Apache                    Web server.
Terraform                 Infrastructure automation.
Sphinx                    Code documentation generation.
RShiny                    Application framework build on R.
ShinyProxy                Server for scaling RShiny applications.
MySql                     Application database for UI.
Jupyter                   Python notebooks for examples and training material.
========================  ===============================================================================



.. 
   From GitHub repositories



|
.. _github_repositories:

GitHub repositories
*******************

.. csv-table::
  :header: "Repository name", "Purpose"

  "`CookiecutterOasisSimpleModel <https://github.com/OasisLMF/CookiecutterOasisSimpleModel>`_", "Repository template for a model implementation."
  "`CookiecutterOasisComplexModel <https://github.com/OasisLMF/CookiecutterOasisComplexModel>`_", "Repository template for a complex implementation."
  "`ktools <https://github.com/OasisLMF/Ktools>`_", "Model execution kernel."
  "`OasisEvaluation <https://github.com/OasisLMF/OasisEvaluation>`_", "Getting started with the Oasis platform."
  "`OasisLMF <https://github.com/OasisLMF/OasisLMF>`_", "Python package, with the core oasis business logic, MDK command line tools and the Oasis API client."
  "`OasisPiWind <https://github.com/OasisLMF/OasisPiWind>`_", "Example model implementation."
  "`OasisPlatform <(https://github.com/OasisLMF/OasisPlatform>`_", "Flask application that provides the Oasis API and workers for running a model."
  "`OasisUI <https://github.com/OasisLMF/OasisUI>`_", "Shiny application, Flask application and database for the Flamingo application."