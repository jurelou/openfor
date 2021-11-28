from openfor import settings
from splunklib import client as splunk_client
from loguru import logger
from pathlib import Path

def make_client():
    client = splunk_client.connect(
        host=settings.splunk.host,
        port=settings.splunk.port,
        scheme=settings.splunk.scheme,
        username=settings.splunk.username,
        password=settings.splunk.password,
        verify=False,
        autoLogin=True
    )
    logger.info(f"Successfully connected to splunk {settings.splunk.host}")
    return client


def create_app(client, app_name: str):
    if app_name in client.apps:
        logger.info(f"Splunk App {app_name} already exists")
        return
    client.apps.create(name=app_name, author="ljk", description="openfor app", label="TA-openfor", visible=0, check_for_updates=0)
    logger.info(f"Created splunk app {app_name}")

def create_index(client, index: str):
    if index in client.indexes:
        logger.info(f"Index {index} already exists")
        return
    client.indexes.create(name=index)
    logger.info(f"Created splunk index {index}")

def create_sourcetypes(client):
    props = client.confs.create(name='props')

    evtx_stype = "windowsevtx"
    config = {
        'ANNOTATE_PUNCT': 'false',
        'INDEXED_EXTRACTIONS': 'json',
        'KV_MODE': 'json',
        'SHOULD_LINEMERGE': 'false',
        'TIMESTAMP_FIELDS': 'System.TimeCreated.#attributes.SystemTime',
        'TIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%Q',
        'TRUNCATE': '0',
        'TZ': 'GMT',
        'category': 'openfor',
        'description': 'Evtx files.',
    }

    if evtx_stype in props:
        logger.info(f"Sourcetype 'windows:evtx' already exists")
        a = props[evtx_stype].update(**config)
        return

    props.create(name=evtx_stype, **config)

"""
def ingest_file(client, index, sourcetype, file_path):
    if file_path.stat().st_size == 0:
        logger.warning(f"Cannot ingest empty file {file_path}")
        return
    
    with client.indexes[index].attach(
        host="openfor",
        source=str(file_path),
        sourcetype=sourcetype,
    ) as stream:
        with file_path.open(mode='rb') as f:
            while chunk := f.read(8192):
                stream.write(chunk)

    logger.info(f'Successfully ingested file `{file_path}` into Splunk index `{index}`')
"""

def ingest_data(client, index, sourcetype, data):
    
    with client.indexes[index].attach(
        host="openfor",
        source="nope",
        sourcetype=sourcetype,
    ) as stream:
        stream.write(data.encode(encoding='UTF-8', errors='backslashreplace'))

    logger.info(f'Successfully ingested data into Splunk index `{index}`')

client = make_client()
create_app(client, "TA-openfor")
create_index(client, "monindex")
create_sourcetypes(client)

#ingest_file(client, index="monindex", sourcetype="winadows:evtx", file_path=Path("output/1638049203.2222497/DE_1102_security_log_cleared/evtx_dump/DE_1102_security_log_cleared.json"))

data = """
<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event"><Provider Name="Microsoft-Windows-Security-Auditing" Guid="{54849625-5478-4994-a5ba-3e3b0328c30d}"></Provider>
<EventID Qualifiers="">4663</EventID>
<Version>0</Version>
<Level>0</Level>
<Task>12801</Task>
<Opcode>0</Opcode>
<Keywords>0x8020000000000000</Keywords>
<EventRecordID>452922</EventRecordID>
<Correlation ActivityID="" RelatedActivityID=""></Correlation>
<Execution ProcessID="4" ThreadID="60"></Execution>
<Channel>Security</Channel>
<Computer>PC01.example.corp</Computer>
<Security UserID=""></Security>
<SubjectUserSid>S-1-5-19</SubjectUserSid>
<SubjectUserName>LOCAL SERVICE</SubjectUserName>
<SubjectDomainName>NT AUTHORITY</SubjectDomainName>
<SubjectLogonId>0x00000000000003e5</SubjectLogonId>
<ObjectServer>Security</ObjectServer>
<ObjectType>Key</ObjectType>
<ObjectName>\REGISTRY\MACHINE\SYSTEM\ControlSet001\Control\Lsa</ObjectName>
<HandleId>0x00000420</HandleId>
<AccessList>%%4432</AccessList>
<AccessMask>0x00000001</AccessMask>
<ProcessId>0x000005a8</ProcessId>
<SystemTime>2019-03-19 23:35:15.365477</SystemTime>
<ProcessName>C:\Windows\System32\svchost.exe</ProcessName>
</Event>
"""
ingest_data(client, index="monindex", sourcetype="WinEventLog", data=data)
