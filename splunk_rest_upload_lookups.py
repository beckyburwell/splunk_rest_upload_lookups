#!/usr/bin/env python3
# coding: utf-8

# Simple python script using Splunk lookup-editor https://splunkbase.splunk.com/app/1724 rest endpoint to upload lookups (wiki https://lukemurphey.net/projects/splunk-lookup-editor/wiki/REST_endpoints)


# Downloaded from https://github.com/mthcht/lookup-editor_scripts and modified
# Original author: mthcht (contact on Twitter)
# Modified by: Becky Burwell, April 26, 2023

#########################################################################################################################
# Usage: splunk_rest_upload_lookups.py splunk_head_url lookup_file splunk_app
#
# Example: splunk_rest_upload_lookups.py https://myhead:9999 /home/burwell/mylookup.csv search
#
# Troubleshoot lookup-editor errors on splunk: index=_internal (sourcetype=lookup_editor_rest_handler OR sourcetype=lookup_backups_rest_handler)
#########################################################################################################################

import json
import requests
import csv
import re
import logging
import pathlib
import sys
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable warning for insecure requests
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Setup logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s.%(msecs)03dZ splunk_rest_upload_lookups: %(levelname)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

# Get the parameters
if len(sys.argv) != 4:
   logging.critical ("Usage: splunk_rest_upload_lookups.py splunk_head_url lookup_file splunk_app")
   exit (1)
   
splunk_head_url = sys.argv[1]
lookup_file     = sys.argv[2]
splunk_app      = sys.argv[3]

# GET requests to this endpoint will execute get_lookup_contents() and POST requests to this endpoint will execute post_lookup_contents() from the lookup_editor_rest_handler.py in the lookup-editor app
splunk_management_service = "/services/data/lookup_edit/lookup_contents" #endpoint lookup-editor 

# Read data from CSV file
lookup_content = []
lookup_name = pathlib.Path(lookup_file).name
try:
   with open(lookup_file, encoding='utf-8', errors='ignore',newline='') as f:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
          lookup_content.append(row)
except  Exception as e:
   logging.error("Error reading {} : {}".format(lookup_file,e))
   exit (1)

# The file was read so now we can upload. Get the credentials
splunk_username = getpass.getpass(prompt='Splunk username: ', stream=None)
splunk_password = getpass.getpass(prompt='Splunk password: ', stream=None)

print ("")

# Send POST request to Splunk server
try:
   r = requests.post("{}{}".format(splunk_head_url,splunk_management_service),
                     verify=False,
                     auth=(splunk_username, splunk_password),
                     data={"output_mode": "json",
                           "namespace": splunk_app,
                           "lookup_file": lookup_name,
                           "contents": json.dumps(lookup_content)},
                     timeout=60
                     )
   if r.status_code == 200:
      logging.info("[success] file: \'{}\' uploaded to Lookup editor handler {} and saved in splunk app \'{}\'".format(lookup_file,r.url,splunk_app))
   else:
      logging.error("[failed] file: \'{}\', status:{}, reason:{}, url:{}".format(lookup_file,r.status_code,r.reason,r.url))
except Exception as e:
   logging.error("Error sending request to Splunk server: {}".format(e))
