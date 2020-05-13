Model Development Kit (MDK)
===========================

The oasislmf Python package comes with a command line interface for creating, testing and managing models.
The tool is split into several namespaces that group similar commands. 
For a full list of namespaces use ``oasislmf --help``, and ``oasislmf <namespace> --help`` for a full list of commands available in each namespace.

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
