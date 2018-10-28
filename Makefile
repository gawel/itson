venv:
	python3 -m venv venv
	./venv/bin/pip install -e .

serve: venv
	./venv/bin/itson
