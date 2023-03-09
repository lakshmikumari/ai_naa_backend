import os
import json
from log import logger
import work_files

# script path
scriptPath = os.path.dirname(os.path.realpath(__file__))


# function to write into a file
def writeData(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))


def exception_json(audit_info):
    """
    output: This function creates AllData.json and allexception.json inside /data folder
     input: by processing the .json files under json folder under  "/ExceptionTables" + audit_id + "/json/"
    """
    try:
        ExceptionData = []
        file_name = audit_info['fileName'].split('.')[0]
        with open(work_files.internalDir + "allData.json", "r") as f:
            allData_exception_json = json.loads(f.read())
        for jsonData in allData_exception_json:
            if jsonData["NMSArea"] != "" and len(jsonData["data"]) >= 1:
                for item in jsonData["data"]:
                    for i in item:
                        if list(i.keys())[0] != 'Host Name (IP Address)' and "NREPs" and "No data available.":
                            if list(i.values())[0]['Sev'] != "White":
                                exception_data = {'exception_name': list(i.keys())[0]}
                                exception_data.update(list(i.values())[0])
                                exception_line = {"crPartyId": jsonData['crPartyId'],
                                                  "cpyKey": jsonData['cpyKey'], "location": audit_info['location'],
                                                  "auditId": jsonData["auditId"],
                                                  "auditName": jsonData["auditName"],
                                                  "tableName": jsonData["tableName"],
                                                  "NMSArea": jsonData["NMSArea"], 'Exception': exception_data,
                                                  "report": True,
                                                  "NCE Comments": ""}
                                ExceptionData.append(exception_line)

        # generate all_exception json file
        writeData(work_files.allExceptions(scriptPath, file_name), ExceptionData)
        file_size = os.stat(work_files.allExceptions(scriptPath, file_name)).st_size
        logger.info("exception_data.json created, size: {}".format(file_size / 1024))
        if os.path.isfile(work_files.internalDir + "allData_node.json"):
            ExceptionData_addremaining = []
            with open(work_files.internalDir + "allData_node.json", "r") as f:
                allData_exception_json = json.loads(f.read())
            for jsonData in allData_exception_json:
                if jsonData["NMSArea"] != "" and len(jsonData["data"]) >= 1:
                    for item in jsonData["data"]:
                        for i in item:
                            if list(i.keys())[0] != 'Host Name (IP Address)' and "NREPs" and "No data available.":
                                if list(i.values())[0]['Sev'] != "White":
                                    exception_data_addremaining = {'exception_name': list(i.keys())[0]}
                                    exception_data_addremaining.update(list(i.values())[0])
                                    exception_line_addremaining = {"crPartyId": jsonData['crPartyId'],
                                                                   "cpyKey": jsonData['cpyKey'],
                                                                   "location": audit_info['location'],
                                                                   "auditId": jsonData["auditId"],
                                                                   "auditName": jsonData["auditName"],
                                                                   "tableName": jsonData["tableName"],
                                                                   "NMSArea": jsonData["NMSArea"],
                                                                   'Exception': exception_data_addremaining,
                                                                   "report": True,
                                                                   "NCE Comments": ""}
                                    ExceptionData_addremaining.append(exception_line_addremaining)

            # generate all_exception json file
            writeData(work_files.allExceptions_addremaining(scriptPath, file_name), ExceptionData_addremaining)
            file_size = os.stat(work_files.allExceptions_addremaining(scriptPath, file_name)).st_size
            logger.info("exception_data_node.json created, size: {}".format(file_size / 1024))
    except Exception as e:
        logger.error(e)
