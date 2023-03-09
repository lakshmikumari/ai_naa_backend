import concurrent
import os
import re
from bs4 import BeautifulSoup
import getNMSArea
from log import logger
import work_files
import json

# script path
scriptPath = os.path.dirname(os.path.realpath(__file__))


# function to write into a file
def writeData(file_name, data):
    with open(file_name, "w") as f:
        f.write(json.dumps(data))


# getting the table name
def getTableName(file_name):
    html_data = ""
    tableName = []
    # with open(file_name, "r", encoding="utf-8") as f:
    with open(file_name, "r") as f:
        html_data = f.read()
    if len(html_data) > 2:
        soup = BeautifulSoup(html_data, features="html.parser")
        x = soup.find("thead")
        # print("in getTableName :: " + str(x))
        if x:
            rows = x.findChildren('tr')
            tableName = [x.getText() for x in rows[0].findChildren('td')]
            tableName[0] = tableName[0].replace("/", " ")[0:100]
            return tableName
        else:
            return file_name.split(".")[0]


# Getting the column names
def getColumnNames(file_name):
    html_data = ""
    columnNames = []
    with open(file_name, "r") as f:
        html_data = f.read()

    soup = BeautifulSoup(html_data, features="html.parser")
    x = soup.find("thead")
    rows = x.findChildren('tr')
    if len(rows) > 1:
        rows = rows[1:]
    k = 0
    for row in reversed(rows):
        k = k + 1
        currentPointer = 0
        cols = row.findChildren('td')

        for col in cols:
            if int(col["colspan"]) == 1 and int(col["rowspan"]) == k:
                columnNames.insert(currentPointer, col.getText().replace("\xa0", ""))
                currentPointer = currentPointer + 1
            else:
                for i in range(0, int(col["colspan"])):
                    temp = columnNames[currentPointer + i]
                    temp = col.getText() + " - " + temp
                    columnNames[currentPointer + i] = temp
                currentPointer = currentPointer + int(col["colspan"])

    return columnNames


def convertTable(stat_table):
    """trigers only if rowspan in cell,
    this function will change the table's rowspan data to table heading then returns the converted table
    """
    tbl = str(stat_table)
    rowPtr = []
    tbl = tbl[tbl.find('</thead>') + 8:]
    tbl_list = tbl.split("</td>")
    for i in range(0, len(tbl_list) - 1):
        if "<tr" in tbl_list[i]:
            currItem = tbl_list[i]
            tbl_list[i] = currItem[0: currItem.find(">") + 1]
            tbl_list.insert(i + 1, currItem[currItem.find(">") + 1:])

    for _ in range(4):
        for i in range(0, len(tbl_list)):
            if "</tr><tr" in tbl_list[i]:
                currItem = tbl_list[i]
                tbl_list[i] = currItem[0:5]
                currItem = currItem[5:]
                tbl_list.insert(i + 1, currItem[0:currItem.find(">") + 1])
                tbl_list.insert(i + 2, currItem[currItem.find(">") + 1:])

    # if <tr in tbl_list
    [rowPtr.append(i) for i in range(0, len(tbl_list) - 1) if ("<tr" in tbl_list[i])]

    w, h = (rowPtr[1] - rowPtr[0]), len(rowPtr)
    Matrix = [[0 for x in range(w)] for y in range(h)]
    j, k = -1, 0
    # import pdb; pdb.set_trace()
    for i in range(0, len(tbl_list)):
        if "<tr" in tbl_list[i]:
            j = j + 1
            k = 0
        while Matrix[j][k] != 0:
            k = k + 1
        if "tr" not in tbl_list[i]:
            rowspan = re.findall("rowspan=\"\d\"", tbl_list[i])
            if not rowspan:
                rowspan = ["rowspan=1 "]
            if int(rowspan[0][-2:-1]) > 1:
                for locPtr in range(1, int(rowspan[0][-2:-1])):
                    Matrix[j + locPtr][k] = re.sub("rowspan=\"\d\"", '', tbl_list[i])
            Matrix[j][k] = re.sub("rowspan=\"\d\"", '', tbl_list[i]) + "</td>"
        else:
            Matrix[j][k] = re.sub("rowspan=\"\d\"", '', tbl_list[i])

    tableStr = str(stat_table)
    tableStr = tableStr[0: tableStr.find('</thead>') + 8]
    for item in Matrix:
        for k in range(0, len(item)):
            if item[k] != 0:
                tableStr = tableStr + item[k]

    # import pdb; pdb.set_trace()
    return tableStr


