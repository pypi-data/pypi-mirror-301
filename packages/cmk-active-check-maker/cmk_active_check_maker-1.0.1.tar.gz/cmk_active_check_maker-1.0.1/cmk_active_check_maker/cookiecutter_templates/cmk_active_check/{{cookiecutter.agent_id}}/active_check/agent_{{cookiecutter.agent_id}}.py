#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>

# enable if you want to use libs
# require install extra libs: snmp, requests
# import netsnmp
# import re
# import ast
import json
import os
import requests
import sys
import logging
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# -----------------------------------------   
#   DO NOT MODIFY BELLOW CONSTANTS
#   you could add more constants if you need
# -----------------------------------------   
HOME_PATH = Path.home()
LOG_DIR_PATH = os.path.join(HOME_PATH, "logs")
LOG_FILE_PATH = os.path.join(LOG_DIR_PATH, "{{cookiecutter.agent_id}}.log")
#
DEBUG = "DEBUG"
OK = "OK"
WARN = "WARN"
WARNING = "WARNING"
CRITICAL = "CRITICAL"
ERROR = "ERROR"
UNKNOWN = "UNKNOWN"
# -----------------------------------------   


def setup_log(name: str):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------     
    if not os.path.isdir(LOG_DIR_PATH):
        os.makedirs(LOG_DIR_PATH)
    
    logger = logging.getLogger(name)
    
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(LOG_FILE_PATH, when='midnight', interval=1, backupCount=30)
    handler.setFormatter(logging.Formatter('%(message)s')) 
    logger.addHandler(handler)
    return logger

# create logger, DO NOT MODIFY
logger = setup_log("{{cookiecutter.agent_id}}-logger")


def terminate_check(status, msg):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    print(f"{status} - {msg}")
    if status == OK:
        sys.exit(0)
    elif status == WARNING:
        sys.exit(1)
    elif status == CRITICAL:
        sys.exit(2)
    else:
        sys.exit(3)


def log(msg, **kwargs):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    data = {
        'time': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
        'service_name': '{{cookiecutter.agent_id}}',
        'msg': msg,
        **kwargs
    }
    
    api_resp = kwargs.get('api_resp', None)
    if isinstance(api_resp, requests.Response):
        data.update({
            'api_request_url': api_resp.request.url,
            'api_request_method': api_resp.request.method,
            'api_request_headers': dict(api_resp.request.headers),
            'api_request_body': api_resp.request.body.decode('utf-8'),
            'api_status_code': api_resp.status_code,
            'api_response_text': api_resp.text
        })
    logger.info(json.dumps(data))
    
def create_directory(dir_path: str, mode: int = 0o777):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path, mode=mode)
        log(f"Create directory {dir_path}")
    else:
        log(f"Directory {dir_path} existed")
    
    
def make_request(url, method: str, headers: dict = {}, data:dict = {}, verify=False):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE']:
        log(f"Method {method} not supported")
        return terminate_check(UNKNOWN, f"request API method >>{method}<< not supported")
    try:
        response = requests.request(method, url, headers=headers, data=data, verify=verify)
        response.raise_for_status()
        
    except requests.exceptions.ConnectTimeout:
        log(f"Timeout when connect to {url}", api_resp=response)
        terminate_check(UNKNOWN, f"Timeout when connect to {url}")
    except requests.exceptions.ReadTimeout:
        log(f"Timeout when connect to {url}", api_resp=response)
        terminate_check(UNKNOWN, f"Timeout when read data from {url}")
    except Exception as e:
        log(f"Timeout when connect to {url}", api_resp=response)
        terminate_check(UNKNOWN, f"Error when request to {url} with error: {e}")

def run():
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    try:
        args = sys.argv[1:]
        while args:
            section = args.pop(0)
            if section == '--data':
                formatted_json = args.pop(0).replace("'", '"')
                data = json.loads(formatted_json)
            if section == '--ip':
                ip = str(args.pop(0))
            if section == '--community':
                community = str(args.pop(0))
    except Exception as e:
        terminate_check(UNKNOWN, f"Error when parse arguments with error: {e}")
    
    if not data:
        terminate_check(UNKNOWN, "Missing data argument")
    if not ip:
        terminate_check(UNKNOWN, "Missing ip argument")
    
    # run agent 
    try:
        run_active_check(data, ip, community)
    except Exception as e:
        terminate_check(UNKNOWN, f"Error when run active check with error: {e}")
    

# ----------------------------------------- 
#   Your code begin here, entry point is run_active_check function
#   You could define other function to support run_active_check function
#   DO NOT MODIFY ABOVE, If you need other id, create new plugin template!
# -----------------------------------------        
def run_active_check(data, host_ip, snmp_community, **kwargs):
    log(f"run check with data {data} for host {host_ip} with community {snmp_community} and kwargs {kwargs}")
    # your code here
    # .....
    # .....
    # here is my example, remove it and replace with your code 
    return example_get_os_info()
    
def example_get_os_info():
    # example cod
    import platform
    # Gather OS details
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    architecture = platform.architecture()
    node = platform.node()
    machine = platform.machine()
    processor = platform.processor()

    # show message then exit
    terminate_check(
        OK,    
        f"Operating System: {os_name}, Version: {os_version}, Release: {os_release}, Architecture: {architecture[0]}, Hostname: {node}, Machine: {machine}, Processor: {processor}"
    )


if __name__ == '__main__':
    # ----------------------------------------- 
    #   DO NOT MODIFY
    # -----------------------------------------    
    run()
    # -----------------------------------------
