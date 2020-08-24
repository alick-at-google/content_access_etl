# Content Access 
## The content access repo is used to grab data necessary to help answer questions regarding content access for users on an instance

code for ETL job which leverages [Looker Python SDK](https://pypi.org/project/looker-sdk/), [Pandas](https://pandas.pydata.org/) to grab and format data which ETL's directly to Big Query by leveraging [BigQuery API](https://cloud.google.com/bigquery/docs/reference/rest) 

The 2 code files are used to Leverage Looker's Python SDK and enable users to find and manage content access at both a group/user level

`content_access.py` is Looker Python SDK-specific code used to generate tables necessary to obtain data. 
Tables are broken into:

- folder
- folder_access
- content
- content
- user
- group


![alt text](https://github.com/alickzhang97/content_access_etl/blob/master/content_access_ERD.png)


`etl_to_bq.py` leverages the BigQuery API and automates ETL process by directly uploading/updating tables based off ETL job. This file can be hosted on a server to automate and run based off cron

ETL job should be done into BigQuery database and we should be able to use the predefined block listed [here](https://github.com/alickzhang97/content_access_lookml) to generate prebuilt dashboards/content
