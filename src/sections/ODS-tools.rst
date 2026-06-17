ODS Tools
=========

On this page:
-------------

* :ref:`intro_ODS_Tools`
* :ref:`analysis_settings`
* :ref:`exposure_data`
* :ref:`installation`
* :ref:`cli_ODS_Tools`
* :ref:`links_ODS_Tools`

|

.. _intro_ODS_Tools:

Introduction
************

----

ODS Tools is a Python package designed to manage :doc:`../../sections/ODS` data, and ensure that it complies with the
:doc:`ODS <../../sections/ODS>` schema. It includes a range of tools for working with Oasis data files, including loading,
conversion, validation, and generation of synthetic test data. This package implements the
`ODS Open Exposure Data <https://github.com/OasisLMF/ODS_OpenExposureData>`_ standard.

As a separate service, the package includes functionality to manage :doc:`../../sections/model_settings` and
:doc:`../../sections/analysis_settings` files that are used to perform an analysis.

ODS tools comprises primarily of two parts:

* :ref:`analysis_settings`
* :ref:`exposure_data`


|

.. _analysis_settings:

Management of analysis settings
********************************

----

ODS Tools manages two settings files: ``model_settings.json`` and ``analysis_settings.json``. These are used in both the
Platform and MDK for running models.

* ``analysis_settings.json`` is the main user input. This is used to configure execution options, selected output reports,
  and (depending on the model) lookup and keys generation.

* ``model_settings.json`` presents all valid inputs set in an ``analysis_settings.json`` (along with some default values
  if no input is given). The intended use of this is that a UI, such as OasisUI, picks up the available options and renders
  them as widgets and input fields to generate an ``analysis_settings.json`` file.


|

.. _exposure_data:

Management of exposure data
****************************

----

This part of ODS Tools manages OED data through an ETL step. It checks the incoming data and ensures it is in the correct
format. This is achieved through several functionalities:

* It loads data from a range of sources (data stream, CSV and Parquet files, pandas DataFrames), storing all as a pandas
  DataFrame.

* It sets column types according to the OED specification.

* It performs validation against the OED schema, checking **source_coherence, required_fields, unknown_column,
  valid_values, perils, occupancy_code, construction_code, country_and_area_code**.

* It checks currencies in the exposure data and provides built-in functionality to convert to a single currency.

* It provides capability to convert exposure to different formats (CSV and Parquet are currently implemented).

More information can be found `here <https://github.com/OasisLMF/ODS_Tools/tree/develop#readme>`_.



|

.. _installation:

Installation
************

----

ODS Tools can be installed via pip:

.. code-block::

    pip install ods-tools

If using the ``transform`` command, install with optional extras:

.. code-block::

    pip install ods-tools[extra]

|

.. _cli_ODS_Tools:

Command Line Interface
**********************

----

ODS Tools provides a command line interface with the following subcommands:

.. code-block::

    ods_tools {convert,check,transform,combine,generate} ...

Each command supports ``-v LOGGING_LEVEL`` to control verbosity (debug:10, info:20, warning:30, error:40, critical:50).

----

convert
#######

Convert OED files to another format (e.g. CSV to Parquet) or OED version (e.g. 3.0 to 4.0).

Exposure data can be specified in several ways:

* By providing individual file paths: ``--location``, ``--account``, ``--ri-info``, ``--ri-scope``
* By providing an OED config JSON file: ``--config-json``
* By providing a directory containing standard-named OED files: ``--oed-dir``

Either ``--compression`` or ``--version`` must be provided.

.. code-block::

    # Convert to Parquet format
    ods_tools convert --location SourceLocOEDPiWind.csv --compression parquet --output-dir ./output

    # Convert an entire directory
    ods_tools convert --oed-dir ./exposure_data --compression parquet

    # Convert to a specific OED version
    ods_tools convert --location loc.csv --version 4.0.0 --output-dir ./output

    # Validate before converting
    ods_tools convert --location loc.csv --check-oed True --compression parquet --output-dir ./output

