Overview
========

The Oasis Loss Modelling Framework is an open source catastrophe modelling platform, free to use by anyone.
It is also a community that seeks to unlock and change the world around catastrophe modelling to better understand risk in insurance and beyond. 
While its development is largely driven by the global (re-)insurance community, it seeks to provide tools and utility to all.
For more information about the Oasis LMF initiative visit `oasislmf.org <http://www.oasislmf.org/>`_.

.. figure:: images/oasis_ecosystem.jpg
    :alt: Oasis Ecosystem

    Oasis Ecosystem

Our main users are:

**Model developers**, who build, test and publish the risk models. 
They are typically scientists or software developers, working in a risk modelling company or academia.

**Risk analysts** who operate the models for decision support purposes.
The core user group are analysts at insurance or reinsurance organizations who are running the models to support pricing and portfolio management.
This would also cover government and third sector users.

**Enterprise risk systems** at insurance or reinsurance organizations, where Oasis risk models will be integrated using APIs into pricing and portfolio management workflows.

Our software components are:

**Oasis Platform** is a catastrophe modelling system that encompasses a set of data standards; an API; and tools and components for building and running models.
This is the core part of Oasis underpinning the other components and is where most of the domain specific code and performance optimization is required.

**Oasis User Interface (UI)** is a web-based application for uploading exposure data, running models deployed in Oasis, and retrieving results data.
It is targeted at operating models by (re)insurance companies in in conjunction with existing exposure management and reporting tools; model evaluation; and using models in government or third sector contexts.

**Oasis Model Development Kit (MDK)** provides various features and tools for developing, implementing, running and testing Oasis models. It has two features - a command line interface, and a set of Python modules and class frameworks for building and running lookups, exposure management, and general utilities.

**Oasis Model Library** is a hosted catalogue for Oasis models, hosted in AWS. 
It allows regression of the models after updates to the Oasis Platform code, and validation of model operation and scalability within a hosted Oasis Platform.

.. toctree::
    :titlesonly:
    :caption: Getting started

    getting_started/mdk_quickstart
    getting_started/using_the_oasis_ui


.. toctree::
    :titlesonly:
    :caption: Developer guide

    developer_guide/platform_architecture
    developer_guide/development_approach
    developer_guide/github_repositories
    developer_guide/technology_stack
    developer_guide/release_process

.. toctree::
    :titlesonly:
    :caption: Modelling methodology 

    modelling_methodology/what_is_a_catastrophe_model
    modelling_methodology/simulation_methodology
    modelling_methodology/financial_modelling_and_exposure_data
    modelling_methodology/risk_metrics

.. toctree::
    :titlesonly:
    :caption: Module documentation

    docs/oasis_rest_api
    docs/mdk
    docs/modules
    docs/general

.. toctree::
    :titlesonly:
    :caption: Release Notes
    :maxdepth: 0

    releases/oasis_platform.md

.. toctree::
    :titlesonly:
    :caption: Changelogs
    :maxdepth: 0

    releases/ktools.md
    releases/oasislmf.md