# getting the table data from html
def getTableData(file_name):
    html_data = ""
    with open(file_name, "r") as f:
        html_data = f.read()
    html_data = html_data.replace("<B>", "")
    html_data = html_data.replace("</B>", "")
    soup = BeautifulSoup(html_data, features="html.parser")
    stat_table = soup.find('table')
    # print(stat_table)
    # stat_table=stat_table[0]
    data = []
    sev_data = []
    rowspanflag = 0
    doneFlag = 0
    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td', class_=True):
            if "rowspan" in str(cell.encode("utf-8")):
                x = re.search('rowspan.*=.*1', str(cell.encode("utf-8")))
                if x:
                    continue
                try:
                    stat_table = convertTable(stat_table)
                except Exception as e:
                    logger.debug("Error in convertTable() function. Not processing this further %s", e)
                    return None, None

                # print(stat_table)
                doneFlag = 1
            if doneFlag == 1:
                break
        if doneFlag == 1:
            break

    if isinstance(stat_table, str):
        soup = BeautifulSoup(stat_table, features="html.parser")
        stat_table = soup.find('table')

    for row in stat_table.find_all('tr'):
        for cell in row.find_all('td', class_=True):
            y = cell.text.replace("\xa0", " ")
            sev = cell["class"][0]
            if 'ADDFFF' in sev:
                sev_data.append("Critical")
            elif 'FF0000' in sev:
                sev_data.append("High")
            elif 'F9966B' in sev:
                sev_data.append("Medium")
            elif 'FFFF00' in sev:
                sev_data.append("Low")
            elif '00FF00' in sev:
                sev_data.append("Informational")
            else:
                sev_data.append("White")

            data.append(y)

    return data, sev_data


