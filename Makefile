.PHONY: \
	all install run

all: .make-install

install: .make-install

.make-install-pipenv:
	@if ! which pipenv &> /dev/null; then \
		pip3 install pipenv==2021.5.29; \
	fi
	@touch $@

.make-install: Pipfile .make-install-pipenv
	pipenv install -d
	@touch $@

run: .make-install
	uvicorn src.skill_vk_trainee.application:app --reload

flake:
	flake8 src/skill_vk_trainee
	flake8 src/tests

mypy:
	mypy src/skill_vk_trainee

isort:
	isort setup.py
	isort src/skill_vk_trainee
	isort src/tests

test:
	pytest -q src/tests
