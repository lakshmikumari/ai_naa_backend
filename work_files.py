# temporary files created before added in to DB
import os
from log import logger

scriptPath = os.path.dirname(os.path.realpath(__file__))

allData = lambda scriptPath, audit_id: scriptPath + \
                                       "/ParsedFiles" + audit_id + "/data/audit_table_data.json"
allExceptions = lambda scriptPath, audit_id: scriptPath + \
                                             "/ParsedFiles" + audit_id + "/data/exception_data.json"
netRulenetAdvice = lambda scriptPath, audit_id: scriptPath + \
                                                "/ParsedFiles" + audit_id + "/data/netRule_netAdvice.json"
severityBreakdown = lambda scriptPath, audit_id: scriptPath + \
                                                 "/ParsedFiles" + audit_id + "/data/severity_breakdown.json"
deviceDetails = lambda scriptPath, audit_id: scriptPath + \
                                             "/ParsedFiles" + audit_id + "/data/device_details.json"
allData_addremaining = lambda scriptPath, audit_id: scriptPath + \
                                                    "/ParsedFiles" + audit_id + "/data/audit_table_data_node.json"
allExceptions_addremaining = lambda scriptPath, audit_id: scriptPath + \
                                                          "/ParsedFiles" + audit_id + "/data/exceptions_data_node.json"
exceptionjson_addremaining = lambda scriptPath, audit_id: scriptPath + \
                                                          "/ParsedFiles" + audit_id + "/internal/allData_node.json"
exceptionjson = lambda scriptPath, audit_id: scriptPath + \
                                             "/ParsedFiles" + audit_id + "/internal/allData.json"
deviceidDetails = lambda scriptPath, audit_id: scriptPath + \
                                             "/ParsedFiles" + audit_id + "/internal/deviceId.json"


def createWorkDirs(audit_id):
    # os.chdir(scriptPath)
    try:
        logger.info("creating working dictionary")
        global exceptionsDir
        exceptionsDir = scriptPath + "/ParsedFiles" + audit_id + "/"
        if not os.path.exists(exceptionsDir):
            os.makedirs(exceptionsDir)

        global addRemainingDir
        addRemainingDir = exceptionsDir + "/Add_Remaining/"
        if not os.path.exists(addRemainingDir):
            os.makedirs(addRemainingDir)

        global dataDir
        dataDir = exceptionsDir + "/data/"
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)

        global internalDir
        internalDir = exceptionsDir + "/internal/"
        if not os.path.exists(internalDir):
            os.makedirs(internalDir)

        global auditSummaryDir
        auditSummaryDir = scriptPath + "/" + audit_id + "/Full/summary/"

        global deviceDir
        deviceDir = scriptPath + "/" + audit_id + "/"

        global tableToNMSMap
        tableToNMSMap = exceptionsDir + "/data/nms_map.json"

        global audit_insight
        audit_insight = dataDir + "/audit_insight.json"

    except Exception as e:
        logger.error("*** Error in work_files -- ".format(e))
