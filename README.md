# splunk_rest_upload_lookups

splunk_rest_upload_lookups.py provides a mechanism to upload a Splunk lookup csv file to a Splunk head. The Splunk head can be
standalone or part of a search head cluster. The lookup will get replicated to the other head members in the case of a search head cluster.

The python script uses Splunk lookup-editor https://splunkbase.splunk.com/app/1724 rest endpoint to upload lookup so it is
a prerequisite that this app is installed on the Splunk head/cluster that you will upload the lookup file to.

## Usage
`splunk_rest_upload_lookups.py splunk_head_url lookup_file splunk_app`

Note: Splunk user name and password will be prompted for but NOT echoed

## Example

```shell
$ ./splunk_rest_upload_lookups.py https://myhead:9999 ~/mylookup.csv search
Splunk username: 
Splunk password:

2023-04-26T16:26:11.648Z splunk_rest_upload_lookups: INFO: [success] file: '/Users/burwell/ug_demo.csv' uploaded to Lookup editor handler https://myhead:9999/services/data/lookup_edit/lookup_contents and saved in splunk app 'search'

```

## References
The python script is based on work referenced in https://community.splunk.com/t5/Splunk-Search/Can-you-create-modify-a-lookup-file-via-REST-API/m-p/193671
from this repo https://github.com/mthcht/lookup-editor_scripts

