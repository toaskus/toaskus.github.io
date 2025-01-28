import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("GOOGLE_API_KEY가 설정되지 않았습니다.")
    st.stop()

class AskusEducationBot:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.company_info = self._load_company_info()
        
    def _load_company_info(self):
        # 회사 소개 파일에서 관련 내용 참조
        return {
            "company_intro": """
            애스커스는 코칭 기반 HRD 전문 교육 기업으로, 공공기관 및 일반 기업의 비전 달성과 
            성과 향상을 위한 교육 솔루션을 제공합니다. 창의적 문제 해결과 코칭을 바탕으로 
            계층별 역량 교육, 워크숍, 커뮤니티 운영, 컨설팅 등 다양한 사업을 수행하고 있습니다.
            """,
            "expertise": [
                "다양한 분야의 전문가 보유",
                "검증된 교육 실적",
                "높은 고객 신뢰도",
                "맞춤형 교육 제공",
                "실제 업무 적용 가능한 교육"
            ],
            "courses": {
                "ai_basic": "생성형 AI 이해와 활용 (AI 기초)",
                "ai_advanced": "업무 능력 향상 with 생성형 AI",
                "ai_chatgpt": "인공지능 이해 기초 - 생성형 AI와 ChatGPT 활용"
            }
        }

    def generate_response(self, user_input):
        # 기본 프롬프트 설정
        base_prompt = """
        당신은 애스커스의 교육 전문가입니다. 다음 가이드라인에 따라 답변해주세요:
        1. 간결하고 명확하게 답변
        2. 애스커스의 전문성과 강점 강조
        3. 실제 교육 사례나 성과 언급
        4. 친절하고 전문적인 톤 유지
        5. 필요시 관련 교육과정 추천
        
        질문: {question}
        """
        
        try:
            # 컨텍스트를 포함한 프롬프트 생성
            prompt = base_prompt.format(question=user_input)
            response = self.model.generate_content(prompt)
            return self._format_response(response.text)
        except Exception as e:
            return "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."
    
    def _format_response(self, response):
        # 답변 포맷팅 및 정리
        return response.strip()

def main():
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            background-color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if 'bot' not in st.session_state:
        st.session_state.bot = AskusEducationBot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role = "👤" if message["role"] == "user" else "🎓"
        st.write(f"{role}: {message['content']}")

    user_input = st.text_input("질문을 입력해주세요", key="user_input")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = st.session_state.bot.generate_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
