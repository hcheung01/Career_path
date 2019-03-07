import os
import time
import requests
from googleapiclient.discovery import build
import json

client_service = build('jobs', 'v3')
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']
# [END instantiate]


# def run_sample():
#     print(client_service)
#     print(parent)


def basic_keyword_search(client_service, company_name, keyword):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'query': keyword}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'search_mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'job_query': job_query,
    }

    response = client_service.projects().jobs().search(
        parent=parent, body=request).execute()
    print(response)
    print(type(response))




if __name__ == '__main__':
    # run_sample()
    basic_keyword_search(client_service, "facebook", "engineer")
