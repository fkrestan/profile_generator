init:
	pipenv install \
	&& pipenv install --dev

test:
	PYTHONPATH=..:$(PYTHONPATH) \
	py.test -vs --fulltrace tests/

build:
	python3 setup.py build

dist: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} \+
	find . -type f -name "*.pyc" -exec rm -rf {} \+

.PHONY: init test build dist clean
