import pymongo
from contextlib import contextmanager
from db_credentials import *
from log import logger
import gridfs
import work_files
import json
import os

# scriptpath
scriptPath = os.path.dirname(os.path.realpath(__file__))


@contextmanager
def mongo_connection():
    mdbclient = pymongo.MongoClient(MONGO_HOST_CONNECTION)
    try:
        logger.info('db connection successful')
        yield DIDB(mdbclient)

    except pymongo.errors.ConnectionFailure as e:
        logger.info('db connection error : %s' % e)
    finally:
        mdbclient.close
        logger.info('db connection closed')


class DIDB:
    def __init__(self, mdbclient):
        self.db = mdbclient[MONGO_DB]
        self.commonDB = mdbclient[MONGO_COMMOM_DB]
        self.audit_information = self.commonDB["audit_information"]
        self.np_inventory = self.db['np_inventory']
        self.audit_table_data = self.db['audit_table_data']
        self.decice_audits_exception = self.db['decice_audits_exception']
        self.decice_audits_all = self.db['decice_audits_all']
        self.exception_data = self.db['exception_data']
        self.hardware_summary = self.db['hardware_summary']
        self.software_summary = self.db['software_summary']
        self.severities_breakdown = self.db['severities_breakdown']
        self.audit_insights = self.db['audit_insights']
        self.netRule_netAdvice = self.db['netRule_netAdvice']
        self.recommendation = self.db['recommendation']
        self.NMS_mapping = self.db['NMS_mapping']
        self.device_details = self.db['device_details']
        self.fs = gridfs.GridFS(self.db)
        self.files = self.db.fs.files


# write data from fs to file
def write_data(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
        logger.info('Data has been written to the file')


# getting audit information whereas status is created
def audit_information():
    try:
        with mongo_connection() as didb:
            sortField = 'creationTime'
            sortDir = 1
            audit_info = list(didb.commonDB.audit_information.find({'statusInternal': 'created', "type": "CNA"
                                                                    }
                                                                   ).sort(sortField, sortDir))
            if len(audit_info) == 0:
                logger.info('---No audit files are available to process---')
            return audit_info
    except Exception as e:
        logger.error(e)


# getting audit information whereas status is created
def status_check(audit_id):
    try:
        with mongo_connection() as didb:

            audit_info = list(didb.commonDB.audit_information.find({'auditId': audit_id},
                                                                   {'_id': 0, 'statusInternal': 1}))
            return audit_info[0]['statusInternal']
    except Exception as e:
        logger.error(e)


# update audit information as status is in-progress/ completed
def update_audit_information(audit_id, status_internal, status, time):
    try:
        with mongo_connection() as didb:
            didb.commonDB.audit_information.update_one({"auditId": audit_id},
                                                       {'$set': {'statusInternal': status_internal, 'status': status,
                                                                 'executionTime': time}})
            logger.info('status has been updated: %s', status)
    except Exception as e:
        logger.error(str(e))


# insert all data to DB
def insert_json_data():
    try:
        with mongo_connection() as didb:
            if os.path.isfile(work_files.dataDir + "audit_insight.json"):
                with open(work_files.dataDir + "/audit_insight.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.audit_insights.insert_one(jsonData)
                        logger.info('--data inserted, file_name:audit_insight.json')
            if os.path.isfile(work_files.dataDir + "device_details.json"):
                with open(work_files.dataDir + "device_details.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.device_details.insert_one(jsonData)
                        logger.info('---data inserted in device_details')
            if os.path.isfile(work_files.dataDir + "nms_map.json"):
                with open(work_files.dataDir + "nms_map.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.NMS_mapping.insert_one(jsonData)
                        logger.info('---data inserted in nms data')
            for file in os.listdir(work_files.dataDir):
                if file.startswith("audit_table_data"):
                    with open(work_files.dataDir + file, "r") as json_file:
                        jsonData = json.loads(json_file.read())
                        if len(jsonData) > 0:
                            didb.db.audit_table_data.insert_many(jsonData)
                            logger.info('---data inserted in all data,filename:{}'.format(file))
            if os.path.isfile(work_files.dataDir + "exception_data.json"):
                with open(work_files.dataDir + "exception_data.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.exception_data.insert_many(jsonData)
                        logger.info('---data inserted in exception')
            if os.path.isfile(work_files.dataDir + "severity_breakdown.json"):
                with open(work_files.dataDir + "severity_breakdown.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.severities_breakdown.insert_one(jsonData)
                        logger.info('---data inserted in severity breakdown')
            if os.path.isfile(work_files.dataDir + "netRule_netAdvice.json"):
                with open(work_files.dataDir + "netRule_netAdvice.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.netRule_netAdvice.insert_many(jsonData)
                        logger.info('---data inserted in netrule netadvise')
            # if os.path.isfile(work_files.dataDir + "audit_table_data_node.json"):
            #     with open(work_files.dataDir + "audit_table_data_node.json", "r") as json_file:
            for file in os.listdir(work_files.dataDir):
                if file.startswith("audit_table_data_node"):
                    with open(work_files.dataDir + file, "r") as json_file:
                        jsonData = json.loads(json_file.read())
                        if len(jsonData) > 0:
                            didb.db.audit_table_data.insert_many(jsonData)
                            logger.info('node data inserted in audit table data')
            if os.path.isfile(work_files.dataDir + "exceptions_data_node.json"):
                with open(work_files.dataDir + "exceptions_data_node.json", "r") as json_file:
                    jsonData = json.loads(json_file.read())
                    if len(jsonData) > 0:
                        didb.db.exception_data.insert_many(jsonData)
                        logger.info('---node data inserted in exception')

    except Exception as e:
        logger.error("*** Error while inserting data into DB *** please check DB.py file**** {}".format(e))


# insert single document data in collection
def insert_data(json_data, collection_name):
    try:
        with mongo_connection() as didb:
            collection = didb.db[collection_name]
            collection.insert_one(json_data)
            logger.info('Data got inserted in %s', collection_name)
    except Exception as e:
        logger.error(str(e))


# insert multiple document data in collection
def insert_many_data(json_data, collection_name):
    try:
        with mongo_connection() as didb:
            collection = didb.db[collection_name]
            collection.insert_many(json_data)
            logger.info('multiple document got inserted to %s collection', collection_name)
    except Exception as e:
        logger.error(str(e))


# getting audit extracted data whereas status is created
def get_data(collection_name):
    try:
        with mongo_connection() as didb:
            collection = didb.db[collection_name]
            data = list(collection.find({}, {'_id': 0, 'audit_name': 1, 'table_name': 1}))
            return data
    except Exception as e:
        logger.error(str(e))


# downloading the file where the status is created
def file_download(filename, audit_id):
    try:
        with mongo_connection() as didb:
            data = didb.files.find_one({'filename': filename, 'auditId': audit_id})
            logger.info('get details from fs.files')
            my_id = data['_id']
            output_data = didb.fs.get(my_id).read()
            downloadLoc = scriptPath + "/" + filename.split('.')[0] + ".zip"
            logger.info("downloading the zip file")
            write_data(downloadLoc, output_data)
            return 'Successfully downloaded file'
    except Exception as e:
        logger.error(e)
        return None
