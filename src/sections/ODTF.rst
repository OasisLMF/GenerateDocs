ODTF
=========
Data transformation tool in ODS-tools

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


The `transform` command can be used to convert data from one format to another (e.g., from the AIR Cede format to OED). It will convert from a specific version of the source format to a specific version of the target format, for example from AIR Cede 10.0.0 to OED 3.0.2.

As of :doc:`../sections/ODS-tools` 3.2.3, we support conversions between AIR Cede and OED formats.


----

.. _inputs:

Inputs
************



For a transformation to run, the necessary input files should be present.
The input files you will need to run a transformation are:



**Configuration file**

See, e.g., this `example configuration file <https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/odtf/examples/example_config.yaml>`_:

|
.. code-block:: yaml

    transformations:
      loc: # Transformation name
        input_format:
          name: Cede_Location
          version: 10.0.0
        output_format:
          name: OED_Location
          version: 3.0.2
        runner:
          batch_size: 150000 # Number of rows to process in a single batch
        extractor:
          options:
            path: ./cede_location_1000.csv # Path to the input file
            quoting: minimal
        loader:
          options:
            path: ./oed_location_1000.csv # Path to the output file
            quoting: minimal
|
 
The configuration file contains a list of transformations to run (currently loc for location and acc for account data).
Each transformation includes name and version of the input and output formats, the (optional) batch size, and the paths to the input (extractor) and output (loader) files.

To connect to a database, the extractor should include the database connection details. For example, see this `example configuration file <https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/odtf/examples/example_config_db.yaml>`_:

|
.. code-block:: yaml

    transformations:
      loc: # Transformation name
        input_format:
          name: Cede_Location
          version: 10.0.0
        output_format:
          name: OED_Location
          version: 3.0.2
        runner:
          batch_size: 150000 # Number of rows to process in a single batch
        extractor:
          type: mssql # other options are 'postgres' and 'sqlite'. Assumes a file if not specified
          options:
            host: localhost
            database: AIRExposure_CEDE
            port: 1433
            user: user
            password: password
            sql_statement: ./sql/cede_location.sql # Path to the SQL file
        loader:
          options:
            path: ./oed_location_1000.csv # Path to the output file
            quoting: minimal


**Input data**

The input data should be in the format that you want to transform from. For example, if you want to transform data from AIR Cede to OED, the input data should be in the AIR Cede format.
File types supported:
.csv

Database connections supported:
mssql
postgres
sqlite


**SQL statement**

If the input data is in a database, the extractor should include the path to an SQL file containing the query to extract (and, if necessary, rename) the data.
For example, see this `example SQL file <https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/odtf/examples/sql/cede_location.sql>`_.

**Mapping file**

A mapping file is a file in .yaml format that describes how to run a conversion between the source and target formats and vice versa.
Multiple mapping files can be used together to define a mapping between a source and destination format that do not appear in the same mapping file. I.e., A mapping file for model A to B and and a mapping file for Model B to C, can be used to transform data directly from A to C.

Transformations can copy one field into another, substitute field values using a replace function, or include conditional transformation using a where clause. For columns that can contain multiple values (the LocPerils column in AIR Cede which could contain, for example "CF, CH, EQ"), the replace_multiple allows to input a separator used in the cell to split the values.
Only the transformations involving columns present in the input file will be run.


For example, see the `Cede-OED mapping file <https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/odtf/data/mappings/mapping_loc_Cede-OED.yaml>`_



----

.. _use:

Usage
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
A data validation file contains comparisons of various metrics in both the input file and output file.
For example, the sum of Total Insured Value grouped by Occupancy Type and Currency. The fields and operations are defined by the user in the validation definition files.
The validation definition file is in .yaml format.
See, for example, this `example validation file <https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/odtf/data/validators/validation_OED_Location_loc.yaml>`_.


.. note::
  The ODTF and the transform command are adapted from the `Open Data Transformation Framework <https://oasislmf.github.io/OpenDataTransform/>`_.
|