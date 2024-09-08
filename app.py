# app.py
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

import json

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        response_text = ""
        previous_message = ""  # 중복 메시지를 확인하기 위한 변수

        with requests.post(self._host + '/testapp/v1/tasks/2wk14jt9/chat-completions',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    # "data:"로 시작하는 라인에서 JSON 형식의 메시지 추출
                    if decoded_line.startswith("data:"):
                        try:
                            # JSON 문자열을 Python 딕셔너리로 변환
                            json_data = json.loads(decoded_line[5:])
                            # "content" 키가 있는 경우 메시지 추가
                            if 'message' in json_data and 'content' in json_data['message']:
                                current_message = json_data['message']['content']
                                # 중복 메시지 확인: 이전 메시지와 같지 않으면 추가
                                if current_message != previous_message:
                                    response_text += current_message
                                    previous_message = current_message
                            # "stopReason"으로 응답이 종료된 시점 확인
                            if 'stopReason' in json_data and json_data['stopReason'] is not None:
                                break
                        except json.JSONDecodeError:
                            continue

        # 추출된 전체 메시지 반환
        return response_text.strip() if response_text else "응답을 처리하지 못했습니다."


# API 키 설정
completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYzliiThaVNY20aNF1/J33m+ttZZmfwcd8McUmO7CG7I9',
        api_key_primary_val='aZYj03o8vtBH1LD7p8c9BpWipwWIytzG3b3ok1Ob',
        request_id='031e55a4-4151-4875-96d7-15348ddca025'
    )


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    preset_text = [{"role":"system","content":"친구처럼 대화하듯이 반말로 답변한다."},{"role": "user", "content": user_message}]
    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 501,
        'temperature': 0.3,
        'repeatPenalty': 7.99,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    response = completion_executor.execute(request_data)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
