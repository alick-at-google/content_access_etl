from datalab.context import Context
import datalab.storage as storage
import datalab.bigquery as bq
from google.cloud import bigquery

#/Users/alickzhang/desktop/mysdk/contentaccess-d2808270be30.json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '____PATH_TO_KEY_____'
# Construct a BigQuery client object.
client = bigquery.Client()

#make dataset
dataset_id = 'folder_access'
dataset = client.dataset(dataset_id)

table_ref = dataset.table("folder_access_df")
#upload to BQ 
load_job = client.load_table_from_dataframe(folder_access_df, table_ref)



#etljob


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/alickzhang/desktop/mysdk/contentaccess-d2808270be30.json'
# Construct a BigQuery client object.
client = bigquery.Client()

#specify the list of tables ("database")
dataset_id = 'content_access'
dataset = client.dataset("folder_access")


####specify dataframe info - change df to those that match your syntax. 
dfs = [folder_df, folder_access_df, content_df, user_df, group_df]
df_name = ["folder_df", "folder_access_df", "content_df", "user_df", "group_df"]

#loop through dfs and upload tables to dataset
for df, df_name in zip(dfs, df_name):
    print(df_name)
    table_ref = dataset.table(str(df_name))
    #upload to BQ 
    load_job = client.load_table_from_dataframe(df, table_ref)