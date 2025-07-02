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
phonics/
├── backend/
└── docker-compose.yml(phonics 루트디렉토리에 추가, 아래에 yml 파일 코드 있음.)
```

```yml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGO_URL=mongodb+srv://angkmfirefoxygal:Rose77490801@30days.rtqtg.mongodb.net/?retryWrites=true&w=majority&appName=30days
```

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

### 🙋‍♀️ 문의
BE 팀장 angkmfirefoxygal

