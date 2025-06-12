#!/usr/bin/env python3
import json
import requests
import shutil
import os
import subprocess

import ods_tools
from os import path
from ods_tools.oed.setting_schema import ModelSettingSchema, AnalysisSettingSchema

# Locations
MODEL_SETTINGS_SCHEMA = './src/schema/model_settings.json'
ANALYSIS_SETTING_SCHEMA = './src/schema/analysis_settings.json'
PLAT_V1_SCHEMA = './src/schema/platform-1.json'
PLAT_V2_SCHEMA = './src/schema/platform-2.json'

# urls
PLAT_VER = '2.4.4'
PLAT_V1_URL = f"https://github.com/OasisLMF/OasisPlatform/releases/download/{PLAT_VER}/v1-openapi-schema-{PLAT_VER}.json"
PLAT_V2_URL = f"https://github.com/OasisLMF/OasisPlatform/releases/download/{PLAT_VER}/v2-openapi-schema-{PLAT_VER}.json"


def read_file(file):
    with open(file, mode='rb') as f:
        return f.read()

def write_json(file, data):
    with open(file, mode='w') as f:
        json.dump(data, f)

def patch_schema(base_schema, version, description):
    base_schema['info']['x-logo'] = { "url": "https://oasislmf.github.io/_images/OASIS_LMF_COLOUR.png" }
    base_schema['info']['description'] = description
    base_schema['info']['version'] = version
    return base_schema

## Patch model settings schema
model_schema = ModelSettingSchema().schema
model_desc = read_file('./redoc/model_settings/description.md').decode()
model_temp = json.loads(read_file('./redoc/model_settings/redoc_template.json'))
model_temp['definitions']['ModelParameters'] = model_schema
write_json(MODEL_SETTINGS_SCHEMA, patch_schema(model_temp, ods_tools.__version__, model_desc))

## Patch analysis Settings schema
analysis_schema = AnalysisSettingSchema().schema
analysis_desc = read_file('./redoc/analysis_settings/description.md').decode()
analysis_temp = json.loads(read_file('./redoc/analysis_settings/redoc_template.json'))
analysis_temp['definitions']['AnalysisSettings'] = analysis_schema
write_json(ANALYSIS_SETTING_SCHEMA, patch_schema(analysis_temp, ods_tools.__version__, analysis_desc))

# Patch Platform 1 schmea
plat_1_schema = requests.get(PLAT_V1_URL).json()
plat_1_desc = read_file('./redoc/v1/description.md').decode()
write_json(PLAT_V1_SCHEMA, patch_schema(plat_1_schema, PLAT_VER ,plat_1_desc))

# Patch Platform 2 schema
plat_2_schema = requests.get(PLAT_V2_URL).json()
plat_2_desc = read_file('./redoc/v2/description.md').decode()
write_json(PLAT_V2_SCHEMA, patch_schema(plat_2_schema, PLAT_VER ,plat_2_desc))

## Docker build arguments
#docker_basecmd = ['docker', 'run', '--rm', '-v', f'{os.getcwd()}:/spec', "--user", f"{os.getuid()}", 'redocly/cli', 'build-docs']
#theme_args = ['--theme.openapi.fontFamily', 'Raleway'] # https://redocly.com/docs/api-reference-docs/configuration/theming/
#build_args = [
#    [MODEL_SETTINGS_SCHEMA, '--output', 'build/html/schema/model_settings/index.html'],
#    [ANALYSIS_SETTING_SCHEMA, '--output', 'build/html/schema/analysis_settings/index.html'],
#    [PLAT_V1_SCHEMA, '--output', 'build/html/schema/v1/index.html'],
#    [PLAT_V2_SCHEMA, '--output', 'build/html/schema/v2/index.html'],
#]
#
## Run docker build
#for redoc_build in build_args:
#    exec_docker_cmd = docker_basecmd + redoc_build + theme_args
#    print("Running docker: " + " ".join(exec_docker_cmd))
#
#    result = subprocess.run(exec_docker_cmd, capture_output=True, text=True)
#    print("Standard Output:")
#    print(result.stdout)
#    print("\nStandard Error:")
#    print(result.stderr)
