
# 🐍 FastAPI + MySQL 사용자 관리 프로젝트

## 📌 소개
이 프로젝트는 Python을 이용하여 사용자 정보(CRUD)를 MySQL DB와 연동해 관리하는 API입니다.  
FastAPI, SQLAlchemy, dotenv를 활용하여 모듈화된 백엔드를 구현했습니다.

## 🔧 기술 스택
- FastAPI
- MySQL
- SQLAlchemy
- Python dotenv

## 📁 주요 파일 설명
| 파일명 | 설명 |
|--------|------|
| `main.py` | CLI 기반 사용자 관리 프로그램 |
| `main_refactoring.py` | FastAPI + DB 커넥션 직접 사용 |
| `main_refactoring_final.py` | FastAPI + SQLAlchemy ORM 완성 |
| `models.py` | 사용자 테이블 정의 |
| `db.py` | DB 연결 및 세션 구성 |

## ▶️ 실행 방법
1. `.env` 파일에 DB 접속 정보를 입력
2. `requirements.txt` 설치  
```bash
pip install -r requirements.txt
```
3. FastAPI 실행  
```bash
uvicorn main_refactoring_final:app --reload
```

## 📮 API 엔드포인트
| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/users` | 사용자 전체 조회 |
| POST | `/users` | 사용자 추가 |
| PUT | `/users/{username}` | 사용자 수정 |
| DELETE | `/users/{username}` | 사용자 삭제 |
