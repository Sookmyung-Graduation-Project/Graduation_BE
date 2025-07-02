# 🐳 Backend FastAPI + MongoDB 실행 가이드

## ✅ 프로젝트 개요

* **Backend Framework:** FastAPI
* **DB:** MongoDB Atlas
* **Containerization:** Docker, Docker Compose

---

## 📁 Directory 구조

```bash
phonics/
├── backend/
│   ├── .env
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── docker-compose.yml
```

* `docker-compose.yml` 파일은 **phonics 루트 디렉토리**에 위치해야 합니다.
* `backend/` 폴더에는 BE 레포에서 clone 받은 파일들이 포함됩니다.

---

## ⚠️ 사전 설치

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치

  * Windows는 WSL2 권장
* Git

---

## 🔧 1. 레포 클론

```bash
git clone [BE 레포 URL] backend
cd backend
```

---

## 🔧 2. .env 설정

`.env` 파일을 팀에서 공유된 값으로 수정합니다.

```env
MONGO_URL=mongodb+srv://angkmfirefoxygal:Rose77490801@30days.rtqtg.mongodb.net/?retryWrites=true&w=majority&appName=30days
```

---

## 🔧 3. docker-compose.yml 작성

`phonics/docker-compose.yml` 파일 내용:

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGO_URL=mongodb+srv://angkmfirefoxygal:Rose77490801@30days.rtqtg.mongodb.net/?retryWrites=true&w=majority&appName=30days
```

---

## 🔧 4. Docker Compose 실행

루트 디렉토리(`phonics/`)에서 아래 명령어 실행:

```bash
docker compose up --build
```

* 첫 실행은 이미지 빌드로 시간이 소요될 수 있습니다.
* 이후에는 `docker compose up` 만 입력해도 실행 가능합니다.

---

## ✅ 5. FastAPI 서버 접속 확인

* [http://localhost:8000](http://localhost:8000) 접속
* `/test` API 호출 시 MongoDB 연결 확인 가능

---

## 🛑 6. 서버 종료

터미널에서 `CTRL + C`
또는 별도 터미널에서 아래 명령어 실행:

```bash
docker compose down
```

---

## 🙋‍♀️ 문의

BE 팀장 **angkmfirefoxygal**

---

✅ **요약**

1. phonics 루트 디렉토리에 `docker-compose.yml` 작성
2. backend 레포 clone → backend 폴더에 배치
3. .env 수정
4. `docker compose up --build` 실행으로 FastAPI + MongoDB 서버 구동 완료

필요하면 FE + BE docker-compose 통합 가이드도 이어서 작성해줄 수 있으니 알려주세요!