Key options:

* ``--compression`` — output format (e.g. ``parquet``, ``csv``, ``zip``, ``gzip``)
* ``--version`` — convert to a specific OED schema version
* ``--check-oed`` — validate OED files before converting (True/False)
* ``--oed-dir`` — path to a directory containing standard-named OED files
* ``--config-json`` — path to an OED config JSON file
* ``--validation-config`` — path to a custom validation config file
* ``--save-config`` — if True, saves an OED config file to the output directory

|

----

check
#####

Validate OED exposure files and optionally validate settings files.

.. code-block::

    # Check a location file
    ods_tools check --location SourceLocOEDPiWind.csv

    # Check an entire OED directory
    ods_tools check --oed-dir ./exposure_data

    # Check with model and analysis settings
    ods_tools check --location loc.csv --model-settings-json model_settings.json --analysis-settings-json analysis_settings.json

Key options:

* ``--location``, ``--account``, ``--ri-info``, ``--ri-scope`` — individual OED file paths
* ``--oed-dir`` — directory of standard-named OED files
* ``--config-json`` — OED config JSON file
* ``--model-settings-json`` — model settings JSON to validate
* ``--analysis-settings-json`` — analysis settings JSON to validate
* ``--validation-config`` — custom validation configuration file

|

----

transform
#########

Transform location and account data from other formats to OED (or vice versa), based on a mapping file.
Requires ``ods-tools[extra]`` to be installed.

.. code-block::

    ods_tools transform --config-file configuration.yaml

See :doc:`../sections/ODTF` for full documentation on the transformation framework and mapping files.

|

----

combine
#######

Combine multiple ORD (Open Results Data) analysis outputs into a single result set. Requires a configuration file
specifying how to combine the results.

.. code-block::

    ods_tools combine --analysis-dirs ./analysis_1 ./analysis_2 --config-file combine_config.json --output-dir ./combined_output

Key options:

* ``--analysis-dirs`` / ``-a`` — list of paths to analysis results directories (required)
* ``--config-file`` — path to the combine configuration JSON file (required)
* ``--output-dir`` — path to the output directory

See ``ods_tools combine --help`` for all options.

|

----

generate
########

Generate synthetic OED test data files from a JSON configuration. Useful for creating test portfolios, reproducing
issues, and benchmarking.

.. code-block::

    # Generate using a config file
    ods_tools generate --config config.json --output-dir ./output

    # Print an example config to get started
    ods_tools generate --example-config

    # Save example config to file then edit it
    ods_tools generate --example-config > my_config.json

    # Generate as Parquet
    ods_tools generate --config config.json --output-dir ./output -f parquet

    # List available OED schema versions
    ods_tools generate --list-versions

    # List all fields available for a given file type
    ods_tools generate --list-fields Loc --oed-version 4.0.0

Key options:

* ``--config`` — path to a JSON configuration file controlling what gets generated
* ``--output-dir`` — output directory (default: ``./oed_output``)
* ``-f`` / ``--format`` — output format: ``csv`` or ``parquet``
* ``--oed-version`` — OED schema version to generate against
* ``--example-config`` — print a sample configuration file and exit
* ``--list-versions`` — list available OED versions and exit
* ``--list-fields`` — list fields available for a given file type (e.g. ``Loc``, ``Acc``, ``ReinsInfo``, ``ReinsScope``)

The configuration file controls OED file types to generate (Loc, Acc, ReinsInfo, ReinsScope), number of rows, which
fields to include, financial terms, and portfolio structure. Use ``--example-config`` to get a starting template.

|

.. _links_ODS_Tools:

Links for further information
*****************************

----

Further information on ODS Tools can be found in the `GitHub repository <https://github.com/OasisLMF/ODS_Tools/tree/develop>`_.
