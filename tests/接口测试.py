# coding=utf8
import requests
import pandas as pd
import time


def rasa_model(data):
    querys=[]
    answer=[]
    probablitys=[]
    times=[]
    # # i="你好"
    # # with open("test.txt","w",encoding="utf-8") as f:
    for i in data1["question"]:
        print(i)
        data={"text":i}
        url = 'http://10.1.100.105:10020/api/model/rasa'
        time_start=time.time()
        req = requests.post(url=url, data=data)
        time_end=time.time()
        timesss=str(time_end-time_start)
        print(req.json())
        req_json=req.json()
        answers=req_json["answer_id"]
        probablity=req_json["probablity"]
        # timess=req_json["time_delta"]
        # f.write(i+"\t"+answers+"\t"+timesss+"\n")
        querys.append(i)
        answer.append(answers)
        probablitys.append(probablity)
        times.append(timesss)
    print(querys)
    dicts=pd.DataFrame(querys)
    dicts1=pd.DataFrame(answer)
    dicts2=pd.DataFrame(probablitys)
    dicts3=pd.DataFrame(times)
    dicts4=pd.concat((dicts,dicts1),axis=1)
    dicts5=pd.concat((dicts4,dicts2),axis=1)
    dicts6=pd.concat((dicts5,dicts3),axis=1)
    # dicts[:,"querys"]=querys
    # dicts[:,"answer"]=answer
    # dicts[:,"times"]=times
    # dicts6.loc[:,"原始id"]=data1["answer_id"]
    dicts6.to_excel("模型测试结果1.xlsx",index=None,header=["question","answer_id","预测分值","响应时间"])
def event_model(data):
    querys=[]
    event_ids=[]
    probs=[]
    for i in data1["question"]:
        j="617"
        data={"query":i,"type":j}
        url="http://8.136.15.60:10019/api/model/singleTurnFaq"
        req = requests.post(url=url, data=data)
        print(req.json())
        req_json = req.json()
        answer_id=req_json["answer_id"]
        querys.append(i)
        if answer_id:
            answer_id="id_"+str(answer_id)
            probs.append(1)
            event_ids.append(answer_id)
        else:
            event_id = req_json["eventIds"][0]["event_id"]
            prob = req_json["eventIds"][0]["prob"]
            event_id="id_"+str(event_id)
            event_ids.append(event_id)
            probs.append(prob)
    dicts = pd.DataFrame(querys)
    dicts1=pd.DataFrame(event_ids)
    dicts2=pd.DataFrame(probs)
    dicts3=pd.concat((dicts,dicts1),axis=1)
    dicts4=pd.concat((dicts3,dicts2),axis=1)
    dicts4.to_excel("事件模型测试结果.xlsx",index=None,header=["query","answer_id","times"])

if __name__ == '__main__':
    data1 = pd.read_excel(r"测试样本.xlsx")
    rasa_model(data1)
# data=pd.read_excel("模型测试结果.xlsx")
# print(data.head())
# with open("test.txt","r",encoding="utf-8") as f:
#     data=f.readlines()
#     aa=[]
#     bb=[]
#     cc=[]
#     for i in data:
#         i=i.strip()
#         a=i.split("\t")[0]
#         b=i.split("\t")[1]
#         c=i.split("\t")[2]
#         aa.append(a)
#         bb.append(b)
#         cc.append(c)
#     data_fram=pd.DataFrame(aa)
#     dataq_fram=pd.DataFrame(bb)
#     cc=pd.DataFrame(cc)
#     dd=pd.concat((data_fram,dataq_fram),axis=1)
#     ee=pd.concat((dd,cc),axis=1)
#     ee.to_excel("aa.xlsx")
    # data_fram[:,"问题"]=aa
    # data_fram[:,"答案"]=bb
    # data_fram[:,"时间"]=cc
    # data_fram.to_excel("aa.xlsx")