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

class EducationChatbot:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.course_data = self._load_course_data()
        
    def _load_course_data(self):
        return {
            "AI_BASIC": {
                "name": "생성형 AI 이해와 활용 (AI 기초)",
                "description": "생성형 AI의 기본 원리를 이해하고, 최신 AI 기술 동향을 파악합니다.",
                "topics": ["프롬프트 엔지니어링", "업무 적합 AI 선택", "AI 커뮤니케이션"]
            },
            "AI_ADVANCED": {
                "name": "업무 능력 향상 with 생성형 AI",
                "description": "실제 업무에 생성형 AI를 활용하여 생산성을 높이는 방법을 배웁니다.",
                "topics": ["AI 비서 활용", "문서 작성", "챗봇 제작"]
            }
        }

    def generate_response(self, user_input):
        if "과정" in user_input or "커리큘럼" in user_input:
            prompt = f"""
            당신은 애스커스의 교육 전문가입니다. 다음 요구사항에 맞는 교육 과정을 추천해주세요:
            {user_input}
            """
        else:
            prompt = f"""
            당신은 애스커스의 교육 전문가입니다. 다음 질문에 친절하게 답변해주세요:
            {user_input}
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요."

def main():
    st.markdown("교육 과정이나 커리큘럼에 대해 궁금하신 점을 자유롭게 물어보세요.")
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = EducationChatbot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"👤: {message['content']}")
        else:
            st.write(f"🤖: {message['content']}")

    user_input = st.text_input("")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = st.session_state.chatbot.generate_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
