# openfor

Small toolkit for analyzing raw artifacts
Supported modules:
- zircolite
- evtx_dump

# Installation

- [OPTIONAL] Create a python virtual environment:

```
python3.8 -m venv env
source env/bin/activate
```

- Installation of dependencies:

```
python setup.py install
```


# Analyze event logs

Launch a module on a folder containing raw artifacts (.evtx)
This folder will be searched recursively

```
openfor_cli -f <INPUT_FOLDER> -e <MODULE>
```

`INPUT_FOLDER` is your folder containing raw files. (it may 
contains subfolders)

`MODULE` is one of:
- zircolite
- evtx_dump

You may supply multiple  `-e <MODULE>` arguments

By default, files will be stored in `./output`.
You may change the output folder by providing `-o <OUTPUT_FOLDER>`

# Extract an archive from DFIR-ORC

You may need to extract files from ORC archives.

```
./unzip_orcs.sh <INPUT_FOLDER> <OUTPUT_FOLDER>
```


# Configure a splunk forwarder

For example, to connect to the receiving indexer with the hostname idx.mycompany.com and that host listens on port 9997 for forwarders, type in:

sudo ./bin/splunk add forward-server localhost:9997 -auth ufadmin:rootroot

sudo ./bin/splunk list forward-server

Add to you etc/system/local/inputs.conf

[monitor://C:\tmp\*]
disabled=false
index=myindex
sourcetype=preprocess-winevet
crcSalt = <SOURCE>

