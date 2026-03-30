# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Jekyll 기반 개인 블로그/교육 사이트 (https://toaskus.github.io). "애스커스(Askus)" 코칭 기반 HRD·기업교육 조직의 웹사이트로, Minimal Mistakes 테마(v4.26.2, mint 스킨)를 사용한다. Streamlit 기반 AI 챗봇(Google Gemini)이 iframe으로 통합되어 있다.

## Build & Development

```bash
# Jekyll 로컬 서버 실행
bundle install
bundle exec jekyll serve

# Streamlit 챗봇 로컬 실행
pip install -r requirements.txt
streamlit run app.py

# JavaScript 압축 (Rakefile)
bundle exec rake js
```

GitHub Pages로 자동 배포된다 (master 브랜치 push 시).

## Architecture

- **Jekyll 정적 사이트** + **Streamlit Python 챗봇** 하이브리드 구조
- 테마: Minimal Mistakes (gem 기반, `_sass/minimal-mistakes/`에 SCSS 소스)
- 챗봇: `app.py`(AskusEducationBot 클래스, Gemini Pro) → Streamlit Cloud 배포 → `_includes/chatbot.html`에서 iframe 임베드
- 모든 콘텐츠는 한국어

## Key Configuration

| 파일 | 역할 |
|------|------|
| `_config.yml` | Jekyll 설정 (사이트 메타, 플러그인, 댓글, 분석) |
| `_data/navigation.yml` | 메인 메뉴 (Category, Tag, Search) |
| `assets/css/main.scss` | CSS 진입점 + 챗봇 위젯 커스텀 스타일 |
| `app.py` | Streamlit 챗봇 앱 (Gemini API) |
| `.env` | Google API 키 (커밋 주의) |

## Post Convention

`_posts/` 디렉토리에 `YYYY-MM-DD-##.md` 형식. 프론트매터:

```yaml
layout: single
title: "제목"
categories: Operation
tags: [태그]
toc: true
toc_sticky: true
toc_label: "목차"
author_profile: true
```

YouTube 영상 삽입: `{% include video id="VIDEO_ID" provider="youtube" %}`

## Git

- 브랜치: `master`
- 리모트: `https://github.com/toaskus/toaskus.github.io.git`
- 커밋 메시지: 한국어 사용
- user.name: `toaskus`, user.email: `mission7777@hanmail.net`
