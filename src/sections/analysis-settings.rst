Analysis Settings
=================

The run time settings for the analysis are controlled by the analysis_settings.json file which is a user supplied file 
detailing all of the options requested for the run (model to run, exposure set to use, number of samples, occurrence 
options, outputs required, etc.). In the MDK, the analysis settings file must be specified as part of the command line 
arguments (or in the oasislmf.json configuration file) and in the platform, it needs to be posted to the endpoint. A full 
json schema for the available options in the analysis settings file can be found here:

https://github.com/OasisLMF/ODS_Tools/blob/develop/ods_tools/data/analysis_settings_schema.json

|

----

``analysis_settings``
---------------------

``analysis_settings`` requires ``model_supplier_id``, ``model_name_id``, ``model_settings``, ``gul_output``, and ``gul_summaries``.

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json
    :hide_key: /**/definitions
|

``/output_summaries``
*********************

``output_summaries`` only requires ``id``.

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries

----

|

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/id

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/oed_fields

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/summarycalc

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/eltcalc

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/aalcalc

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/pltcalc

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/lec_output

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/leccalc

----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/definitions/output_summaries/items/properties/ord_output


----

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/analysis_settings_schema.json#/properties

|




