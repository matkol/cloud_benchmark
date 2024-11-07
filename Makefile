#!/usr/bin/make -f

.PHONY: python-environment clean data clean-docker clear test lint

virtual_env_name := cstr

clean:
	rm -rf static
	find . -path '*/__pycache__/*' -delete
	find . -type d -iname '__pycache__' -delete
	find . -type f -iname '*.pyc' -delete

clean-docker:
	bash scripts/clean_docker_images.sh

data:
	bash scripts/create_test_data.sh

lint:
	flake8 .
	black . --check

format:
	autoflake . -r --in-place --remove-all-unused-imports --exclude migrations,venv/
	black . --exclude venv/
	isort .

python-environment:
	bash scripts/setup_virtual_env.sh
	pip install pip-tools

python-environment-docker:
	docker build -t .

wipe-python-environment:
	bash scripts/clean_virtual_env.sh


environment:python-environment:
	pip install -r requirements.txt
	python3 setup.py develop

test:environment
	pytest tests
