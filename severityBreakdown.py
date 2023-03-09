import os
import json
from log import logger

# script path
import work_files

scriptPath = os.path.dirname(os.path.realpath(__file__))


# function to write into a file
def writeData(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))


def severity_breakdown_json(audit_info):
    """
    this function give output of severities
    input: /json all files
    output: calculating the
    """
    try:
        file_name = audit_info['fileName'].split('.')[0]
        severities = {"auditId": audit_info['auditId'], "crPartyId": audit_info['crPartyId'],
                      "crPartyName": audit_info['crPartyName'], "location": audit_info['location'],
                      "Verify Manually": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Total": 0},
                      "Configuration Management": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Total": 0},
                      "Capacity Management": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Total": 0},
                      "Fault Management": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Total": 0},
                      "Performance Management": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Total": 0},
                      "Security Management": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0, "Total": 0},
                      "Total": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0}}
        folder_name = audit_info['fileName'].split('.')[0]
        verifyManually = {"unique": {}, "names": {}}
        configManagement = {"unique": {}, "names": {}}
        capacityManagement = {"unique": {}, "names": {}}
        faultManagement = {"unique": {}, "names": {}}
        performanceManagement = {"unique": {}, "names": {}}
        securityManagement = {"unique": {}, "names": {}}
        severity_count = {"Critical": {}, "High": {}, "Medium": {}, "Low": {}, "Informational": {}}
        NMS = {"Verify Manually": verifyManually, "Configuration Management": configManagement,
               "Capacity Management": capacityManagement, "Fault Management": faultManagement,
               "Performance Management": performanceManagement, "Security Management": securityManagement}
        with open(work_files.dataDir + "exception_data.json", "r") as f:
            allData_exception_json = json.loads(f.read())
            for jsonData in allData_exception_json:
                if (jsonData["Exception"]["exception_name"] + jsonData["Exception"]["Sev"] not in
                        NMS[jsonData["NMSArea"]]["unique"]):
                    severities[jsonData["NMSArea"]][jsonData["Exception"]["Sev"]] = severities[jsonData["NMSArea"]][
                                                                                        jsonData["Exception"][
                                                                                            "Sev"]] + 1

                    NMS[jsonData["NMSArea"]]["unique"][
                        jsonData["Exception"]["exception_name"] + jsonData["Exception"]["Sev"]] = 1

                if jsonData["Exception"]["exception_name"] not in NMS[jsonData["NMSArea"]]["names"]:
                    severities[jsonData["NMSArea"]]["Total"] = severities[jsonData["NMSArea"]]["Total"] + 1
                    NMS[jsonData["NMSArea"]]["names"][
                        jsonData["Exception"]["exception_name"]] = 1
                if jsonData["Exception"]["exception_name"] not in severity_count[jsonData["Exception"]["Sev"]]:
                    # severities["Total"][jsonData["Exception"]["Sev"]] = severities["Total"][
                    #                                                         jsonData["Exception"]["Sev"]] + 1
                    severity_count[jsonData['Exception']['Sev']][jsonData["Exception"]["exception_name"]] = 1
        logger.info(severity_count['Informational'])
        if os.path.isfile(work_files.dataDir + "exceptions_data_node.json"):
            with open(work_files.dataDir + "exceptions_data_node.json", "r") as f:
                allData_exception_json_addremaining = json.loads(f.read())
                for jsonData in allData_exception_json_addremaining:
                    if (jsonData["Exception"]["exception_name"] + jsonData["Exception"]["Sev"] not in
                            NMS[jsonData["NMSArea"]]["unique"]):
                        severities["Total"][jsonData["Exception"]["Sev"]] = severities["Total"][
                                                                                jsonData["Exception"]["Sev"]] + 1
                        severities[jsonData["NMSArea"]][jsonData["Exception"]["Sev"]] = severities[jsonData["NMSArea"]][
                                                                                            jsonData["Exception"][
                                                                                                "Sev"]] + 1

                        NMS[jsonData["NMSArea"]]["unique"][
                            jsonData["Exception"]["exception_name"] + jsonData["Exception"]["Sev"]] = 1

                    if jsonData["Exception"]["exception_name"] not in NMS[jsonData["NMSArea"]]["names"]:
                        severities[jsonData["NMSArea"]]["Total"] = severities[jsonData["NMSArea"]]["Total"] + 1
                        NMS[jsonData["NMSArea"]]["names"][
                            jsonData["Exception"]["exception_name"]] = 1
                    if jsonData["Exception"]["exception_name"] not in severity_count[jsonData["Exception"]["Sev"]]:
                        # severities["Total"][jsonData["Exception"]["Sev"]] = severities["Total"][
                        #                                                         jsonData["Exception"]["Sev"]] + 1
                        severity_count[jsonData['Exception']['Sev']][jsonData["Exception"]["exception_name"]] = 1
        severities['Total']['Critical'] = len(severity_count['Critical'])
        severities['Total']['Low'] = len(severity_count['Low'])
        severities['Total']['High'] = len(severity_count['High'])
        severities['Total']['Informational'] = len(severity_count['Informational'])
        severities['Total']['Medium'] = len(severity_count['Medium'])
        logger.info(severity_count['Informational'])
        writeData(work_files.severityBreakdown(scriptPath, file_name), severities)
        file_size = os.stat(work_files.severityBreakdown(scriptPath, file_name)).st_size
        logger.info("severity breakdown created, size: {}".format(file_size / 1024))

    except Exception as e:
        logger.error(e)
