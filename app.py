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
        애스커스는 코칭 기반 HRD 전문 교육 기업입니다.
        
        주요 특징:
        - 공공기관 및 기업 대상 교육 솔루션 제공
        - 창의적 문제해결과 코칭 기반 교육
        - 계층별 맞춤형 교육 및 워크숍
        - AI 트랜스포메이션 교육 전문
        - 98% 교육 만족도와 4.93/5점의 평가
        
        주요 교육 프로그램:
        1. AI 및 데이터 리터러시 교육
        2. 소통공감 리버스 멘토링
        3. 변화대응 셀프리더십
        4. 강사역량 강화과정
        
        교육 운영 프로세스:
        1. 요구사항 분석
        2. 맞춤형 프로그램 개발
        3. 전문적 교육 운영
        4. 체계적 사후 관리
        """

    def generate_response(self, user_input):
        for attempt in range(MAX_RETRIES):
            try:
                prompt = f"""
                다음 컨텍스트를 바탕으로 질문에 답변해주세요. 
                답변은 3-4문장으로 간단명료하게 작성하되, 
                애스커스의 전문성과 강점이 잘 드러나도록 해주세요.

                컨텍스트:
                {self.context}

                질문: {user_input}
                """
                
                response = self.model.generate_content(prompt)
                return response.text.strip()
                
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    return "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
                time.sleep(RETRY_DELAY)

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

    # 이전 메시지들 표시
    for message in st.session_state.messages:
        role = "👤" if message["role"] == "user" else "🎓"
        st.write(f"{role}: {message['content']}")

    # 사용자 입력
    user_input = st.text_input("질문을 입력해주세요", key="user_input")
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 생각하는 중 표시
        with st.spinner("답변을 생성하고 있습니다..."):
            response = st.session_state.bot.generate_response(user_input)
        
        # 봇 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 입력창 초기화를 위한 rerun
        st.experimental_rerun()

if __name__ == "__main__":
    main()
