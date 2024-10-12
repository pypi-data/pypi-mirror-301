import MrLou_AudioCodes
import base64

from MrLou_AudioCodes.acsbc_api import get_ini


fqdns = {
    "EO": "eosbc.qbe.com",
    "AOAP": "ausbcphy.qbe.com",
    "NA": "nasbc.qbe.com",
    "EOTEST": "eosbc.qbetest.com",
}

#SBC_INI_FILES = r"D:\UnifiedComm\scripts\DDImanager\build\01.sbc_backup_ini"
SBC_INI_FILES = r"C:\local\ini"

Username = "GL-USAP-UCAutomation"
Password = "spu4ez!1aFayLsobe3o6oc2_u"


def create_auth(username: str, password: str) -> str:
    # Concatenate username and password with a colon
    credentials_auth = f"{username}:{password}"

    # Encode the credentials in Base64
    encoded_credentials = base64.b64encode(credentials_auth.encode('utf-8')).decode('utf-8')

    # Return only the Base64 encoded string without the "Basic " prefix
    return encoded_credentials

auth_header = create_auth(username=Username, password=Password)


for region, fqdn in fqdns.items():
    get_ini(
        fqdn=fqdn,
        auth=auth_header,
        ini_name=fqdn.replace('.', '_'),
        ini_file_path=SBC_INI_FILES
    )
