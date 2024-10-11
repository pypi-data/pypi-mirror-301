#!/usr/bin/env python3
# Template Author: NhanDD <hp.duongducnhan@gmail.com>


from active_check.agent_{{cookiecutter.agent_id}} import run_active_check, LOG_FILE_PATH

HOST_IP = '127.0.0.1'
SNMP_COMMUNITY = 'public'
SAMPLE_DATA = {
    'name': '{{cookiecutter.author_name}}',
    'email': '{{cookiecutter.email}}'
}
OTHER_KWARGS = {}


if __name__ == '__main__':
    print('log file will be written to', LOG_FILE_PATH)
    run_active_check(SAMPLE_DATA, HOST_IP, SNMP_COMMUNITY, **OTHER_KWARGS)