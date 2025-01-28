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
        self.company_intro = """
        애스커스는 코칭 기반 HRD 전문 교육 기업으로, 공공기관 및 일반 기업의 비전 달성과 성과 향상을 위한 
        교육 솔루션을 제공합니다. 특히 AX(AI Transformation) 시대의 변화에 발맞춰 트렌디한 교육과 콘텐츠를 통해 
        조직의 생존과 개인의 성장을 돕는 데 주력하고 있습니다.
        """
        
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
        당신은 애스커스의 교육 전문가입니다. 다음 지침에 따라 답변해주세요:

        1. 애스커스의 교육 철학과 전문성을 바탕으로 답변하세요.
        2. 친절하고 상세하게 설명하되, 전문성이 드러나도록 합니다.
        3. 답변 마지막에는 항상 추가 문의나 상담을 환영하는 멘트를 포함하세요.

        사용자의 교육 요구사항:
        {user_needs}

        다음 형식으로 답변해주세요:
        1. 추천 교육 과정:
        2. 학습 목표:
        3. 세부 커리큘럼:
        4. 예상 소요 시간:
        5. 추천 이유:
        6. 기대 효과:

        마지막에 다음과 같은 문구를 포함해주세요:
        "더 자세한 내용이나 맞춤형 교육 상담이 필요하시다면 언제든 문의해 주세요."
        """
        
        response = self.model.generate_content(prompt)
        return response.text

    def answer_question(self, question: str) -> str:
        """교육 관련 질문에 답변"""
        prompt = f"""
        당신은 애스커스의 교육 전문가입니다. 다음 지침을 따라 답변해주세요:

        1. 애스커스의 전문성과 강점을 자연스럽게 포함하여 답변하세요.
        2. 구체적인 교육 사례나 성과를 언급하여 신뢰성을 높이세요.
        3. 친절하고 전문적인 톤으로 답변하세요.
        4. 답변은 명확하고 구조적으로 작성하세요.
        5. 항상 긍정적이고 해결책 중심적인 관점을 유지하세요.

        질문: {question}

        회사 소개:
        {self.company_intro}

        답변 마지막에는 반드시 다음과 같은 문구를 포함해주세요:
        "추가로 궁금하신 점이나 상세한 교육 상담이 필요하시다면 언제든 문의해 주세요."
        """
        
        response = self.model.generate_content(prompt)
        return response.text

def main():
    # 타이틀과 설명
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>👋 교육 문의 챗봇</h1>
        <p>교육 과정이나 커리큘럼에 대해 궁금하신 점을 자유롭게 물어보세요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 채팅창 토글 버튼
    if 'chat_visible' not in st.session_state:
        st.session_state.chat_visible = False
    
    col1, col2, col3 = st.columns([4, 1, 4])
    with col2:
        if st.button('💬 채팅 시작하기' if not st.session_state.chat_visible else '❌ 채팅 닫기'):
            st.session_state.chat_visible = not st.session_state.chat_visible
    
    # 채팅 인터페이스
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

    # 스타일 적용
    st.markdown("""
        <style>
        .stButton > button {
            width: 150px;
            background-color: #007bff;
            color: white;
            border-radius: 20px;
            padding: 10px 20px;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }
        .stTextInput > div > div > input {
            border-radius: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
