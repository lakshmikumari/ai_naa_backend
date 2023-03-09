import datetime
import shutil
import os
import psutil
import allException
import createjson
import deviceDetails
import nmsMapping
import allData
import severityBreakdown
import netRulenetAdvice
import addRemaining
import work_files
import auditInsight
import DB
from pathlib import Path
import zipfile
from log import logger
from s3Handler import S3Handler
from email.message import EmailMessage
import smtplib

# script path file details

scriptPath = os.path.dirname(os.path.realpath(__file__))


# function to extract zipfile
def extractZip(fileName):
    data_path = Path(scriptPath)
    zip_path = data_path.joinpath(fileName)
    extract_path = data_path
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            logger.info('Extracting all the files now...')
            zip_ref.extractall(extract_path)
    except Exception as e:
        logger.error('Error while extracting the file --'.format(e))


def sendMail(userId, auditId, crPartyName, fileName, status, message):
    try:
        supportEmail = 'bgl-cx-bcs-audit@cisco.com'
        msg = EmailMessage()
        msg['Subject'] = f"Audit Insights : status of audit id {auditId}!!"
        msg['From'] = 'DONOTREPLY_AuditInsights@cisco.com'
        msg['To'] = f'{userId}@cisco.com'
        server = smtplib.SMTP("outbound.cisco.com")
        if status == 'Completed':
            msg.set_content(f'Hello {userId},\n\n' +
                            f'Processing of audit {auditId} is completed in audit insight tool.\n\n' +
                            'Details are:\n' +
                            f'Company Name: {crPartyName}\n' +
                            f'File Name: {fileName}\n\n' +
                            'Thank you,\n' +
                            'Team Audit Insights')
        if status == 'Error':
            msg.set_content(f'Hello {userId},\n\n' +
                            f'Processing of audit {auditId} is Halted due to an error.\n\n' +
                            'Details are:\n' +
                            f'Company Name: {crPartyName}\n' +
                            f'File Name: {fileName}\n' +
                            f'Message: {message}\n\n' +
                            'Thank you,\n' +
                            'Team Audit Insights')
        server.send_message(msg)
        logger.info("Mail sent to user about the audit status")
    except Exception as e:
        logger.error("Error while sending mail is : ", e)


# function to get the execution time for each process
def getTime(date):
    if date == "timestamp":
        return str(datetime.datetime.timestamp(datetime.datetime.now())).split(".")[0]
    elif date == "date":
        return datetime.datetime.now()


def memory_check():
    mem = psutil.virtual_memory()
    total = mem.total / (1024 ** 3)
    available = mem.available / (1024.0 ** 3)
    used = mem.used / (1024 ** 3)
    free = mem.free / (1024 ** 3)
    memory_details = {"Total": round(total, 2), "Available": round(available, 2), "Used": round(used, 2),
                      "Free": round(free, 2)}
    return memory_details


