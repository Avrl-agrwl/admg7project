#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import boto3
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import requests
import csv
import sys
import botocore
import uuid
from collections import defaultdict
import random
import numpy as np
import streamlit as st
from packaging import version
from botocore.exceptions import ClientError
from pathlib import Path

# Setup Clients
#st.beta_set_page_config(layout="wide")

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')
personalize_events = boto3.client('personalize-events')
usr='12344'
auth=pd.read_csv('c_auth.csv')
prod = pd.read_csv('products.csv')
st.image('img/logo.png')
em=st.text_input("enter email ID: ")
if not em:
    st.write("Enter your email ID")
else:
    if em in list(auth["email"]):
        try:
            st.title("Welcome back!")
            id=auth[auth.email==em]['user_Id'].apply(lambda x: str(x))
            usr =id.iloc[0]
            response=personalize_runtime.get_recommendations(
                campaignArn='arn:aws:personalize:us-east-1:333474833395:campaign/userproductrecommendation',
                userId=usr,
                filterArn= "arn:aws:personalize:us-east-1:333474833395:filter/purchase-filter"
            )
            t=response["itemList"]
            st.write("---------------------------------------------")
            st.write("Based on your recent purchases, products you might like:")
           
        except:
            st.write("email error")
    else:
        try:
            n=st.text_input("Name:")
            st.title("Welcome")
            response=personalize_runtime.get_recommendations(
                campaignArn='arn:aws:personalize:us-east-1:333474833395:campaign/userproductrecommendation',
                userId=usr,
                filterArn= "arn:aws:personalize:us-east-1:333474833395:filter/purchase-filter"
            )
            t=response["itemList"]
        
            st.title("products recommended:")
        except:
            st.write("cold start error")
    
    try:
        col= st.beta_columns([1,1,1,1])
        for i in range(0,4):
            with col[i]:
                item=prod[prod.item_id==t[i]["itemId"]]["item_name"].iloc[0]
                pic=prod[prod.item_id==t[i]["itemId"]]["image"].iloc[0]
                st.write(item)
                pic='img/'+pic
                st.image(pic)
    except:
        st.write("error")
        
    st.write("---------------------------------------------")
    ########################

    st.write("Search Products:")
    try:
        product= st.selectbox('Choose a Product:', prod['item_name'])

        prod_id = prod[prod.item_name==product]["item_id"].iloc[0]



        response=personalize_runtime.get_recommendations(
            campaignArn='arn:aws:personalize:us-east-1:333474833395:campaign/item-similarity',
            itemId=prod_id,
            userId=usr,
            filterArn= "arn:aws:personalize:us-east-1:333474833395:filter/similarityfilter"
        )
        t=response["itemList"]
        col= st.beta_columns([1,1,1,1])
        for i in range(0,4):
            with col[i]:
                item =prod[prod.item_id==t[i]["itemId"]]["item_name"].iloc[0]
                pic=prod[prod.item_id==t[i]["itemId"]]["image"].iloc[0]
                st.write(item)
                pic='img/'+pic
                st.image(pic)
    except:
        pass
    
    st.text_input("to Subscribe to our newsletter, enter your email")

