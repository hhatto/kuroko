all:
	@echo "make clean"
	@echo "make pypireg"

PYTHON?=python

pypireg:
	${PYTHON} setup.py register
	${PYTHON} setup.py sdist upload

clean:
	rm -rf *.egg-info build dist kuroko/*.pyc
