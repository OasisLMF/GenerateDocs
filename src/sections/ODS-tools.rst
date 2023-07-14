ODS Tools
=========

On this page:
-------------

* :ref:`intro_ODS_Tools`
* :ref:`analysis_settings`
* :ref:`exposure_data`
* :ref:`installation`
* :ref:`links_ODS_Tools`

|

.. _intro_ODS_Tools:

Introduction
************

----

ODS Tools is a Python package designed to manage :doc:`../../sections/ODS` data, and ensure that this is complying with the 
:doc:`../../sections/ODS` schema. This package is designed to be compatible with Oasis files, but can operate independently  
with any :doc:`../../sections/ODS` data. It includes a range of tools for working with Oasis data files, including loading, 
conversion, and validation. This package is in accordance with :doc:`../../sections/ODS`. 

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

* ``model_settings.json`` presents all valid inputs set in an analysis_settings.json (along with some default values 
  if no input is given). The intended use pf this is that a UI, such as OasisUI, picks up the available options and render 
  them as widgets and input fields to generate an analysis_settings.json file.


|

.. _exposure_data:

Management of exposure data
****************************

----

This part of ODS Tools is to manage OED data through an ELT step. ELT is crucial as it checks the incoming data and makes 
sure it's in the correct format. This is achieved through several functionalities:

* It loads the data from a range of sources (which are currently: data stream, csv and parquet files, pandas dataframe). 
  This is then stored all as a pandas dataframe.

* It sets the columns in the dataframe to correct type. More information on the columns and type can be found in the `Open 
  Exposure Data Spec spreadsheet <https://github.com/OasisLMF/ODS_OpenExposureData/blob/develop/OpenExposureData/Docs/
  OpenExposureData_Spec.xlsx>`_.

* It performs checks to ensure the data is correct by validating that the OED data according to the OED schema in 
  the `Open Exposure Data Spec spreadsheet <https://github.com/OasisLMF/ODS_OpenExposureData/blob/develop/OpenExposureData/
  Docs/OpenExposureData_Spec.xlsx>`_. This currently checks **source_coherence, required_fields, unknown_column, valid_values, 
  perils, occupancy_code, construction_code, country_and_area_code**

* It checks the currencies in the exposure data. Only one currency is required for the exposure, so there is built in 
  functionality to convert to one currency type if required.

* It provides capability to convert the exposure to different format if required (csv and parquet are the one currently 
  implemented).

More information of these capabilities can be found `here <https://github.com/OasisLMF/ODS_Tools/tree/develop#readme>`_.



|

.. _installation:

Installation and Application
****************************

----

ODS Tools can be installed via pip by running the following command:

.. code-block:: python 

    pip install ods-tools

Once installed, ODS Tools can be used utilised via the command line interface to quickly convert oed files.

Example :

.. code-block:: python 

    ods_tools convert --location path_to_location_file --path output folder

.. note::
    See ``ods_tools convert --help`` for more options.
|



.. _links_ODS_Tools:

Links for further information
*****************************

----

Further information on ODS Tools can be found `here <https://github.com/OasisLMF/
ODS_Tools/blob/master/README.md>`_.