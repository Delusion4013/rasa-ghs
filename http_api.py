# rasa api启动
# 启动Rasa API服务 rasa run --enable-api
# 浏览器访问api地址，检验是否启动成功，默认：http://localhost:5005/
import json
import requests
from flask import Flask, request
import re
from pprint import pprint
import secrets

# 要启动Rasa API服务： rasa run --enable-api
s = requests.session()
s.keep_alive = False
app = Flask(__name__)
host = '0.0.0.0'
port = '10020'


def rasa_post(msg):
    url = "http://localhost:5005/model/parse"
    data = {"text": msg}
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    result = json.loads(r.text)
    pprint(result)
    # val = result[0]['text']
    # # 解析 dict
    intent_name = result['intent']['name']
    confidence_score = result['response_selector']['default']["response"]['confidence']
    probablity = str(confidence_score)
    # intent_name = result['intent']['name']
    # print(intent_name)
    # if intent_name != 'nlu_fallback':
    # if confidence_score>0.9:
    responses_list = result['response_selector']['default']['response']['responses']
    answer_id = re.sub('"', '', responses_list[0]['text'])
    return answer_id, probablity
    # else:
    #     answer_id = 'id_2022101903480505'
    #     probablity=0
    #     return answer_id,probablity



@app.route("/api/model/rasa", methods=["POST"])
def get_message():
    if request.method == 'POST':
        message = str(request.form.get('text'))
        print("message: {}".format(message))
        answer_id, prob = rasa_post(message)
        result = {
            "answer_id": answer_id,
            "probablity": prob
        }
        return result


if __name__ == '__main__':
    app.run(host, port, debug=True)
