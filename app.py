import os
from dotenv import load_dotenv
import streamlit as st
from typing import Dict, List

load_dotenv()

# Gemini API 설정
import google.generativeai as genai

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
        
    def _load_course_data(self) -> Dict:
        """교육 과정 데이터 로드"""
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
            },
            # ... 다른 과정들 추가
        }

    def generate_curriculum(self, user_needs: str) -> str:
        """사용자 요구사항에 맞는 커리큘럼 생성"""
        prompt = f"""
        다음은 사용자의 교육 요구사항입니다:
        {user_needs}
        
        애스커스의 교육 과정을 기반으로 맞춤형 커리큘럼을 추천해주세요.
        다음 형식으로 응답해주세요:
        1. 추천 교육 과정:
        2. 학습 목표:
        3. 세부 커리큘럼:
        4. 예상 소요 시간:
        5. 추천 이유:
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def answer_question(self, question: str) -> str:
        """교육 관련 질문에 답변"""
        prompt = f"""
        다음은 교육 과정에 대한 질문입니다:
        {question}
        
        애스커스의 교육 전문가로서 답변해주세요.
        """
        
        response = self.model.generate_content(prompt)
        return response.text

def main():
    # 채팅 버튼 (우측 하단에 고정)
    st.markdown("""
        <div class="chat-button-container">
            <button id="chat-button" class="chat-button">
                <i class="fas fa-comments"></i>
            </button>
        </div>
        
        <style>
        .chat-button-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        .chat-button {
            width: 60px;
            height: 60px;
            border-radius: 30px;
            background-color: #007bff;
            color: white;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            transition: all 0.3s ease;
        }
        
        .chat-button:hover {
            background-color: #0056b3;
            transform: scale(1.05);
        }
        
        @media (max-width: 768px) {
            .chat-button {
                width: 50px;
                height: 50px;
                font-size: 20px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 채팅 인터페이스
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = False
        
    # JavaScript로 버튼 클릭 이벤트 처리
    st.markdown("""
        <script>
            document.getElementById('chat-button').addEventListener('click', function() {
                window.parent.postMessage({type: 'toggleChat'}, '*');
            });
        </script>
    """, unsafe_allow_html=True)
    
    if st.session_state.chat_visible:
        chatbot = EducationChatbot()
        
        # 세션 상태 초기화
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # 채팅 히스토리 표시
        for chat in st.session_state.chat_history:
            st.markdown(f"**🤖**: {chat['bot']}")
            st.markdown("---")
        
        # 입력창
        user_input = st.text_input("질문을 입력해주세요", key="user_input")
        
        if user_input:
            try:
                if "과정" in user_input or "커리큘럼" in user_input:
                    response = chatbot.generate_curriculum(user_input)
                else:
                    response = chatbot.answer_question(user_input)
                
                if response and not response.startswith("죄송합니다"):
                    st.session_state.chat_history.append({"bot": response})
                    st.rerun()
                else:
                    st.error("죄송합니다. 응답을 생성하는 데 문제가 발생했습니다. 다시 시도해 주세요.")
            
            except Exception as e:
                st.error("죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

if __name__ == "__main__":
    main()