def createJson(f, audit_info, nms_map_json, device_details_data):
    """ Creates json files including serverties into /json folder
    """
    try:
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        fName = (getTableName(f)[0]).strip()
        fName = re.sub(' +', ' ', fName)
        logger.info('file name: %s,table name: %s', f, fName)
        # fName = f.split('-')[0] + '-' +fName
        # audit_name = (f.split('-')[1]).split('.')[0]
        audit_name = f.split('-')[-1][0:-5]
        jsonData = {"crPartyId": audit_info['crPartyId'], "crPartyName": audit_info['crPartyName'],
                    "cpyKey": audit_info['cpyKey'], "location": audit_info['location'],
                    "auditId": audit_info['auditId'], "auditName": audit_name,
                    "tableName": fName, "NMSArea": "", "Critical": 0, "High": 0, "Medium": 0, "Low": 0,
                    "Informational": 0, "columnNames": [], "data": []}
        alljson = {"crPartyId": audit_info['crPartyId'], "crPartyName": audit_info['crPartyName'],
                   "cpyKey": audit_info['cpyKey'], "location": audit_info['location'],
                   "auditId": audit_info['auditId'], "auditName": audit_name,
                   "tableName": fName, "NMSArea": "", "chassis_name": ""}
        # nms_area = getNMSArea(fName, nms_map_json)
        nms_area = ''
        try:
            nmsData = nms_map_json[audit_name]
            nms_area = getNMSArea.getNMSArea(fName, nmsData)
        except Exception as e:
            nms_area = ''
        if nms_area == "":
            jsonData["NMSArea"] = "Verify Manually"
            alljson['NMSArea'] = "Verify Manually"
        else:
            jsonData['NMSArea'] = nms_area
            alljson['NMSArea'] = nms_area

        # process and returns the column names
        try:
            column_names = getColumnNames(f)
        except Exception as e:
            logger.debug('no columns are there for table')
            return None, None
        jsonData["columnNames"] = column_names

        try:
            table_data, sev_data = getTableData(f)
        except Exception as e:
            logger.error(f"Error in processing {f}. Not processing further")

        if len(table_data) % len(column_names) != 0:
            for filler in range(0, len(column_names) - (len(table_data) % len(column_names))):
                table_data.append("0")
                sev_data.append("White")

        table_data_list = []
        sev_data_list = []
        data_dict = {}
        list_of_document = []
        if len(table_data) != 0 and any("Host" in s for s in column_names):
            x = 0
            y = len(table_data)
            for i in range(x, y, len(column_names)):
                x = i
                table_data_list.append(table_data[x:x + len(column_names)])
                sev_data_list.append(sev_data[x:x + len(column_names)])

            data_json = []
            for i in range(0, len(table_data_list)):
                devName = ""
                chassis_name = ""
                ip_address = ''
                device_id = ''
                # get device name, deviceId using ipaddress present in device name
                # for s in table_data_list[i]:
                #     device_match = re.search(pattern, s)
                #     if device_match is not None:
                #         devName = s.split('(')[0]
                if "OSPF Neighbor Table for each sample (Exceptions" in fName:
                    cell_value = table_data_list[i][1]
                    devName = cell_value.split('(')[0]
                else:
                    cell_value = table_data_list[i][0]
                    devName = cell_value.split('(')[0]
                    # ip_address = pattern.search(s)[0] try: deviceId = [i['deviceId'] for i in device_data['data']
                    # if i['deviceIp'] == ip_address.strip()] if len(deviceId) != 0: device_id = deviceId[0] except
                    # Exception as e: #logger.debug('Error in getting the device_id from ipaddress'.format(e))
                    # device_id = '' else: pass
                # getting the chassis name
                # for data in device_details_data:
                #     if devName.strip() in data["node_name"]:
                #         chassis_name = data["model"]
                if devName.strip() in device_details_data:
                    deviceName = devName.strip()
                    chassis_name = device_details_data[deviceName]['model']
                    device_id = device_details_data[deviceName]['device_id']
                # try:
                #     device_id = ''
                #     if len(device_data) != 0:
                #         deviceId = [i['deviceId'] for i in device_data['data'] if i['deviceIp'] == ip_address]
                #         if len(deviceId) != 0:
                #             device_id = deviceId[0]
                # except Exception as e:
                #     logger.debug('Error in getting device id'.format(e))
                alljson['chassis_name'] = chassis_name

                row_data = []
                row_data_all = {}
                #if "\u00a0" in devName:
                    #devName = devName.strip().split("\u00a0")[0] + " " + devName.strip().split("\u00a0")[-1]
                # print("number of columns in table are ::: "+str(len(column_names))+" and row number is "+ str(i))

                for j in range(0, len(column_names)):
                    jjson = {}
                    j_json = {}

                    jjson[column_names[j]] = {"device_name": devName.strip(), 'device_id': device_id,
                                              "chassis_type": chassis_name,
                                              "value": table_data_list[i][j], "Sev": sev_data_list[i][j],
                                              "row_number": i + 1}
                    if 'Host Name' in column_names[j]:
                        j_json['Host Name'] = {"display_name": column_names[j], "value": table_data_list[i][j],
                                               "Sev": sev_data_list[i][j]}
                    else:
                        j_json[column_names[j]] = {"value": table_data_list[i][j], "Sev": sev_data_list[i][j]}
                    row_data.append(jjson)
                    row_data_all.update(j_json)
                    row_number = i + 1
                    if sev_data_list[i][j] == "Low":
                        jsonData["Low"] = jsonData["Low"] + 1
                    elif sev_data_list[i][j] == "High":
                        jsonData["High"] = jsonData["High"] + 1
                    elif sev_data_list[i][j] == "Medium":
                        jsonData["Medium"] = jsonData["Medium"] + 1
                    elif sev_data_list[i][j] == "Critical":
                        jsonData["Critical"] = jsonData["Critical"] + 1
                    elif sev_data_list[i][j] == "Informational":
                        jsonData["Informational"] = jsonData["Informational"] + 1
                data_dict[str(row_number)] = row_data_all
                data_json.append(row_data)
            jsonData["data"] = data_json
            alljson['device_id'] = device_id
            for key, value in data_dict.items():
                examp_dict = {'data': value, 'rowNum': key}
                examp_dict.update(alljson)
                list_of_document.append(examp_dict)

            return list_of_document, jsonData
        else:
            return None, None
    except Exception as e:
        logger.error(e)


