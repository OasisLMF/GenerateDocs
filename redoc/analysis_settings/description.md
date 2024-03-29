# Analysis Settings Overview

The run time settings for the analysis are controlled by the `analysis_settings.json` file which is a user supplied file detailing all of the options requested for the run (model to run, exposure set to use, number of samples, occurrence options, outputs required, etc.). In the MDK, the analysis settings file must be specified as part of the command line arguments (or in the oasislmf.json configuration file) and in the platform, it needs to be posted to the endpoint. A full json schema for the available options in the analysis settings file can be found here:

https://github.com/OasisLMF/ODS_Tools/blob/main/ods_tools/data/analysis_settings_schema.json

This is useful for more technical users who are looking to create their own UI or integrate Oasis with an existing system. The `analysis_settings` schema hierarchy is shown in `json` format in right column of the page. An interactive version of the schema, with descriptions and examples, can be found below: