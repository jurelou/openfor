TMP_RELEASE_FOLDER=/tmp/release-openfor

venv:
	python3.8 -m venv env
	env/bin/python setup.py install

install:
	sudo dpkg -i ./deps/deb/*
	./env/bin/activate
	pip install ./deps/pip/*

release:
	rm -rf ${TMP_RELEASE_FOLDER}
	mkdir ${TMP_RELEASE_FOLDER}
	cp -pr . ${TMP_RELEASE_FOLDER}
	rm -rf ${TMP_RELEASE_FOLDER}/.git \
		${TMP_RELEASE_FOLDER}/env \
		${TMP_RELEASE_FOLDER}/build \
		${TMP_RELEASE_FOLDER}/output \
		${TMP_RELEASE_FOLDER}/openfor.egg-info \
		${TMP_RELEASE_FOLDER}/dist \
		${TMP_RELEASE_FOLDER}/MP_RELEASE_FOLDER
		find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

	7z a -t7z -m0=lzma -mx=9 release.7z ${TMP_RELEASE_FOLDER}
