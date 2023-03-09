import os
import re
import work_files
import json
from log import logger
from bs4 import BeautifulSoup

# script path
scriptPath = os.path.dirname(os.path.realpath(__file__))


# function to write to a file
def writeData(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))


def tableToNMSMapping(file_name, table_to_NMS_Mapping_json):
    """
    file ends with Detailed_Findings will be return the dict
    as example file_name=NAA_Processor/153875/Full/summary/Nexus_Platform_Audit_Detailed_Findings.html'
    returns dict type defaultJson
    """

    flag = 0
    with open(file_name, "r") as f:
        html_data = f.read()
    soup = BeautifulSoup(html_data, features="html.parser")
    anchors = soup.find_all("a")
    for anchor in anchors:
        if ("System Analysis" in anchor.text.strip() or "Media Analysis" in anchor.text.strip()
                or "Protocol Analysis" in anchor.text.strip()):
            html_data = html_data.replace("<b>Fault Management</b>",
                                          "<b><a NAME=Fault Management>Fault Management</a></b>")
            html_data = html_data.replace("<b>Capacity Management</b>",
                                          "<b><a NAME=Capacity Management>Capacity Management</a></b>")
            html_data = html_data.replace("<b>Configuration Management</b>",
                                          "<b><a NAME=Configuration Management>Configuration Management</a></b>")
            html_data = html_data.replace("<b>Performance Management</b>",
                                          "<b><a NAME=Performance Management>Performance Management</a></b>")
            html_data = html_data.replace("<b>Security Management</b>",
                                          "<b><a NAME=Security Management>Security Management</a></b>")
            break
    soup = BeautifulSoup(html_data, features="html.parser")
    anchors = soup.find_all("a")
    for anchor in anchors:
        name1 = anchor.text.strip()
        name = re.sub(' +', ' ', name1)
        if name != "":
            if "Management" in name and "Table" not in name:
                key = name
                flag = 1
            else:
                if flag == 1 and key in table_to_NMS_Mapping_json.keys():

                    table_to_NMS_Mapping_json[key].append(name)
                elif flag == 1:
                    # data[file_name] = [name]
                    table_to_NMS_Mapping_json[key] = [name]

    return table_to_NMS_Mapping_json


# main function for nmsMapping
def table_to_nms_mapping(audit_info):
    """
    file ends with Detailed_Findings will be return the dict
    as example file_name=NAA_Processor/153875/Full/summary/Nexus_Platform_Audit_Detailed_Findings.html'
    and loading the data in DB
    """
    try:
        nmsmapping = {}
        parseDir = work_files.auditSummaryDir
        for item in os.listdir(parseDir):
            if ((item.endswith(".html") and "NodeAndSummary_" in item)
                    or "Detailed_Findings.html" in item):
                if "Detailed_Findings" in item:
                    audit_name = item.split('_Detailed_Findings')[0]
                elif "NodeAndSummary_" in item:
                    audit_name = (item.split('NodeAndSummary_')[1]).split('.')[0]

                defaultJson = {"Performance Management": [], "Capacity Management": [], "Fault Management": [],
                               "Configuration Management": [], "Security Management": []}
                tableToNMSMap = tableToNMSMapping(work_files.auditSummaryDir + item,
                                                  defaultJson)
                nmsmapping[audit_name] = tableToNMSMap
        nmsmapping['auditId'] = audit_info['auditId']
        nmsmapping['crPartyId'] = audit_info['crPartyId']
        nmsmapping['crPartyName'] = audit_info['crPartyName']
        nmsmapping['location'] = audit_info['location']
        writeData(work_files.tableToNMSMap, nmsmapping)
        file_size = os.stat(work_files.tableToNMSMap).st_size
        logger.info("nmsmapping json created, size: {} KB".format(round(file_size/1024,2)))
    except Exception as e:
        logger.error(e)
