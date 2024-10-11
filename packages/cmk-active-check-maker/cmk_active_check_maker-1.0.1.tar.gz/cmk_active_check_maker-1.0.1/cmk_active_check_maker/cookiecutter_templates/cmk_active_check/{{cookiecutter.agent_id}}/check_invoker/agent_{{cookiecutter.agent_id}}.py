#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>

# -----------------------------
# Function get params in this case is port, passed via WATO agent rule cunfiguration, hostname and ip addres of host, 
# for which agent will be invoked 
#
import json


def check_arguments(params):
    args = ''
    data = json.dumps(params)
    args = [
        '--data', data, 
        '--ip', '$HOSTADDRESS$',            # device ip address
        '--community', '$_HOSTSNMPCOMMUNITY$'        # community string, configured in host configuration
    ]
    return args


def check_description(params):
    return f"{{cookiecutter.agent_id}}: Hello, I'm agent {{cookiecutter.agent_id}}"         # text displayed in service section in monitor page

# -----------------------------
# register invoke function for our agent
# key value for this dictionary is name part from register datasource of our agent (name="special_agents:myspecial" remember?)
#
try:
    active_check_info['{{cookiecutter.agent_id}}'] = {
        "command_line": "agent_{{cookiecutter.agent_id}}.py $ARG1$",
        "argument_function": check_arguments,
        "service_description": check_description,
        "has_perfdata": True,
    }
except Exception as e:
    import traceback
    print(traceback.print_exc())
