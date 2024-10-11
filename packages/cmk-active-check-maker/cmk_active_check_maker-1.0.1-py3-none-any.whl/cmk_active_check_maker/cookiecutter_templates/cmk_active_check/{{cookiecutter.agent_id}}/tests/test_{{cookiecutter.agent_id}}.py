#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>

import os
import json
from active_check.agent_{{cookiecutter.agent_id}} import run_active_check

# I just want to test the active check function, 
# so I will use the sample data to test the function
# but please modify the test case to match 
# your active check function and the sample data


TEST_HOST_IP = '127.0.0.1'
TEST_SNMP_COMMUNITY = 'public'


def load_sample_data() -> dict:
    sample_data_file_path = os.path.join(os.getcwd(), 'sample_data.json')
    with open(sample_data_file_path, 'r') as f:
        sample_data = json.load(f)  
    if not sample_data:
        raise Exception('Sample data is empty')
    # example of sample_data
    # sample_data ={
    #     "OK": [],         # list of data for OK status
    #     "WARNING": [],    # list of data for WARNING status
    #     "CRITICAL": [],   # list of data for CRITICAL status
    #     "UNKNOWN": []     # list of data for UNKNOWN status
    # }
    return sample_data


def test_ok_status():
    sample_data = load_sample_data()
    for data in sample_data.get('OK', []):
        status, msg = run_active_check(data, TEST_HOST_IP, TEST_SNMP_COMMUNITY)
        assert status == 'OK', f'{msg}'

def test_warning_status():
    sample_data = load_sample_data()
    for data in sample_data.get('WARNING', []):
        status, msg = run_active_check(data, TEST_HOST_IP, TEST_SNMP_COMMUNITY)
        assert status == 'WARNING', f'{msg}'
        
def test_critical_status():
    sample_data = load_sample_data()
    for data in sample_data.get('CRITICAL', []):
        status, msg = run_active_check(data, TEST_HOST_IP, TEST_SNMP_COMMUNITY)
        assert status == 'CRITICAL', f'{msg}'
        
def test_unknown_status():
    sample_data = load_sample_data()
    for data in sample_data.get('UNKNOWN', []):
        status, msg = run_active_check(data, TEST_HOST_IP, TEST_SNMP_COMMUNITY)
        assert status == 'UNKNOWN', f'{msg}'