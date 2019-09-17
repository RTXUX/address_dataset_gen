import base64
import hashlib
import requests
from dicttoxml import dicttoxml
gateway = "https://shidclink.cainiao.com/gateway/link.do"

def sign(request, resource_code):
    return base64.encodebytes(hashlib.md5(''.join((request,resource_code)).encode("utf-8")).digest()).decode('utf-8')

def build_request(msg_type, provider_id, payload, salt):
    payload = dicttoxml({"request": payload}, root=False, attr_type=False)
    payload = payload.decode("utf-8")
    digest = sign(payload, salt)
    digest = digest.rstrip('\n')
    data = {
        "msg_type": msg_type,
        "logistic_provider_id": provider_id,
        "logistics_interface": payload,
        "data_digest": digest
    }
    r = requests.post(gateway,data=data, headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
    return r

def guess(division, detail_address, limit=10, degrade=False):
    r = build_request(
        "CNDZK_GUESS_ADDRESS",
        "cndzk_guess_address_cpcode",
        {
            "divisionAddress": division,
            "detailAddress": detail_address,
            "isDegrade": 1 if degrade else 0,
            "limit": limit
        },
        "cndzk_guess_address"
    )
    return r.json()





