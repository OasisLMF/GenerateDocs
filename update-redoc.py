#!/usr/bin/env python3
import json 
import requests 
import shutil
import os

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



with open(MODEL_SETTINGS_SCHEMA, "w") as f:
    json.dump(ModelSettingSchema().schema, f)
with open(ANALYSIS_SETTING_SCHEMA, "w") as f:
    json.dump(AnalysisSettingSchema().schema, f)
with open(PLAT_V1_SCHEMA, "w") as f:
    rsp_1 = requests.get(PLAT_V1_URL)
    json.dump(rsp_1.json(), f)
with open(PLAT_V2_SCHEMA, "w") as f:
    rsp_2 = requests.get(PLAT_V2_URL)
    json.dump(rsp_2.json(), f)


def copy_files(src, dst):
    for root, dirs, files in os.walk(src):
        rel_dir = os.path.relpath(root, src)
        dst_dir = os.path.join(dst, rel_dir)

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_dir, file)
            shutil.copy2(src_file, dst_file)

SOURCE_DIR = path.abspath('./schema/')
TARGET_DIR = path.abspath('./build/html/schema/')
copy_files(SOURCE_DIR, TARGET_DIR)
