# coding: utf-8

import requests

date = "2019-06-11"
def getTransInfoByTrainCode(trainCode):
    url = "https://search.12306.cn/search/v1/train/search"
    params = {"keyword" : trainCode, "date" : date.replace("-", ""), "_" : "_"}
    rsp = requests.get(url, params).json()
    #print(rsp)
    if "data" in rsp:
        return rsp["data"]
    return []

def getStationsOfTrainNo(trainNo):
    url = "https://www.12306.cn/index/otn/index12306/queryStopStations"
    params = {"train_no": trainNo, "depart_date": date}
    rsp = requests.get(url, params).json()
    return rsp["data"]

def showCheckInInfo(trainCode):
    print("查询 {} 检票口：".format(trainCode.upper()), end="")
    trainsInfo = getTransInfoByTrainCode(trainCode)
    if not trainsInfo:
        print("查询失败...")
        return
    if trainCode != trainsInfo[0]["station_train_code"]:
        print("查询失败：暂无此车次")
        return
    trainNo = trainsInfo[0]["train_no"]
    stations = getStationsOfTrainNo(trainNo)
    if not stations:
        print("查询失败...")
        return

    print("\n{} 列车信息： 从 {} 开往 {} 途经：".format(trainsInfo[0]["station_train_code"], trainsInfo[0]["from_station"], trainsInfo[0]["to_station"]), end="")
    for stationNo in sorted(stations):
        print(stations[stationNo][0], end=", ")
    print()

    url = "https://www.12306.cn/index/otn/index12306/queryTicketCheck"
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    for stationNo in sorted(stations):
        stationName = stations[stationNo][0]
        stationCode = stations[stationNo][1]
        payload = {"trainDate": date, "station_train_code": trainCode, "from_station_telecode": stationCode}
        checkInInfo = requests.post(url, data=payload, headers=header).json()["data"]
        if checkInInfo:
            print("{:　<5} {:<8} 检票口：{}".format(stationName, trainCode, checkInInfo))


def showTransInfoByTrainCode(trainCode):
    trainsInfo = getTransInfoByTrainCode(trainCode)
    if not trainsInfo:
        print("查询列车 {} 信息失败".format(trainCode.upper()))
        return
    for info in trainsInfo:
        print("时间：{} 从 {:　<5} 开往 {:　<5} 车次: {:<8} 途经：".format(info["date"], info["from_station"], info["to_station"], info["station_train_code"]), end="")
        stations = getStationsOfTrainNo(info["train_no"])
        for stationNo in sorted(stations):
            print(stations[stationNo][0], end=", ")
        print()

#showTransInfoByTrainCode("G622")
showCheckInInfo("G6258")