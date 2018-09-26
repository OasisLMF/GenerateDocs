Model Development Kit (MDK)
===========================

The oasislmf Python package comes with a command line interface for creating, testing and managing models.
The tool is split into several namespaces that group similar commands. 
For a full list of namespaces use ``oasislmf --help``, and ``oasislmf <namespace> --help`` for a full list of commands available in each namespace.

Overview


Python package


config
-----

.. autocli:: oasislmf.cmd.config.ConfigCmd
   :noindex:


model
-----

``oasislmf model generate-keys``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cmd.model.GenerateKeysCmd
   :noindex:

``oasislmf model generate-losses``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cmd.model.GenerateLossesCmd
   :noindex:

``oasislmf model generate-oasis-files``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cmd.model.GenerateOasisFilesCmd
   :noindex:

``oasislmf model run``
^^^^^^^^^^^^^^^^^^^^^^

.. autocli:: oasislmf.cmd.model.RunCmd
   :noindex:

version
-------

.. autocli:: oasislmf.cmd.version.VersionCmd
   :noindex:
