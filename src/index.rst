Introduction:
=============

----

* **What is Oasis**: The Oasis Loss Modelling Framework is an open source catastrophe modelling platform, free to use by anyone.
  It is also a community that seeks to unlock and change the world around catastrophe modelling to better understand risk in insurance and beyond. 
  While its development is largely driven by the global (re-)insurance community, it seeks to provide tools and utility to all.
  For more information about the Oasis LMF initiative visit `oasislmf.org <http://www.oasislmf.org/>`_.

* **How the documentation is structured**: This documentation is broken down into 4 main areas: Model developers, Model 
  users, Installing and developing Oasis, and Supporting and Oasis model deployment. These are the different use cases that 
  are detailed in this documentation. By selecting your use case, the relevant information can be accessed.

|

Overview
--------

----

.. figure:: images/oasis_ecosystem.jpg
    :alt: Oasis Ecosystem

    Oasis Ecosystem

|

Our main users are:
*******************

----

**Model developers**, who build, test and publish the risk models. 
They are typically scientists or software developers, working in a risk modelling company or academia.

**Risk analysts** who operate the models for decision support purposes.
The core user group are analysts at insurance or reinsurance organizations who are running the models to support pricing and portfolio management.
This would also cover government and third sector users.

**Enterprise risk systems** at insurance or reinsurance organizations, where Oasis risk models will be integrated using APIs into pricing and portfolio management workflows.

|

Our software components are:
****************************

----

**Oasis Platform** is a catastrophe modelling system that encompasses a set of data standards; an API; and tools and components for building and running models.
This is the core part of Oasis underpinning the other components and is where most of the domain specific code and performance optimization is required.

**Oasis User Interface (UI)** is a web-based application for uploading exposure data, running models deployed in Oasis, and retrieving results data.
It is targeted at operating models by (re)insurance companies in in conjunction with existing exposure management and reporting tools; model evaluation; and using models in government or third sector contexts.

**Oasis Model Development Kit (MDK)** is a set of tools for building, calibrating and creating a model, ready to be deployed into the Oasis Platform.
It is designed with a model developer or academic user in mind, who are likely to be comfortable working directly with the data from the command line or programmatically.

**Oasis Model Library** is a hosted catalogue for Oasis models, hosted in AWS. 
It allows regression of the models after updates to the Oasis Platform code, and validation of model operation and scalability within a hosted Oasis Platform.

----

.. toctree::
    :titlesonly:
    :caption: Home:

    home/introduction.rst
    Oasis GitHub <https://github.com/OasisLMF>
    home/git-repo.rst
    home/FAQs.rst

.. toctree::
    :titlesonly:
    :caption: Use Cases:

    use_cases/model-developer
    use_cases/model-users
    use_cases/installing-deploying-Oasis

.. toctree::
    :titlesonly:
    :caption: Sections:

    sections/absolute-damage.rst
    sections/analysis_settings
    sections/API.rst
    sections/camel.rst
    sections/correlation.rst
    sections/deployment.rst
    sections/disaggregation.rst
    sections/financial-module.rst
    sections/keys-service.rst
    sections/ktools.rst
    sections/model-data-library.rst
    sections/model-development-kit.rst
    sections/model-providers.rst
    sections/model_settings
    sections/modelling-methodology.rst
    sections/Oasis-evaluation.rst
    sections/Oasis-file-formats.rst
    sections/Oasis-model-data-formats.rst
    sections/Oasis-models.rst
    sections/Oasis-platform.rst
    sections/Oasis-UI.rst
    sections/Oasis-workflow.rst
    sections/OasisLMF-package.rst
    sections/ODS-tools.rst
    sections/ODS.rst
    sections/OED.rst
    sections/ORD.rst
    sections/platform_1
    sections/platform_2
    sections/post-loss-amplification.rst
    sections/pytools.rst
    sections/releases.rst
    sections/results.rst
    sections/SaaS-providers.rst
    sections/sampling-methodology.rst
    sections/versioning.rst
    
.. 
  sections to be populated: sections/pre-analysis-adjustments.rst, sections/errors.rst, sections/complex-model.rst

