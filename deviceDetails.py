import re
import os
import json
from db_credentials import prod_auth
import requests
import work_files
from log import logger

# script path
scriptPath = os.path.dirname(os.path.realpath(__file__))


# function to write into a file
def writeData(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))


def getDeviceId(audit_info):
    try:
        device_dict = {}
        authToken_response = requests.post(prod_auth)
        auth_token = authToken_response.json()['access_token']
        header = {'Authorization': 'Bearer ' + auth_token}
        response = requests.get("https://mimir-prod.cisco.com/api/mimir/np/device_details",
                                params={"cpyKey": audit_info['cpyKey']}, headers=header)
        data = response.json()
        for d in data['data']:
            device_dict[d['deviceName']] = d['deviceId']
        return device_dict
    except Exception as e:
        logger.error('Error in mimir API call... proceding with empty records')
        return {}


def device_to_chassis_mapping(audit_info):
    """input:  reads .html files from fileName=153875 + Full folder and sub folders
    Writes node name to model linking data like {"node name": "N9K-1", "Model": "cevChassisN9Kc9504"} to DB """
    try:
        device_data = getDeviceId(audit_info)
        device_details = {}
        os.chdir(scriptPath)
        file = audit_info['fileName']
        file_name = file.split('.')[0]

        nodeNames = []
        json_data = {"auditId": audit_info['auditId'], "crPartyId": audit_info['crPartyId'],
                     "location": audit_info['location'],
                     "crPartyName": audit_info['crPartyName'], "data": []}
        os.chdir(os.path.join(scriptPath, file_name, "Full"))
        for d in os.listdir("."):
            if os.path.isdir(d) and d != "summary" and d != "commonImages":
                for file in os.listdir(d):
                    if file.endswith(".html"):
                        with open(d + "/" + file, "r") as f:
                            fileData = str(f.read())
                            startInd = fileData.find("Node Name:")
                            endInd = fileData.find("</b>", startInd)
                            startInd2 = fileData.find("Model:")
                            endInd2 = fileData.find("</b>", startInd2)

                            nodeName = ((fileData[startInd:endInd]).split(":")[1]).lstrip()
                            n1 = nodeName
                            try:
                                if nodeName.find("\n"):
                                    nodeName = nodeName.split(',')[1].lstrip("' ")
                                nodeName = re.sub(r'[\\t]*', '', nodeName)
                            except Exception as e:  ###index out of range
                                nodeName = n1
                            model = ((fileData[startInd2:endInd2]).split(":")[1]).lstrip()
                            m1 = model
                            try:
                                if model.find("\n"):
                                    model = model.split(',')[1].lstrip("' ")
                                model = re.sub(r'[\\t]*', '', model)
                            except Exception as e:
                                model = m1
                            if device_data != {}:
                                if nodeName in device_data:
                                    device_id = device_data[nodeName]
                                else:
                                    device_id = ''
                            else:
                                device_id = ''
                            nodeNames.append({"node_name": nodeName, "model": model, "device_id": device_id})
                            device_details[nodeName] = {"model": model, "device_id": device_id}
        # removing duplicate directory from the list ( similar device_name and model name will be removed)
        nodeNames = [dict(t) for t in {tuple(d.items()) for d in nodeNames}]

        json_data['data'] = nodeNames

        writeData(work_files.deviceDetails(scriptPath, file_name), json_data)
        writeData(work_files.deviceidDetails(scriptPath, file_name), device_details)
        file_size = os.stat(work_files.deviceDetails(scriptPath, file_name)).st_size
        logger.info('device_details.json created, size:{} KB'.format(round(file_size/1024,2)))
        return 'Generated devicedetails.json'
    except Exception as e:
        logger.error(e)
        return None
