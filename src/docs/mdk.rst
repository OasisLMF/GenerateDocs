Model Development Kit (MDK)
===========================

The model development kit (MDK) is the `oasislmf <https://pypi.org/project/oasislmf/>`_ Python package. It provides various features and tools for developing, implementing, running and testing Oasis models. It has two features - a command line interface, and a set of Python modules and class frameworks for building and running lookups, exposure management, and general utilities.

CLI
---

The package is named ``oasislmf`` and has several top-level command groups / namespaces, which are described below.

test
~~~~
(Deprecated) Tests a model by running some API checks via an API client connecting to a running API server, and also generates a Docker file for a model API tester Docker image.

.. autocli:: oasislmf.cmd.test.TestModelApiCmd
    :noindex:

.. autocli:: oasislmf.cmd.test.GenerateModelTesterDockerFileCmd
    :noindex:

bin
~~~
Generating and processes model binary files, including validation of CSV-to-bin conversion tools.

.. autocli:: oasislmf.cmd.bin.BuildCmd
    :noindex:

.. autocli:: oasislmf.cmd.bin.CleanCmd
    :noindex:

.. autocli:: oasislmf.cmd.bin.CheckCmd
    :noindex:

config
~~~~~~
Displays the MDK configuration (JSON) file format for running a model end-to-end (via ``model run``).

.. autocli:: oasislmf.cmd.config.ConfigCmd
   :noindex:

model
~~~~~
Provides various options for working with models, including transforming source exposure and/or accounts (financial terms) files to the canonical Oasis format, generating an Rtree file index for the area peril lookup component of the built-in lookup framework, generating keys files from lookups, generating Oasis input CSV files (GUL + optionally FM), generating losses from a preexisting set of Oasis input CSV files, running a model end-to-end.

``oasislmf model transform-source-to-canonical``
________________________________________________
Transforms a source exposure or accounts CSV file (in either EDM or OED format) to an appropriate canonical Oasis format.

.. autocli:: oasislmf.cmd.model.TransformSourceToCanonicalFileCmd
    :noindex:

``oasislmf model transform-canonical-to-model``
_______________________________________________
Transforms a canonical exposure CSV file (in either EDM or OED format) to a suitable format that can be processed by the model lookup.

.. autocli:: oasislmf.cmd.model.TransformCanonicalToModelFileCmd
    :noindex:

``oasislmf model generate-peril-areas-rtree-file-index``
________________________________________________________
Generates an Rtree file index for the area peril lookup component of the built-in lookup framework.

.. autocli:: oasislmf.cmd.model.GeneratePerilAreasRtreeFileIndexCmd
    :noindex:

``oasislmf model generate-keys``
________________________________
Generates keys files from lookups directly (no keys server involved).

.. autocli:: oasislmf.cmd.model.GenerateKeysCmd
   :noindex:

``oasislmf model generate-oasis-files``
_______________________________________
Generates Oasis input CSV files (GUL + optionally FM).

.. autocli:: oasislmf.cmd.model.GenerateOasisFilesCmd
   :noindex:

``oasislmf model generate-losses``
__________________________________
Generates losses from a preexisting set of Oasis input CSV files.

.. autocli:: oasislmf.cmd.model.GenerateLossesCmd
   :noindex:

``oasislmf model run``
______________________
Runs a model end-to-end.

.. autocli:: oasislmf.cmd.model.RunCmd
   :noindex:

version
-------
dDisplays the installed package version.

.. autocli:: oasislmf.cmd.version.VersionCmd
   :noindex:
