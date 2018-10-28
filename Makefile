APP:=$(shell basename `pwd`)
HOSTNAME:=$(shell hostname)
HOST:=amandine

venv:
	python3 -m venv venv
	./venv/bin/pip install -e .

serve: venv
	./venv/bin/$(APP)

sync:
	scp amandine:~/.$(APP).json ~/.$(APP).json

upgrade:
ifeq ($(HOSTNAME), $(HOST))
	git pull origin master
	~/apps/bin/circusctl restart $(APP)
else
	git push origin master
	ssh $(HOST) "cd ~/apps/$(APP) && make upgrade"
endif

