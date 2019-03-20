#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import render_template, url_for, flash, redirect, request, Flask, jsonify, abort
from models import storage, CNC
from models.job import Job
from datetime import datetime

def add_item(job, key, skill_list):
    temp = job['description']
    job_list_skill = temp.replace(',', ' ').replace('(', ' ').replace(')', ' ').lower().split()
    list = skill_list.lower().split()
    sub_set = set(job_list_skill).intersection(set(list))
    print(sub_set)
    print(skill_list)
    m = round(len(sub_set) / len(list) * 100, 0)
    print("m is ", m)
    # setattr(job, key, "{0:.2f}%".format(m))
    job[key] = "{}%".format(int(m))
    return job

def relative_compare(user_info, job_req):
    """Function to compare 2 list, if matching greater than 30% return true"""
    user_list = [item.lower() for item in user_info.replace(',', '').replace(' USA', '').split(' ')]
    job_list = [item.lower() for item in job_req.replace(',', '').replace(' USA', '').split(' ')]
    sub_set = set(user_list).intersection(set(job_list))
    m = len(sub_set) / len(job_list)
    if m >= 0.2:
        return True
    return False

@app_views.route('/job_search_gereral', methods=['GET'])
def job_search_gereral():
    """
        job search route to handle http method for requested job query by profile
    """
    job_list = [job.to_json() for job in storage.all('Job_db').values()]
    sorted_job_list = sorted(job_list, key=lambda k: k['date_post'])
    return jsonify(sorted_job_list)

@app_views.route('/job_search_by_criteria/<position>/<location>', methods=['GET'])
def job_search_by_criteria(position=None, location=None):
    """
        job search route to handle http method for requested job query by profile
    """
    """put here request by profile property
    """

    job_list = [job.to_json() for job in storage.all('Job_db').values()]
    if location == 'None' and position == 'None':
        sorted_job_list = sorted(job_list, key=lambda k: k['date_post'])
    else:
        if location != 'None' and position != 'None':
            location = " ".join(location.split('_'))
            position  = " ".join(position.split('_'))
            filter_list = [job for job in job_list if (relative_compare(position, job['position']) and relative_compare(location, job['location']))]
        elif location == 'None':
            position  = " ".join(position.split('_'))
            filter_list = [job for job in job_list if (relative_compare(position, job['position']))]
        else:
            location = " ".join(location.split('_'))
            filter_list = [job for job in job_list if (relative_compare(location, job['location']))]
        sorted_job_list = sorted(filter_list, key=lambda k: k['date_post'])
    return jsonify(sorted_job_list)

@app_views.route('/job_search_by_profile/<profile_id>', methods=['GET'])
def job_search_by_profile(profile_id=None):
    """
        job search route to handle http method for requested job query by profile
    """
    profile_obj = storage.get('Profile', profile_id)
    if profile_obj is None:
        abort(404, 'Not found')
    job_list = [job.to_json() for job in storage.all('Job_db').values()]
    filter_list = [add_item(job, 'skill_match', profile_obj.skills) for job in job_list if (relative_compare(profile_obj.position, job['position'])  and relative_compare(profile_obj.location, job['location']))]
    sorted_job_list = sorted(filter_list, key=lambda k: k['date_post'])
    # print(sorted_job_list[0])
    return jsonify(sorted_job_list)
