#!/usr/bin/env python3

import requests
import json
import sys
from datetime import date

if __name__ == "__main__":

    headers = {
        'Accept': 'Content-Type: application/json',
    }

    # Fetch latests tags 
    tag_plat = requests.get('https://api.github.com/repos/OasisLMF/OasisPlatform/tags').json()[0]['name']
    tag_mdk = requests.get('https://api.github.com/repos/OasisLMF/OasisLMF/tags').json()[0]['name']
    tag_ui = requests.get('https://api.github.com/repos/OasisLMF/OasisUI/tags').json()[0]['name']
    tag_ktools = requests.get('https://api.github.com/repos/OasisLMF/ktools/tags').json()[0]['name']

    title = sys.argv[1].strip()
    if not title:
        release_title = "*Oasis Release:* ({}) - {}".format(tag_plat, date.today().strftime("%d %B, %Y"))
    else:
        release_title = "*{}:* ({}) - {}".format(title, tag_plat, date.today().strftime("%d %B, %Y"))

    slack_message = {
        "text": "Oasis Release {}".format(tag_plat),
        "blocks": [
         {
           "type": "section",
           "block_id": "main",
           "text": {
               "type": "mrkdwn",
               "text": release_title
            }   
        },
        {
           "type": "section",
           "block_id": "platform",
           "text": {
                "type": "mrkdwn",
                "text": f'• <https://github.com/OasisLMF/OasisPlatform/releases/tag/{tag_plat}|OasisPlatform {tag_plat}> (release notes)'
            }
        },
        {
           "type": "section",
           "block_id": "api",
           "text": {
                "type": "mrkdwn",
                "text": f'• <https://api.oasislmfdev.org/swagger/|API Schema {tag_plat}>'
            }
        },
        {
           "type": "section",
           "block_id": "mdk",
           "text": {
                "type": "mrkdwn",
                "text": f'• <https://github.com/OasisLMF/OasisLMF/releases/tag/{tag_mdk}|OasisLMF {tag_mdk}>'
            }
        },
        {
           "type": "section",
           "block_id": "ui",
           "text": {
                "type": "mrkdwn",
                "text": f'• <https://github.com/OasisLMF/OasisUI/releases/tag/{tag_ui}|Oasis UI {tag_ui}>'
            }
        },
        {
           "type": "section",
           "block_id": "ktools",
           "text": {
                "type": "mrkdwn",
                "text": f'• <https://github.com/OasisLMF/ktools/releases/tag/{tag_ktools}|Ktools {tag_ktools}>'
            }
        }
        ]
    }

    for web_hook in sys.argv[2:]:
        requests.post('https://hooks.slack.com/services/{}'.format(web_hook), 
                      headers=headers, data=json.dumps(slack_message))
