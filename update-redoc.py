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
MODEL_SETTINGS_SCHEMA = './schema/model_settings/model_schema.json'
ANALYSIS_SETTING_SCHEMA = './schema/analysis_settings/analysis_schema.json'
PLAT_V1_SCHEMA = './schema/v1/oasis-platform-schema.json'
PLAT_V2_SCHEMA = './schema/v2/oasis-platform-schema.json'

# urls
PLAT_V1_VER = '1.8.0'
PLAT_V2_VER = '2.2.0'
PLAT_V1_URL = f"https://github.com/OasisLMF/OasisPlatform/releases/download/{PLAT_V1_VER}/openapi-schema-{PLAT_V1_VER}.json"
PLAT_V2_URL = f"https://github.com/OasisLMF/OasisPlatform/releases/download/{PLAT_V2_VER}/openapi-schema-{PLAT_V2_VER}.json"


def read_file(file):
    with open(file, mode='rb') as f:
        return f.read()

def write_json(file, data):
    with open(file, mode='w') as f:
        json.dump(data, f)


#def copy_files(src, dst):
#    for root, dirs, files in os.walk(src):
#        rel_dir = os.path.relpath(root, src)
#        dst_dir = os.path.join(dst, rel_dir)
#
#        if not os.path.exists(dst_dir):
#            os.makedirs(dst_dir)
#
#        for file in files:
#            src_file = os.path.join(root, file)
#            dst_file = os.path.join(dst_dir, file)
#            shutil.copy2(src_file, dst_file)

"""
        spec.info['x-logo'] = { url: "https://oasislmf.github.io/_static/OASIS_LMF_COLOUR.png" };

        // Switch schema type
        delete spec.swagger
        spec['openapi'] = "3.0.0";

        // Insert description
        fetch('./description.md')
"""


## Patch model settings schema
model_schema = ModelSettingSchema().schema
model_desc = read_file('./schema/model_settings/description.md').decode()
model_temp = json.loads(read_file('./schema/model_settings/redoc_template.json'))

model_temp['info']['description'] = model_desc
model_temp['info']['version'] = ods_tools.__version__
model_temp['info']['x-logo'] = { "url": "https://oasislmf.github.io/_static/OASIS_LMF_COLOUR.png" }
model_temp['definitions']['ModelParameters'] = model_schema
write_json(MODEL_SETTINGS_SCHEMA, model_temp)

## Patch analysis Settings schema
analysis_schema = AnalysisSettingSchema().schema
analysis_desc = read_file('./schema/analysis_settings/description.md').decode()
analysis_temp = json.loads(read_file('./schema/analysis_settings/redoc_template.json'))

analysis_temp['info']['description'] = analysis_desc
analysis_temp['info']['version'] = ods_tools.__version__
analysis_temp['info']['x-logo'] = { "url": "https://oasislmf.github.io/_static/OASIS_LMF_COLOUR.png" }
analysis_temp['definitions']['AnalysisSettings'] = analysis_schema
write_json(ANALYSIS_SETTING_SCHEMA, analysis_temp)


plat_1_schema = requests.get(PLAT_V1_URL).json()
plat_1_desc = read_file('./schema/v1/description.md').decode()

plat_1_schema['info']['description'] = plat_1_desc
plat_1_schema['info']['x-logo'] = { "url": "https://oasislmf.github.io/_static/OASIS_LMF_COLOUR.png" }
del plat_1_schema['swagger']
plat_1_schema['openapi'] = "3.0.0"
write_json(PLAT_V1_SCHEMA, plat_1_schema)



plat_2_schema = requests.get(PLAT_V1_URL).json()
plat_2_desc = read_file('./schema/v2/description.md').decode()

plat_2_schema['info']['description'] = plat_2_desc
plat_2_schema['info']['x-logo'] = { "url": "https://oasislmf.github.io/_static/OASIS_LMF_COLOUR.png" }
del plat_2_schema['swagger']
plat_2_schema['openapi'] = "3.0.0"
write_json(PLAT_V2_SCHEMA, plat_2_schema)



docker_basecmd = ['docker', 'run', '--rm', '-v', f'{os.getcwd()}:/spec', "--user", f"{os.getuid()}", 'redocly/cli', 'build-docs']

build_args = [
    [MODEL_SETTINGS_SCHEMA, '--output', 'build/html/model_settings.html'],
    [ANALYSIS_SETTING_SCHEMA, '--output', 'build/html/analysis_settings.html'],
    [PLAT_V1_SCHEMA, '--output', 'build/html/platform_1.html'],
    [PLAT_V2_SCHEMA, '--output', 'build/html/platform_2.html'],
]

for redoc_build in build_args:
    print("Running docker: " + " ".join(docker_basecmd + redoc_build))
    result = subprocess.run(docker_basecmd + redoc_build, capture_output=True, text=True)
    print("Standard Output:")
    print(result.stdout)

    print("\nStandard Error:")
    print(result.stderr)
