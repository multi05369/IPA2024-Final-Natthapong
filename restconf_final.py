import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_url = "https://10.0.15.61/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070101"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback66070101",
        "type": "iana-if-type:softwareLoopback",
        "description": "Created by 66070101",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.1.1.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070101 is created successfully" if resp.status_code == 201 else "Cannot create: Interface loopback 66070101"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def delete():
    resp = requests.delete(
        api_url,
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070101 is deleted successfully"
    elif (resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "Cannot delete: Interface loopback 66070101"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def enable():
    # 1) Read current admin state
    state_resp = requests.get(
        api_url,
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if state_resp.status_code == 404:
        print("STATUS NOT FOUND: 404")
        return "Cannot enable: Interface loopback 66070101 not found"

    if 200 <= state_resp.status_code <= 299:
        data = {}
        try:
            data = state_resp.json().get("ietf-interfaces:interface", {})
        except Exception:
            pass
        currently_enabled = bool(data.get("enabled", False))

        # 2) If already enabled, report it
        if currently_enabled:
            return "Cannot enable: Interface loopback 66070101"

        # 3) Otherwise, patch to enable
        yangConfig = {
            "ietf-interfaces:interface": {
                "enabled": True
            }
        }
        resp = requests.patch(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False
        )

        if 200 <= resp.status_code <= 299:
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070101 is enabled successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            try:
                print(resp.text)
            except Exception:
                pass
            return "Cannot enable: Interface loopback 66070101"
    else:
        print('Error. Status Code (GET): {}'.format(state_resp.status_code))
        try:
            print(state_resp.text)
        except Exception:
            pass
        return "Cannot enable: failed to read current state"


def disable():
    # 1) Read current admin state
    state_resp = requests.get(
        api_url,
        auth=basicauth,
        headers=headers,
        verify=False
    )

    if state_resp.status_code == 404:
        # Interface not found; choose the message you prefer
        print("STATUS NOT FOUND: 404")
        return "Cannot disable: Interface loopback 66070101 not found"

    if 200 <= state_resp.status_code <= 299:
        data = {}
        try:
            data = state_resp.json().get("ietf-interfaces:interface", {})
        except Exception:
            pass
        currently_enabled = bool(data.get("enabled", False))

        # 2) If already disabled, report it
        if not currently_enabled:
            return "Cannot shutdown: Interface loopback 66070101"

        # 3) Otherwise, patch to disable
        yangConfig = {
            "ietf-interfaces:interface": {
                "enabled": False
            }
        }
        resp = requests.patch(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False
        )

        if 200 <= resp.status_code <= 299:
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070101 is shutdowned successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            try:
                print(resp.text)
            except Exception:
                pass
            return "Cannot shutdown: Interface loopback 66070101"
    else:
        print('Error. Status Code (GET): {}'.format(state_resp.status_code))
        try:
            print(state_resp.text)
        except Exception:
            pass
        return "Cannot disable: failed to read current state"


# def status():
#     api_url_status = "<!!!REPLACEME with URL of RESTCONF Operational API!!!>"

#     resp = requests.<!!!REPLACEME with the proper HTTP Method!!!>(
#         <!!!REPLACEME with URL!!!>, 
#         auth=basicauth, 
#         headers=<!!!REPLACEME with HTTP Header!!!>, 
#         verify=False
#         )

#     if(resp.status_code >= 200 and resp.status_code <= 299):
#         print("STATUS OK: {}".format(resp.status_code))
#         response_json = resp.json()
#         admin_status = <!!!REPLACEME!!!>
#         oper_status = <!!!REPLACEME!!!>
#         if admin_status == 'up' and oper_status == 'up':
#             return "<!!!REPLACEME with proper message!!!>"
#         elif admin_status == 'down' and oper_status == 'down':
#             return "<!!!REPLACEME with proper message!!!>"
#     elif(resp.status_code == 404):
#         print("STATUS NOT FOUND: {}".format(resp.status_code))
#         return "<!!!REPLACEME with proper message!!!>"
#     else:
#         print('Error. Status Code: {}'.format(resp.status_code))
