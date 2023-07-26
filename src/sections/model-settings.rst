Model Settings
==============

This is a configuration file provided with the model to specify important meta data about the model to model users and 
systems. It is supplied by the model provider and is a static document. A full specification of the model settings schema 
can be found here: https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/data/model_settings_schema.json

|

Model Settings Schema
------------------------

----

The tables below contain the ``model_settings_schema``, that can be found in the link above.

|


Model settings 
**************

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json
    :hide_key: /**/model_settings, /**/lookup_settings, /**/data_settings

----

``/model_settings``
******************

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/model_settings
    :hide_key: /**/event_set, /**/event_occurrence_id, /**/dropdown_parameters

|

``/model_settings/event_set``
############################

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/model_settings/properties/event_set

|

``/model_settings/event_occurrence_id``
######################################

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/model_settings/properties/event_occurrence_id

|

``/model_settings/dropdown_parameters``
######################################

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/model_settings/properties/dropdown_parameters

|

----

``/lookup_settings``
********************

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/lookup_settings

|

``/data_settings``
******************

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/data_settings
    :hide_key: /**/datafile_selectors

|

``/data_settings/datafile_selectors``
####################################

.. jsonschema:: https://raw.githubusercontent.com/OasisLMF/ODS_Tools/main/ods_tools/data/model_settings_schema.json#/properties/data_settings/properties/datafile_selectors





