import os
import json
import work_files
from log import logger
from bs4 import BeautifulSoup

# script path
scriptPath = os.path.dirname(os.path.realpath(__file__))


def getAuditSummary(file_name, audit_info):
    """
    input: file_name= NAA_Processor/153875/Full/summary/Audit_Summary.html
    audit_id= 12345
    output: loaded json data to DB
    """
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            html_data = str(f.read().replace("0xc3", ""))
        soup = BeautifulSoup(html_data, features="html.parser")
        tables = soup.find_all("table")
        tableFlag = 0
        for table in tables:
            head = table.find_all("thead")
            for h in head:
                rows = h.findChildren('tr')
                tableName = [x.getText() for x in rows[0].findChildren('td')]
                if tableFlag == 0:
                    if len(tableName) == 1:
                        audit_info_json = {}
                        soup = BeautifulSoup("<table><thead></thead>" + str(table).split("</thead>")[1][:-8] +
                                             "</tbody></table>", features="html.parser")
                        for row in soup.select('tr'):
                            row_text = [x.text for x in row.find_all('td')]
                            audit_info_json[row_text[0]] = row_text[1]
                        audit_info_json['auditId'] = audit_info['auditId']
                        audit_info_json['crPartyId'] = audit_info['crPartyId']
                        audit_info_json['crPartyName'] = audit_info['crPartyName']
                        audit_info_json['location'] = audit_info['location']
                        tableFlag = 1
                        with open(work_files.audit_insight, "w") as f:
                            f.write(json.dumps(audit_info_json))
                        file_size = os.stat(work_files.audit_insight).st_size
                        logger.info("audit_insight.json created, size: {}".format(file_size / 1024))

    except Exception as e:
        logger.error(e)


# main function of audit information
def audit_information(audit_info):
    """input:  reads .html files from fileName=153875 + Full folder and sub folders
    Writes node name to model linking data like {"node name": "N9K-1", "Model": "cevChassisN9Kc9504"} to DB """
    try:
        os.chdir(scriptPath)
        parseDir = work_files.auditSummaryDir

        file_name = [item for item in os.listdir(parseDir)
                     if item == "Audit_Summary.html" or item == "Audit_Overview.html"]
        logger.info(file_name)
        getAuditSummary(parseDir + file_name[0], audit_info)

    except Exception as e:
        logger.error(e)
