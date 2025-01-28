import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import time

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MAX_RETRIES = 3
RETRY_DELAY = 2

class AskusEducationBot:
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        self.context = self._load_company_context()
    
    def _load_company_context(self):
        return """
        애스커스는 코칭 기반 HRD 전문 교육 기업으로, 공공기관 및 일반 기업의 비전 달성과 성과 향상을 위한 교육 솔루션을 제공합니다.

        전문성과 신뢰성:
        - 교육 운영 전문가, 컨설턴트, 전문 강사 등 다양한 분야의 전문가 보유
        - KT, CJ, 신세계 등 국내 유수 기업에서의 다년간 교육 경험
        - 도쿄일렉트론코리아, 사천시청, 한전원자력연료 등 성공적인 교육 수행
        - 98% 교육 만족도와 4.93/5점의 평가

        주요 교육 프로그램:
        - 기업 교육: 맞춤형 AX/DX 및 HRD 역량 강화
        - 공공기관 교육: 행정 선진화 특화 교육
        - 경영자 교육: 글로벌 리더십 확보
        - 직급별 맞춤 교육: 신입사원부터 임원까지

        특화된 교육 과정:
        1. 생성형 AI 활용
           - 프롬프트 엔지니어링
           - M365 생산성 향상
           - AI 챗봇 제작
        2. 데이터 리터러시
           - 공공데이터 활용
           - 엑셀/파이썬 데이터 분석
        3. 직급별 역량 강화
           - 신입사원 온보딩
           - 과장급 리스킬링
           - 임원급 리더십
        4. 팀빌딩/힐링 프로그램
           - 레이저 서바이벌
           - 명랑운동회
           - 클래식 음악 여행
           - 스트레스 관리

        교육 운영 프로세스:
        1. 맞춤형 요구 분석
        2. 전문적 프로그램 개발
        3. 체계적 교육 운영
        4. 철저한 사후 관리
        """

    def generate_response(self, user_input):
        for attempt in range(MAX_RETRIES):
            try:
                prompt = f"""
                당신은 애스커스의 수석 교육 컨설턴트입니다. 다음 지침에 따라 답변해주세요:

                1. 상세하고 친절한 답변을 제공하되, 전문성이 드러나도록 합니다.
                2. 애스커스의 강점과 차별화된 특징을 자연스럽게 언급합니다.
                3. 관련된 교육 과정이나 프로그램을 구체적으로 추천합니다.
                4. 높은 교육 만족도(98%)와 평가 점수(4.93/5)를 적절히 활용합니다.
                5. 답변 마지막에는 항상 교육 문의나 상담을 권유하는 멘트를 포함합니다.

                컨텍스트:
                {self.context}

                질문: {user_input}

                답변 형식:
                1. 질문에 대한 직접적인 답변
                2. 관련 교육 프로그램 추천
                3. 애스커스의 강점 언급
                4. 교육 문의 안내

                답변 마지막에는 반드시 다음과 같은 문구를 포함해주세요:
                "더 자세한 내용이나 맞춤형 교육 상담이 필요하시다면 언제든 문의해 주세요."
                """
                
                response = self.model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    return "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
                time.sleep(RETRY_DELAY)

def clear_text():
    st.session_state["user_input"] = ""

def main():
    st.markdown("<h3>애스커스 교육 상담 챗봇</h3>", unsafe_allow_html=True)
    
    if 'bot' not in st.session_state:
        try:
            st.session_state.bot = AskusEducationBot()
        except ValueError as e:
            st.error(str(e))
            return
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

    # 이전 메시지들 표시
    for message in st.session_state.messages:
        role = "👤" if message["role"] == "user" else "🎓"
        st.write(f"{role}: {message['content']}")

    # 사용자 입력 - 매번 새로운 key 사용
    user_input = st.text_input("질문을 입력해주세요", key=f"user_input_{st.session_state.input_key}")
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 생각하는 중 표시
        with st.spinner("답변을 생성하고 있습니다..."):
            response = st.session_state.bot.generate_response(user_input)
        
        # 봇 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 입력창 초기화를 위해 key 증가
        st.session_state.input_key += 1
        st.experimental_rerun()

if __name__ == "__main__":
    main()
