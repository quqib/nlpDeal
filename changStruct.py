import copy
import pandas as pd


taskTableRelation = {
    "hw4_xy3465": {
        # 主表字段映射
        "唯一标识": "唯一标识",   # 左边是输出字段，右边是Excel列名
        "项目名称": "项目名称",
        "项目经理": "项目经理",

        # 子表映射
        "hw4_0bvd12": [
            {
                "成员名称": "成员名称",
                "职位": "职位"
            }
        ]
    }
}


# 读取excel
# usage
def parseExcel(path, taskTableRelation):
    # 加载Excel文件
    # file_path = 'datas/数据表.xlsx'
    excelFile = pd.ExcelFile(path)
    sheetNames = excelFile.sheet_names

    excelDataMap = {}
    for sheetName in sheetNames:
        sheetDataList = readSheetData(path, sheetName)
        if sheetDataList:
            excelDataMap[sheetName] = sheetDataList

    # 取指定表数据
    excelMainDataList = []
    for k, v in taskTableRelation.items():
        # 主表表名
        if k.startswith("hw4_") and isinstance(v, dict):
            excelMainDataList = excelDataMap.get(k)
            break

    # 封装excel最终数据
    resultList = []

    for excelMainData in excelMainDataList:
        taskTableRelationNew = copy.deepcopy(taskTableRelation)
        bindDataToTaskTableRelation(excelMainData, taskTableRelationNew, excelDataMap)
        resultList.append(taskTableRelationNew)

    return resultList



# 关系表绑定至excel数据
# @param: excelFatherData 父表数据
# @param: taskTableRelation 关系系
# @param: excelDataMap excel全部数据
# @param: sheetName 表名
def bindDataToTaskTableRelation(excelFatherData, taskTableRelation, excelDataMap, sheetName=""):
    if isinstance(taskTableRelation, dict):
        for k, v in taskTableRelation.items():
            # 主表
            if k.startswith("hw4_") and isinstance(v, dict):
                for mainKey, mainVal in v.items():
                    # mainVal是6个元素的数据
                    if isinstance(mainVal, str):
                        # 直接字段 @mainKey是35字段表格列名
                        v[mainKey] = excelFatherData.get(mainVal)
                    elif isinstance(mainVal, list):
                        # 子表
                        bindDataToTaskTableRelation(excelFatherData, mainVal, excelDataMap, mainKey)


    elif isinstance(taskTableRelation, list):

        if isinstance(excelFatherData, dict):
            # 主表行数据唯一标识
            id = excelFatherData.get("唯一标识")
            # 子表数据
            sheetDataList = excelDataMap.get(sheetName)

            if sheetDataList:
                # 把主表唯一键对应的子表数据进行获取
                filterSheetDataList = [sheetData for sheetData in sheetDataList if sheetData.get("父表唯一标识") == id]
                if filterSheetDataList:
                    newList = []

                    for sheetData in filterSheetDataList:
                        itemCopy = copy.deepcopy(taskTableRelation[0])
                        for kk, vv in itemCopy.items():
                            if isinstance(vv, str):
                                itemCopy[kk] = sheetData.get(vv, "")
                        newList.append(itemCopy)

                    taskTableRelation.clear()

                    taskTableRelation.extend(newList)

                else:
                    clearVal(taskTableRelation)

        else:
            clearVal(taskTableRelation)


'''清空value'''
def clearVal(taskTableRelation):
    if isinstance(taskTableRelation, list):
        for item in taskTableRelation:
            if isinstance(item, dict):
                for k, v in item.items():
                    item[k] = ''


def clean_cell_smart(val):
    """
    清洗单元格数据：
    - NaN / None -> 空字符串
    - 其他 -> 字符串，去除首尾空格
    """
    if pd.isna(val):  # 处理 NaN, None
        return ""
    return str(val).strip()


'''读取sheet中数据'''
def readSheetData(path, sheetName):
    # 使用pandas读取Excel表
    df = pd.read_excel(path, sheet_name=sheetName)

    # 将所有单元格进行字符串清洗，处理 NaN 转换成空字符等
    df = df.map(clean_cell_smart)

    sheetDataList = []
    # df.shape[0] 返回行数，df.shape[1] 返回列数
    for i in range(df.shape[0]):
        itemDict = {}
        for j in range(df.shape[1]):
            col_name = df.columns[j]
            cell_value = df.iat[i, j]
            # 调试时可用：
            # print(f"行索引 {i}, 列索引 {j}, 列名: {col_name}, 值: {cell_value}")
            itemDict[col_name] = cell_value
        sheetDataList.append(itemDict)

    return sheetDataList




if __name__ == "__main__":
    path = "数据表.xlsx"
    result = parseExcel(path, taskTableRelation)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
