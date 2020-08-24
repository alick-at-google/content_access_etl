import looker_sdk
import json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings; warnings.simplefilter('ignore')
import pprint
#display all rows for DF
pd.set_option("display.max_rows", None, "display.max_columns", None)
from looker_sdk import models

#initialize SDK --- specify path to ini file in parenthesis
sdk = looker_sdk.init31()


#############################Gets All Folders#############################
folder_id = []
folder_name = []
content_metadata_id = []
parent_id = []
parent_name = []
child_count = []
folders = {}

for i in sdk.all_folders():
    #append data without parents here
    if i.parent_id is None:
        folder_id.append(i.id)
        folder_name.append(i.name)
        content_metadata_id.append(i.content_metadata_id)
        parent_id.append(i.parent_id)
        parent_name.append("None")
        child_count.append(i.child_count)
    else:
        #find all folders and parents name
        resp = sdk.folder(i.parent_id)
        #add to list
        folder_id.append(i.id)
        folder_name.append(i.name)
        content_metadata_id.append(i.content_metadata_id)
        parent_id.append(i.parent_id)
        parent_name.append(resp.name)
        child_count.append(i.child_count)
        

folders["folder_id"] = folder_id
folders["folder_name"] = folder_name
folders["content_metadata_id"] = content_metadata_id
folders["parent_id"] = parent_id
folders["parent_name"] = parent_name
folders["child_count"] = child_count

folder_df = (pd.DataFrame(folders).astype({"folder_id": "object", 
                                           "parent_id": "object", 
                                           "content_metadata_id": "object", 
                                           "child_count": "int32"})
        .sort_values(by=["parent_id"]))


##############################GET CONTENT ON FOLDER############################
ids = []
names = []
folder_id = []
content_type = []

content_dict = {}

#######Get parent folder content########
for i in instance_folder["folder_id"]:
    print(i)
    #get dashboards in folder
    for dashboard in sdk.space_dashboards(space_id = str(i)):
        ids.append(dashboard.id)
        names.append(dashboard.title)
        content_type.append("dashboard")
        folder_id.append(i)

    #get looks in folder
    for look in sdk.space_looks(space_id = str(i)):
        ids.append(look.id)
        names.append(look.title)
        content_type.append("look")
        folder_id.append(i)

content_dict["folder_id"] = folder_id
content_dict["content_id"] = ids
content_dict["content_name"] = names
content_dict["content_type"] = content_type
content_df = pd.DataFrame(content_dict).astype({'content_id': 'int64'})
content_df



##############################GET CONTENT ACCESS###########################
user_ids=[]
group_ids = []
parent_ids = []
folders = []

folder_access = {}

#loop through each folder
for folder_id, content_metadata_id in zip(instance_folder["folder_id"], instance_folder["content_metadata_id"]):
    #log folder id
    folders.append(folder_id)
    #call function
    resps = sdk.all_content_metadata_accesses(content_metadata_id=str(content_metadata_id))
    #keep calling the function until we get a response
    while resps == []:
        #get the parent folder
        parent_id = sdk.folder_parent(str(folder_id))
        folder_id = parent_id.id
        #check access
        resps = sdk.all_content_metadata_accesses(content_metadata_id=str(parent_id.content_metadata_id))

    ##append to list
    user_id = []
    group_id = []
    for resp in resps:
        if not user_id or resp.user_id is not None:
            user_id.append(resp.user_id)

        if not group_id or resp.group_id is not None:
            group_id.append(resp.group_id)

    #appending into larger array
    user_ids.append(user_id)
    group_ids.append(group_id)
    parent_ids.append(parent_id)

############# CHECK TO REMOVE NONE IF ARRAY IS  NOT EMPTY for USERS ################
index = 0
for ids in user_ids:
    if len(ids) == 0:
        pass
    #pass if list is just an array of 1 None
    elif len(ids) == 1 and ids[0] is None:
        pass
    #if it's just a list of numbers pass
    elif len(ids) >= 1 and not None in ids:
        pass
    else:
        user_ids[index] = [i for i in ids if i]
    index+=1

    
############# CHECK TO REMOVE NONE IF ARRAY IS  NOT EMPTY for GROUPS ################
index = 0
for ids in group_ids:
    if len(ids) == 0:
        pass
    #pass if list is just an array of 1 None
    elif len(ids) == 1 and ids[0] is None:
        pass
    #if it's just a list of numbers pass
    elif len(ids) >= 1 and not None in ids:
        pass
    else:
        group_ids[index] = [i for i in ids if i]
    index+=1    
    

    
folder_access["folder_id"] = folders
folder_access["user_id"] = user_ids
folder_access["group_id"] = group_ids

#content access df
folder_access_df = pd.DataFrame(folder_access)


#############################USERS AND GROUP INFO######################################
########GET USER DF##########
user_id = []
email = []
first_name = []
last_name = []
role_id = []
group_id = []
personal_folder_id = []

user_dict = {}

for i in sdk.all_users():
    email.append(i.email)
    first_name.append(i.first_name)
    last_name.append(i.last_name)
    role_id.append(i.role_ids)
    group_id.append(i.group_ids)
    user_id.append(i.id)
    personal_folder_id.append(i.personal_folder_id)

user_dict["user_id"] = user_id
user_dict["email"] = email
user_dict["first_name"] = first_name
user_dict["last_name"] = last_name
user_dict["role_id"] = role_id
user_dict["group_id"] = group_id
user_dict["personal_folder_id"] = personal_folder_id

user_df = pd.DataFrame(user_dict)

#######GET GROUP DF###########
group_id = []
user_count = []
external_group_id = []
group_name = []

group_dict = {}

for i in sdk.all_groups():
    group_id.append(i.id)
    group_name.append(i.name)
    external_group_id.append(i.external_group_id)
    user_count.append(i.user_count)

group_dict["group_id"] = group_id
group_dict["name"] = group_name
group_dict["external_group_id"] = external_group_id
group_dict["user_count"] = user_count

group_df = pd.DataFrame(group_dict)
group_df


#