def add_remaining_json(audit_info):
    try:
        nodeDir = work_files.addRemainingDir
        allData_list = []
        json_data_list = []
        file_name = audit_info['fileName'].split('.')[0]
        allFileName = work_files.allData_addremaining(scriptPath, file_name).split('.')[0]
        allCount = 1
        with open(work_files.dataDir + "nms_map.json", "r") as f:
            nms_map_json = json.loads(f.read())
        # with open(work_files.dataDir + "device_details.json", "r") as f:
        #     device_details_data = (json.loads(f.read()))['data']
        with open(work_files.internalDir + "deviceId.json", "r") as f:
            device_details_data = (json.loads(f.read()))

        entries_to_remove = ('auditId', 'crPartyId', 'crPartyName')
        for k in entries_to_remove:
            nms_map_json.pop(k)
        if os.listdir(nodeDir):
            logger.info('Parsing node based html files')
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    results = [executor.submit(createJson, nodeDir + f, audit_info, nms_map_json, device_details_data)
                               for f in os.listdir(nodeDir) if f.endswith(".html")]

                    for f in concurrent.futures.as_completed(results):
                        alldata = f.result()[0]
                        jsonData = f.result()[1]
                        if alldata is not None:
                            allData_list.extend(alldata)
                        if jsonData is not None:
                            json_data_list.append(jsonData)
                        # logger.info('alldata list size:{}'.format(allData_list.__sizeof__()))
                        if allData_list.__sizeof__() > 100000:
                            logger.info('SIZE exceeds 100 KB for allData:{}'.format(allData_list.__sizeof__()))
                            writeData(allFileName + '_' + str(allCount) + '.json', allData_list)
                            filename = allFileName + '_' + str(allCount) + '.json'
                            file_size = os.stat(allFileName + '_' + str(allCount) + '.json').st_size
                            logger.info("{}: created, size: {} KB".format(filename, file_size / 1024))
                            allCount += 1
                            allData_list.clear()
            except Exception as e:
                logger.error(e)
            # all table data having device_name and chassis_name, to be use to generate exception
            if len(json_data_list) > 0:
                logger.info('size < 100 KB,json size:{}'.format(json_data_list.__sizeof__()))
                writeData(work_files.exceptionjson_addremaining(scriptPath, file_name), json_data_list)
                file_size = os.stat(work_files.exceptionjson_addremaining(scriptPath, file_name)).st_size
                logger.info("allData_node.json created, size: {}".format(file_size / 1024))
            # all data without device-name and chassis name
            if len(allData_list) > 0:
                logger.info('size < 100 KB,all data size:{}'.format(allData_list.__sizeof__()))
                writeData(work_files.allData_addremaining(scriptPath, file_name), allData_list)
                file_size = os.stat(work_files.allData_addremaining(scriptPath, file_name)).st_size
                logger.info("audit_table_data_node.json created, size: {}".format(file_size / 1024))
        else:
            logger.info('No html files to process for node documents')

    except Exception as e:
        logger.error('***Error in createjson.py file'.format(e))
