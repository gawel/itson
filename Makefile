APP:=$(shell basename `pwd`)
HOSTNAME:=$(shell hostname)
HOST:=amandine
PYTHON?=$(HOME)/.venvs/py3/bin/python3

venv:
	 $(PYTHON) -m venv venv
	./venv/bin/pip install -e .

serve: venv
	./venv/bin/$(APP)

upgrade: venv
ifeq ($(HOSTNAME), $(HOST))
	git pull origin master
	~/apps/bin/circusctl restart $(APP)
else
	git push origin master
	ssh $(HOST) "cd ~/apps/$(APP) && make upgrade"

sync:
	scp $(HOST):~/.$(APP).json ~/.$(APP).json
endif

