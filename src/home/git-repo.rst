OasisLMF GitHub
===============

The OasisLMF GitHub can be found here: https://github.com/OasisLMF.

----


This OasisLMF GitHub currently hosts these reposistories:
*********************************************************

----

* `build <https://github.com/OasisLMF/build>`_

This repository contains the build utilities for `OasisPlatform <https://github.com/OasisLMF/OasisPlatform>`_

----

* `camel <https://github.com/OasisLMF/camel>`_

Camel is a command line tool for automating development processes. It reduces errors and acts as a sort of self 
documentation. Camel also supports terraform which enables users to use it to run and test models.

----

* `ComplexModelMDK <https://github.com/OasisLMF/ComplexModelMDK>`_

ComplexModelMDK is used to run complex models via the :doc:`../../sections/model-development-kit`.

----

* `DeterministicModel <https://github.com/OasisLMF/DeterministicModel>`_

This is a single event model which allows users to apply deterministic losses to a portfolio, defining the damage factors 
in the OED location file. It is similar to the exposure feature in the oasislmf package, but can be deployed as a model in 
it’s own right to model deterministic losses which can then be passed through the Oasis financial module.

----

* `gem <https://github.com/OasisLMF/gem>`_

This is a event-based-risk earthquake model set in the Dominican Republic built by `GEM - Global Earthquake Model 
<https://www.globalquakemodel.org/gem>`_.

----

* `GenerateDocs <https://github.com/OasisLMF/GenerateDocs>`_

This repository is used to store and build Oasis documentation.

----

* `gerund <https://github.com/OasisLMF/gerund>`_

This package is responsible for compiling and running bash commands.

----

* `ktest <https://github.com/OasisLMF/ktest>`_

This is the extended test harness for `ktools <https://github.com/OasisLMF/ktools>`_ which can run in Windows or Linux. Its primary roles are:
    * Installer test - this is the same test as the 'make check' test in ktools
    * ftest - this is an extended set of tests for the Financial Module (fmcalc)

----

* `ktools <https://github.com/OasisLMF/ktools>`_

ktools (kernel tools) is the in-memory solution for the Oasis Kernel. The Kernel is provided as a toolkit of components 
(“ktools”) which can be invoked at the command line.

----

* `LloydsLab2019 <https://github.com/OasisLMF/LloydsLab2019>`_

This repository contains content for Lloyd's Lab 2019.

----

* `OasisAtScaleEvaluation <https://github.com/OasisLMF/OasisAtScaleEvaluation>`_

This is an evaluation repository for testing the redesigned oasis architecture, where the keys lookup and analyses are now 
distributed across a pool of workers

----

* `OasisAzureDeployment <https://github.com/OasisLMF/OasisAzureDeployment>`_

OasisAzureDeployment can be used to manage, deploy, run, monitor, and configure models using the Azure platform.

----

* `OasisEvaluation <https://github.com/OasisLMF/OasisEvaluation>`_

The Oasis Evalutaion repository can be use to spin up an Oasis enviroment to quickly and efficiently run and test models.
The Oasis Platform release now includes a full API for operating catastrophe models and a general consolidation of the 
platform architecture. Windows SQL server is no longer a strict requirement. The platform can be run via docker containers 
on a single machine or, if required, scaled up to run on a cluster.

----

* `OasisLMF <https://github.com/OasisLMF/OasisLMF>`_

The ``oasislmf`` Python package, loosely called the *model development kit (MDK)* or the *MDK package*, provides a command 
line toolkit for developing, testing and running Oasis models end-to-end locally, or remotely via the Oasis API. It can 
generate ground-up losses (GUL), direct/insured losses (IL) and reinsurance losses (RIL). It can also generate 
deterministic losses at all these levels.

----

* `OasisModels <https://github.com/OasisLMF/OasisModels>`_

This repository houses example Oasis models for use in demonstrations and testing. Information on these models can be found 
in :doc:`../../sections/Oasis-models`

----

* `OasisPiWind <https://github.com/OasisLMF/OasisPiWind>`_

This is the original test model in Oasis and is an example of a multi-peril model implementation representing ficticious 
events with wind and flood affecting the Town of Melton Mowbray in England.

----

* `OasisPlatform <https://github.com/OasisLMF/OasisPlatform>`_

This repository provides core components of the Oasis platform, specifically:
    * ``DJango`` application that provides the Oasis REST API
    * ``Celery worker`` for running a model

----


* `OasisPlatformLot3 <https://github.com/OasisLMF/OasisPlatformLot3>`_

?

----

* `OasisUI <https://github.com/OasisLMF/OasisUI>`_

This repository houses the Oasis User Interface (UI). This is a web-browser application and is the front-end of the Oasis 
framework. It enables a user to import their exposure and financial data before executing a cat model. The results produced 
by the model are based on the user-defined outputs, which are extensively customisable, catering for most user requirements.

----

* `OasisWorkerController <https://github.com/OasisLMF/OasisWorkerController>`_ **This is labelled as public archive - so not sure if it should be here?**

This repository contains an example of how you can control workers in your oasis deployment. The process connects to 
the websocket in the api and monitors it for changes in the queue utilization.

----

* `ODS_OpenExposureData <https://github.com/OasisLMF/ODS_OpenExposureData>`_

This repository contains extensive information on the :doc:`../../sections/OED` format.

----

* `ODS_OpenResultsData <https://github.com/OasisLMF/ODS_OpenResultsData>`_

This repository contains extensive information on the :doc:`../../sections/ORD` format.

----

* `ODS_Tools <https://github.com/OasisLMF/ODS_Tools>`_

ODS Tools is a Python package designed to support users of the Oasis Loss Modelling Framework (Oasis LMF). This package 
includes a range of tools for working with Oasis data files, including loading, conversion and validation, in accordance 
with :doc:`../../sections/OED` format.

----

* `OpenDataTransform <https://github.com/OasisLMF/OpenDataTransform>`_

This repository houses the Open Data Transformation Framework. This is an industry collaboration to develop a framework for 
converting catastrophe model exposure data from one data format to another. Detailed documentation on this framework can be 
found at https://oasislmf.github.io/OpenDataTransform/.

----

* `ParisWindstormModel <https://github.com/OasisLMF/ParisWindstormModel>`_

This is very small, single peril model used for demonstration of how to build a simple model in Oasis.

----

* `ReinsuranceTestTool <https://github.com/OasisLMF/ReinsuranceTestTool>`_

This is a test tool for new Oasis reinsurance functionality. A library of worked examples will be created that will be used to validate:
    * the interpretation of the Open Exposure Data (OED) input format
    * the execution logic of the Oasis FM

----

* `water_seller <https://github.com/OasisLMF/water_seller>`_

This is a tool for handling local processes in order to run OasisLMF products.

----

* `Workshop2019 <https://github.com/OasisLMF/Workshop2019>`_

This repository contains content for the 2019 Oasis workshop.

----

* `Workshop2021 <https://github.com/OasisLMF/Workshop2021>`_

This repository contains content for the 2021 Oasis workshop.

----

* `Workshop2022 <https://github.com/OasisLMF/Workshop2022>`_

This repository contains content for the 2022 Oasis workshop.

----

* `ZurichWorkshop2018 <https://github.com/OasisLMF/ZurichWorkshop2018>`_

This repository contains content for the 2018 Zurich workshop.