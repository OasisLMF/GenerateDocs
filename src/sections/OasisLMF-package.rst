OasisLMF Package
================

The ``oasislmf`` Python package, loosely called the model development kit (MDK) or the MDK package, provides a command line 
toolkit for developing, testing and running Oasis models end-to-end locally, or remotely via the Oasis API. It can generate 
ground-up losses (GUL), direct/insured losses (IL) and reinsurance losses (RIL). It can also generate deterministic losses 
at all these levels.

Model Development Kit (MDK)
---------------------------

The oasislmf Python package comes with a command line interface for creating, testing and managing models.
The tool is split into several namespaces that group similar commands. 
For a full list of namespaces use ``oasislmf --help``, and ``oasislmf <namespace> --help`` for a full list of commands 
available in each namespace.

config
------

.. autocli:: oasislmf.cli.config.ConfigCmd
   :noindex:


model
-----


``oasislmf model generate-exposure-pre-analysis``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.model.GenerateExposurePreAnalysisCmd
   :noindex:


``oasislmf model generate-keys``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.model.GenerateKeysCmd
   :noindex:

``oasislmf model generate-losses``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.model.GenerateLossesCmd
   :noindex:

``oasislmf model generate-oasis-files``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.model.GenerateOasisFilesCmd
   :noindex:

``oasislmf model run``
^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.model.RunCmd
   :noindex:

exposure
--------

``oasislmf exposure run``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.model.RunCmd
   :noindex:

API client 
----------

``oasislmf api run``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cli.api.RunApiCmd
   :noindex:



version
-------

.. autocli:: oasislmf.cli.version.VersionCmd
   :noindex:




Run a model using the Oasis MDK 
-------------------------------

The Model Development Kit (MDK) is the best way to get started using the Oasis platform.
The MDK is a command line tookit providing command line access to Oasis' modelling functionality. 
It is installed as a Python package, and available from PYPI: `OasisLMF PYPI module <https://pypi.python.org/pypi/oasislmf>`_.

The OasisLMF package has the following dependencies:

*Debian*: 
    g++, build-essential, libtool, zlib1g-dev, autoconf, unixobdbc-dev
*RHEL*:
    Development Tools, zlib-devel

To install the OasisLMF package run:

.. code-block:: python

    pip install oasislmf

.. warning:: Windows is not directly supported for running the MDK.
    You can run the Oasis MDK on Linux or MacOS.
    You can only run on Windows using a docker container or Linux Subsystem (WSL).

