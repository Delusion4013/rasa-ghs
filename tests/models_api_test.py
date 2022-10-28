# coding=utf8
import requests
import pandas as pd
import time


def rasa_model(data):
    querys = []
    answer = []
    probs = []
    times = []

    for i in test_data["question"]:
        # print(i)
        data = {"text":i}

        url = 'http://10.1.100.105:10020/api/model/rasa'
        time_start = time.time()
        res = requests.post(url=url, data=data)
        time_end = time.time()

        # print(res)

        timesss = str(time_end - time_start)
        req_json = res.json()
        answers = req_json["answer_id"]
        answers = answers[3:]
        # print(answers)
        probablity = req_json["probablity"]

        querys.append(i)
        answer.append(answers)
        probs.append(probablity)
        times.append(timesss)

    dicts = pd.DataFrame(querys)
    dicts1 = pd.DataFrame(answer)
    dicts2 = pd.DataFrame(probs)
    dicts3 = pd.DataFrame(times)
    dicts4 = pd.concat((dicts, dicts1), axis=1)
    dicts5 = pd.concat((dicts4, dicts2), axis=1)
    dicts6 = pd.concat((dicts5, dicts3), axis=1)
    dicts6.to_excel("results.xlsx", index=None, header=["question", "rasa_answer_id", "预测分值", "响应时间"])

def concat_and_evaluate(test_pred, test_true):
    res = pd.concat((test_pred, test_true), axis=1)
    accuracy = (res['rasa_answer_id'] == res['answer_id']).sum() / res.shape[0]
    print(f"Rasa accuracy: {accuracy*100:.2f}%")

def test_event_model(data):
    querys = []
    event_ids = []
    probs = []
    for i in data["question"]:
        channel_code = "617"
        data = {"query": i, "type": channel_code}
        url = "http://8.136.15.60:10019/api/model/singleTurnFaq"
        req = requests.post(url=url, data=data)
        print(req.json())
        req_json = req.json()
        answer_id = req_json["answer_id"]
        querys.append(i)
        if answer_id:
            answer_id = "id_" + str(answer_id)
            probs.append(1)
            event_ids.append(answer_id)
        else:
            event_id = req_json["eventIds"][0]["event_id"]
            prob = req_json["eventIds"][0]["prob"]
            event_id = "id_" + str(event_id)
            event_ids.append(event_id)
            probs.append(prob)
    dicts = pd.DataFrame(querys)
    dicts1 = pd.DataFrame(event_ids)
    dicts2 = pd.DataFrame(probs)
    dicts3 = pd.concat((dicts, dicts1), axis=1)
    dicts4 = pd.concat((dicts3, dicts2), axis=1)
    dicts4.to_excel("事件模型测试结果.xlsx", index=None, header=["query", "answer_id", "times"])
    # return dicts4

if __name__ == '__main__':
    test_file = "test.xlsx"
    test_data = pd.read_excel(test_file)
    rasa_model(test_data)
    test_pred = pd.read_excel("results.xlsx")
    concat_and_evaluate(test_pred, test_data)

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