if __name__ == "__main__":
    """ calling main function to process the audit zip file """
    logger.info('script started,memory: {}'.format(memory_check()))
    audit_list = DB.audit_information()
    audit_id_list = [i['auditId'] for i in audit_list]
    logger.info('Number of audits: %s', len(audit_id_list))
    for audit_info in audit_list:
        startTime = getTime("date")
        file = audit_info['fileName']  # 12345.zip
        file_name = file.split('.')[0]
        audit_id = audit_info['auditId']
        status = DB.status_check(audit_info['auditId'])
        logger.info('status checked')
        if status == 'created':
            try:
                status_upload = ''
                msg = ''
                logger.info("Processing: %s, memory:%s", audit_info['auditId'], memory_check())
                # update the audit information status as processing
                DB.update_audit_information(audit_id, 'Processing', 'Processing', 0)

                startTime_file = getTime("date")

                # download the zip file
                if audit_info['auditType'] == 'upload':
                    file_download = DB.file_download(file, audit_id)
                    if file_download is None:
                        logger.info('Unable to download the file')
                        endTime = getTime("date")
                        execution_time = str(endTime - startTime).split(".")[0]
                        logger.info("Exceution time of audit:%s,file:%s is %s", audit_info['auditId'], file,
                                    str(endTime - startTime).split(".")[0])
                        DB.update_audit_information(audit_id, 'Error', 'Error', execution_time)
                        status_upload = 'Error'
                        msg = 'Internal server error'
                        continue
                elif audit_info['auditType'] == 'import':
                    try:
                        file_download = S3Handler(location='US').download_imported_file(
                            audit_id=audit_info['auditId'], scriptPath=scriptPath)
                        logger.info('Downloaded the file from s3Bucket')
                    except Exception as e:
                        logger.error(e)
                else:
                    logger.error('Unable to proceed with downloading file since auditType is not matching...')
                    endTime = getTime("date")
                    execution_time = str(endTime - startTime).split(".")[0]
                    logger.info("Exceution time of audit:%s,file:%s is %s", audit_info['auditId'], file,
                                str(endTime - startTime).split(".")[0])
                    DB.update_audit_information(audit_id, 'Error', 'Error', execution_time)
                    status_upload = 'Error'
                    msg = 'Internal server error'
                    continue

                # extract the zip file
                try:
                    extractZip(file)
                except Exception as e:
                    logger.error('Error while extracting the file --'.format(e))
                    endTime = getTime("date")
                    execution_time = str(endTime - startTime).split(".")[0]
                    logger.info("Exceution time of audit:%s,file:%s is %s", audit_info['auditId'], file,
                                str(endTime - startTime).split(".")[0])
                    DB.update_audit_information(audit_id, 'Error', 'Error', execution_time)
                    status_upload = 'Error'
                    msg = 'Internal server error'
                    continue

                # Creating the working directory
                work_files.createWorkDirs(file_name)

                logger.info('before device_details:%s', format(memory_check()))

                # creating the device details json
                device_result = deviceDetails.device_to_chassis_mapping(audit_info)
                if device_result is None:
                    logger.error('Error while generating device details the file --')
                    endTime = getTime("date")
                    execution_time = str(endTime - startTime).split(".")[0]
                    logger.info("Exceution time of audit:%s,file:%s is %s", audit_info['auditId'], file,
                                str(endTime - startTime).split(".")[0])
                    DB.update_audit_information(audit_id, 'Error', 'Error', execution_time)
                    status_upload = 'Error'
                    msg = 'Internal server error'
                    continue
                else:
                    pass

                logger.info('after device_details:%s', format(memory_check()))

                # load table to nms mapping after parsing the file data
                nmsMapping.table_to_nms_mapping(audit_info)

                # create audit information json
                auditInsight.audit_information(audit_info)

                logger.info('before all_data:%s', format(memory_check()))

                # create all data json after parsing
                alldata_result = allData.all_data_json(audit_info)
                if alldata_result is None:
                    logger.error('Error while generating all data file --')
                    endTime = getTime("date")
                    execution_time = str(endTime - startTime).split(".")[0]
                    logger.info("Exceution time of audit:%s,file:%s is %s", audit_info['auditId'], file,
                                str(endTime - startTime).split(".")[0])
                    DB.update_audit_information(audit_id, 'Error', 'Error', execution_time)
                    status_upload = 'Error'
                    msg = 'Internal server error'
                    continue
                else:
                    pass

                logger.info('after all_data:%s', format(memory_check()))

                # create html files for node based tables
                addRemaining.add_remaining_files(audit_info)

                logger.info('after addRemaining:%s', format(memory_check()))
                # create json from the node based htmls
                createjson.add_remaining_json(audit_info)

                logger.info('after createjson:%s', format(memory_check()))
                # create exception json
                allException.exception_json(audit_info)

                # severityBreakdown.severity_breakdown_json(audit_info)

                netRulenetAdvice.netRule_netAdvice_json(audit_info)

                logger.info('after net_rule:%s', format(memory_check()))
                # insert all data to DB
                DB.insert_json_data()

                endTime = getTime("date")
                execution_time = str(endTime - startTime).split(".")[0]
                logger.info("Exceution of %s : %s ", file, execution_time)

                # update the audit information status as processing
                DB.update_audit_information(audit_id, 'Completed', 'Completed', execution_time)
                status_upload = 'Completed'
                msg = ''

            except Exception as e:
                # update the audit information status as processing
                endTime = getTime("date")
                execution_time = str(endTime - startTime).split(".")[0]
                DB.update_audit_information(audit_id, 'Error', 'Error', execution_time)
                status_upload = 'Error'
                msg = 'Internal server error'
                continue
            finally:
                file_name = audit_info['fileName'].split('.')[0]  # 12345.zip
                logger.info("Cleaning up ...")
                if os.path.exists(scriptPath + "/AuditReportViewer.htm"):
                    os.remove(scriptPath + "/AuditReportViewer.htm")
                if os.path.exists(scriptPath + "/audit_id.txt"):
                    os.remove(scriptPath + "/audit_id.txt")
                if os.path.exists(scriptPath + "/" + file_name):
                    directoryPath = os.path.join(scriptPath, file_name)
                    shutil.rmtree(directoryPath, ignore_errors=True, onerror=None)
                if os.path.exists(scriptPath + "/" + file_name + ".zip"):
                    os.remove(scriptPath + "/" + file_name + ".zip")
                if os.path.exists(scriptPath + "/ParsedFiles" + file_name):
                    shutil.rmtree(scriptPath + "/ParsedFiles" + file_name, ignore_errors=True, onerror=None)
                if os.path.exists(scriptPath + "/" + file_name):
                    logger.info('file is not deleted, check...')
                if os.path.exists(scriptPath + "/" + file_name + ".zip"):
                    logger.info('zip file not deleted, check...')
                if os.path.exists(scriptPath + "/ParsedFiles" + file_name):
                    logger.info('parsed file not deleted, check...')
                logger.info('memory:%s', format(memory_check()))
                logger.info('------------Processing of auditId %s Completed------------', audit_info['auditId'])
                sendMail(audit_info['userId'], audit_info['auditId'], audit_info['crPartyName'],
                         audit_info['fileName'], status_upload, msg)
                continue
        else:
            pass
