#!/usr/bin/python3
"""
Script to make API calls to Google cloud talent
"""
import os
from googleapiclient.discovery import build
from googleapiclient.errors import Error
import requests
import flask
import json

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']

def basic_keyword_search(client_service, company_name, keyword):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedUserId',
        'domain': 'www.google.com'
    }

    job_query = {'query': keyword}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'search_mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'job_query': job_query,
        'job_view': 'JOB_VIEW_FULL'
    }
    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
    print(response.get('metadata'))

if __name__ == "__main__":
   basic_keyword_search(client_service, "Apple", "software OR java")
