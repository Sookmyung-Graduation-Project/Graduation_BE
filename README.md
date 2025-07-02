# 🐳 Backend FastAPI + MongoDB 실행 가이드

## ✅ 프로젝트 개요

- **Backend Framework:** FastAPI
- **DB:** MongoDB Atlas
- **Containerization:** Docker, Docker Compose

---

## 📁 Directory 구조

```bash

backend/
├── .env
├── Dockerfile
├── main.py
├── requirements.txt
└── venv/ (로컬 가상환경, push 제외)
```



---

## ⚠️ 사전 설치

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치  
  - Windows는 WSL2 권장
- Git

---

## 🔧 1. 레포 클론

```bash
git clone [BE 레포 URL]
cd backend
```

## 🔧 2. .env 설정
.env 파일을 팀에서 공유된 값으로 수정

```env
MONGO_URL = "mongodb+srv://angkmfirefoxygal:Rose77490801@30days.rtqtg.mongodb.net/?retryWrites=true&w=majority&appName=30days"
```

## 🔧 3. Docker Compose 실행

```bash
docker compose up --build
```

첫 실행은 이미지 빌드로 시간이 소요될 수 있음 

이후엔 docker compose up만 입력해도 실행 가능


## ✅ 4. FastAPI 서버 접속 확인
http://localhost:8000 접속

/test API 호출 시 MongoDB 연결 확인 가능

## 🛑 5. 서버 종료
터미널에서 CTRL + C
또는 별도 터미널에서:

```bash
docker compose down
```

### 📌 Trouble Shooting
문제	해결 방법
git 커밋 시 Author identity unknown	git config --global user.name "Your Name" &nbsp;
git config --global user.email "your_email@example.com" &nbsp;
docker compose 실행 권한 오류	VS Code 또는 PowerShell을 관리자 권한으로 실행 &nbsp;
connection refused	.env의 MONGO_URL, Atlas IP whitelist 확인 &nbsp;

### 🙋‍♀️ 문의
BE 팀장 angkmfirefoxygal

