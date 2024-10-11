# Template Author: NhanDD <hp.duongducnhan@gmail.com>


SITE={{cookiecutter.cmk_dev_site}}
SITE_PATH=/omd/sites/${SITE}

AGENT_PATH=/usr/lib/check_mk_agent/plugins/
PLUGIN_PATH=${SITE_PATH}/local/lib/check_mk/base/plugins/agent_based
WATO_PATH=${SITE_PATH}/local/share/check_mk/web/plugins/wato
AGENT_SPECIAL_PATH=${SITE_PATH}/local/share/check_mk/agents/special
CHECKS_PATH=${SITE_PATH}/local/share/check_mk/checks
LIB_PATH=${SITE_PATH}/local/lib/nagios/plugins

CMK_RUN_HOST={{cookiecutter.cmk_dev_hostname}}


# run in OMD[site]
dev-check-agent:
	cmk -d ${CMK_RUN_HOST}

# run in OMD[site]
dev-debug-agent:
	cmk --debug --checks={{cookiecutter.agent_id}} -vvn ${CMK_RUN_HOST}

# run in OMD[site]
dev-detect-plugins:
	cmk --detect-plugins={{cookiecutter.agent_id}} -vI ${CMK_RUN_HOST}


PROJECT_DIR={{cookiecutter.agent_id}}
AGENT_ID={{cookiecutter.agent_id}}

# run in plugin directory (where Makefile is)
dev-deploy-plugin:
#	agent
	sudo cp ./active_check/agent_${AGENT_ID}.py ${LIB_PATH}/agent_${AGENT_ID}.py
	sudo chmod +x ${LIB_PATH}/agent_${AGENT_ID}.py
#	agent invoker
	sudo cp ./check_invoker/agent_${AGENT_ID}.py ${CHECKS_PATH}/agent_${AGENT_ID}.py
	sudo chmod +x ${CHECKS_PATH}/agent_${AGENT_ID}.py
#	wato
	sudo cp ./wato/${AGENT_ID}_register.py ${WATO_PATH}/${AGENT_ID}_register.py

#   after copy done, MUST restart OMD, 
	sudo omd restart ${SITE}


dev-undeploy-plugin:
	sudo rm -f ${AGENT_SPECIAL_PATH}/agent_${AGENT_ID}.py
	sudo rm -f ${CHECKS_PATH}/agent_${AGENT_ID}.py
	sudo rm -f ${WATO_PATH}/${AGENT_ID}_register.py

	sudo omd restart ${SITE}


# create MKP, run in OMD[site]
# mkp config file should be at var/check_mk/packages (in OMD[site])
dev-create-mkp:
	cp ./${PROJECT_DIR}/info ~/var/check_mk/packages/{{cookiecutter.agent_id}}


dev-pack-kmp: 
	mkp package {{cookiecutter.agent_id}}
	ll | grep {{cookiecutter.agent_id}}

dev-mkp-remove:
	mkp list | grep {{cookiecutter.agent_id}}
	mkp disable {{cookiecutter.agent_id}} {{cookiecutter.mkp_version}}
	mkp remove {{cookiecutter.agent_id}} {{cookiecutter.mkp_version}}


dev-install:
	poetry install && poetry shell 

dev-run-test:
	poetry run pytest

dev-run-check:
	poetry run python run_check.py


