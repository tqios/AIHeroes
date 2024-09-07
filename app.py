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

        with requests.post(self._host + '/testapp/v1/tasks/5s8i93pa/chat-completions',
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


# API 키 설정 (이 부분은 실제 키로 교체)
completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYzliiThaVNY20aNF1/J33m+ttZZmfwcd8McUmO7CG7I9',
        api_key_primary_val='aZYj03o8vtBH1LD7p8c9BpWipwWIytzG3b3ok1Ob',
        request_id='14b03c4d-6622-4634-a554-a1ad13d61b6f'
)
# completion_executor = CompletionExecutor(
#         host='https://clovastudio.stream.ntruss.com',
#         api_key='NTA0MjU2MWZlZTcxNDJiYzliiThaVNY20aNF1/J33m+ttZZmfwcd8McUmO7CG7I9',
#         api_key_primary_val='aZYj03o8vtBH1LD7p8c9BpWipwWIytzG3b3ok1Ob',
#         request_id='9045a73a-8b56-4325-8670-ebfe70cb3ae8'
#     )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    preset_text = [{"role": "user", "content": user_message}]
    #preset_text = [{"role":"system","content":"- 답변을 사용자와 친구처럼 대화하듯이 대화체로 구성할 것 "},{"role":"user","content":"금연을 빨리 해야하는 이유는 뭐야? \r\n\n"},{"role":"assistant","content":"흡연이 건강에 안 좋다는 건 알고 있지? 흡연으로 인해 발생하는 질병들이 정말 많아. 폐암, 후두암, 구강암 등 각종 암부터 시작해서 호흡기 질환, 심혈관 질환까지 다양한 질병들이랑 연관되어 있어. 그리고 담배를 피면 피부도 나빠지고 치아도 노랗게 변하잖아. 이런 외모적인 부분에서도 문제가 생기고 말이야. 또 냄새도 나고 주변 사람들에게 피해를 주기도 하고. 그래서 금연을 빨리 하는 게 좋아!"},{"role":"user","content":"금연의 장점을 알려줘 \r\n\n"},{"role":"assistant","content":"우선 가장 큰 장점은 건강이지! 앞서 말했듯이 여러 가지 질병들을 예방할 수 있고 수명도 연장돼. 게다가 깨끗한 혈관 덕분에 혈압이나 혈당 조절에도 도움이 되고 운동 능력도 향상된다고 해. 그 외에도 돈 절약, 시간 절약, 자신감 상승 같은 부가적인 장점들도 많고 가족이나 지인들에게도 간접흡연의 피해를 주지 않게 돼. 어때 끌리지 않아?"},{"role":"user","content":"건강 말고 다른 장점은 어떤게 있어?"},{"role":"assistant","content":"경제적으로도 이득이라는 점 또한 무시할 수 없지! 하루 한 갑 기준으로 1년이면 약 163만원 정도 아낄 수 있다고 해. 이 금액이라면 여행을 가거나 평소 갖고 싶었던 물건을 살 수도 있겠지? 거기다 담배를 사기 위해 편의점 가는 시간도 줄어들고 옷이나 차에서 나는 불쾌한 냄새도 사라질 거야. 무엇보다 비흡연자라는 사실 만으로도 스스로 자부심을 느낄 수 있을거야!"},{"role":"user","content":"성별에 따라 흡연 원인에 차이가 있어?\r\n여성의 금연 방법을 알려줘. \r\n\n"},{"role":"assistant","content":"남성들은 대개 호기심이나 스트레스 때문에 흡연을 시작하는데 여성들은 사회적인 압박이나 다이어트 목적으로 피우는 경우가 많다고 해. 하지만 성별 상관없이 중독성이 강하기 때문에 쉽게 끊을 수 없는 공통점이 있기도 하지.\r\n \r\n여성이라고 해서 특별한 금연 방법이 있는 건 아니지만 몇 가지 팁을 주자면 우선 목표 기간을 짧게 설정해봐. 예를 들어 '일주일만 참자!' 라는 식으로 말이야. 이렇게 작은 성공 경험들이 모여 결국엔 금연에 성공할 수 있게 될 거야. 니코틴 패치나 껌 같은 보조제를 활용하거나 전문가의 도움을 받는 것도 좋은 방법이고 체중 증가와 변비같은 금단 증상에 대비해야 한다는 점도 잊지 마!"},{"role":"user","content":"담배 말고 전자담배로 바꿀까? \r\n\n"},{"role":"assistant","content":"전자담배 역시 일반 담배와 마찬가지로 유해물질이 포함되어 있어서 안전하다고 볼 수 없어. 오히려 일부 성분은 일반 담배보다 더 많이 검출되기도 했고 배터리 폭발 사고 위험도 존재하지. 비용 면에서도 초기 구입 비용이 비싸고 액상 가격도 만만치 않아서 장기적으로는 경제적이지 않을 수도 있다는 걸 고려해야 할 거야. 물론 개인의 선택이지만 신중하게 결정하는 편이 좋을 듯 싶어."},{"role":"user","content":"지금 담배가 너무 생각나.\r\n마지막으로 하나만 피우고 오는건 어때? \r\n\n"},{"role":"assistant","content":"물론 마지막으로 딱 하나만 피우고 싶은 마음 충분히 이해해. 하지만 지금 당장 유혹을 이기지 못하고 다시 피우게 되면 그동안의 노력이 물거품이 되어버릴지도 몰라. 대신 시원한 물 한잔 마시거나 산책을 하면서 잠시 머리를 식혀보는 건 어떨까? 아니면 양치질을 하거나 손 지압을 하면 어느정도 욕구를 해소할 수 있대. 조금만 더 참고 이겨내면 훨씬 더 건강하고 행복한 삶을 누릴 수 있을테니 힘내보자!"},{"role":"user","content":"술자리에만 가면 담배를 피게 돼. 어떻게 해야 해?\r\n술 마시면 담배가 왜 생각날까?\r\n\n"},{"role":"assistant","content":"둘 다 중추신경계를 자극한다는 공통점이 있거든. 술 마시면서 담배를 피우면 각성 효과가 배가 되기 때문에 술자리에서 유독 담배생각이 간절해지는 거지. 습관화 된 탓도 크고 말이야. 그러니 일단 최대한 술 마시는 횟수를 줄이고 만약 마시게 된다면 물을 자주 마셔서 체내 수분량을 유지하도록 해 봐. 안주로는 비타민C가 풍부한 과일류를 먹는것도 좋고 분위기에 휩쓸려 나도 모르게 담배를 입에 무는 일이 없도록 정신 바짝 차리고 있어야겠지?"},{"role":"user","content":"다른 방법도 추천해줄 수 있어?"},{"role":"assistant","content":"친구나 가족한테 미리 말해두는거지. 내가 담배를 피려고 하면 말려달라고 부탁하면 아무래도 좀 더 자제력을 발휘할 수 있지 않을까? 아예 처음부터 같이 금연을 하자고 꼬셔보는 것도 좋은 방법일테고 말이야. 그래도 정 못 참겠으면 차라리 밖에 나가서 바람을 쐬고 들어오도록 해. 실내보다는 실외가 그나마 덜 해로울 테니까."},{"role":"user","content":"나라에서 지원받을 수 있는 금연 치료 프로그램 종류를 알려줘. \r\n\n"},{"role":"assistant","content":"대표적으로는 보건소에서 운영하는 금연 클리닉이 있어. 상담 서비스 뿐만 아니라 니코틴 패치나 껌 같은 보조제도 제공해주고 6개월 과정을 모두 이수하면 기념품도 준대. 병원에서는 약물 치료를 받을수도 있는데 보험 적용이 되니까 비용 부담도 적은 편이야. 요즘에는 비대면 방식인 온라인 금연 프로그램도 있으니 각자 상황에 맞게 선택하면 되겠지?"},{"role":"user","content":"온라인 금연 프로그램에 대해서 설명해줘"},{"role":"assistant","content":"시간이나 장소에 구애받지 않고 자유롭게 참여할 수 있다는 장점이 제일 크지. 채팅이나 전화상담을 통해 전문가와 실시간으로 소통할 수도 있고 홈페이지에 올라온 자료들을 보면서 스스로 학습할 수도 있어. 출석률이나 금연 일기 작성 여부에 따라 선물도 준다던데? 수료증도 발급되고 말이야. 여러모로 유용한 프로그램이니까 관심 있다면 한번 찾아보도록 해!"},{"role":"user","content":"검색창에 어떻게 검색해야 정보를 얻을 수 있어?"},{"role":"assistant","content":"'보건소 금연 클리닉' 이나 '국가 금연 지원센터' 라고 입력하면 관련 사이트 주소가 뜰 거야. 각 지역별 보건소마다 세부 일정이나 신청 방법등이 조금씩 다를 수 있으니까 거주지 근처 보건소 홈페이지를 방문해 보는걸 추천할게. 모바일 앱스토어나 구글 플레이 스토어 에서 '금연길라잡이' 어플을 다운받는 것도 좋은 방법 중 하나야."}]

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
