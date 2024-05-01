Data transformations in ODS-tools
=========

On this page:
-------------

* :ref:`intro_ODTF`
* :ref:`inputs`
* :ref:`use`
* :ref:`validation`

----

.. _intro_ODTF:

Introduction
************


The `transform` command is used to convert data from one format to another (e.g., from the AIR Cede format to OED). Note that it will convert from a specific version of the source format to a specific version of the target format, for example from AIR Cede 10.0.0 to OED 3.0.2.


----

.. _inputs:

Inputs
************



For a transformation to run, the necessary input files should be present.
The input files you will need to run a transformation are:

Configuration file

It should include...

For example, [link to odtf/example/config.yaml]


Input data

The input data should be in the format that you want to transform from. For example, if you want to transform data from AIR Cede to OED, the input data should be in the AIR Cede format.
File type supported:
.csv


Mapping file

A mapping file is

For example, [link to odtf/data/mapping/mapping_to_select.yaml]

----

.. _use:

Command line usage
************


Command line usage..

    ods_tools transform [-h] --config-file CONFIG_FILE [-v LOGGING_LEVEL] [--nocheck NOCHECK]

Transform data format to/from OED.

options:
  -h, --help            show this help message and exit

  --config-file CONFIG_FILE
                        Path to the config file

  -v LOGGING_LEVEL, --logging-level LOGGING_LEVEL
                        logging level (debug:10, info:20, warning:30, error:40, critical:50)

  --nocheck NOCHECK     if True, OED file will not be checked after transformation


----

.. _validation:

Validation
************


Validation is performed after a conversion to make sure that the output file is valid with respect to specific rules.
The validation rules are defined in the validation, see for example [link to odtf/data/validation/validate_oed.yaml].