venv:
	python3.8 -m venv env

install:
	sudo dpkg -i ./deps/deb/*
	./env/bin/activate
	pip install ./deps/pip/*
