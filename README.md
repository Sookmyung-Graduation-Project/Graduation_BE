# 🐳 Backend FastAPI + MongoDB 실행 가이드

## ✅ 프로젝트 개요

* **Backend Framework:** FastAPI
* **DB:** MongoDB Atlas
* **Containerization:** Docker, Docker Compose

* [erd 링크 🔗](https://dbdiagram.io/d/68649308f413ba3508d03220)
![alt text](image.png)
---

## 📁 Directory 구조

```bash
backend/
   ├── .env
   ├── Dockerfile
   ├── main.py
   ├── docker-compose.yml
   └── requirements.txt

```

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
JWT_SECRET_KEY="18aa1bc885f3ae5e2522f68fb57811daa299260d07889e1c42ef3e0f50048db3"
ELEVENLABS_API_KEY="sk_57c2e5bf0bdfcf05c6ce507c9df2c064c5e6839201855d80"
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

✅ **요약**

1. 루트 디렉토리에 `docker-compose.yml` 작성
2. backend 레포 clone → backend 폴더에 배치
3. .env 수정
4. `docker compose up --build` 실행으로 FastAPI + MongoDB 서버 구동 완료

필요하면 FE + BE docker-compose 통합 가이드도 이어서 작성해줄 수 있으니 알려주세요!


---- 
## Project Structure
```bash

Graduation_BE/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── voice.py
│   │   ├── attendance.py
│   │   ├── user_favorite_books.py
│   │   └── user_recent_viewed_books.py
│   ├── db.py
│   └── main.py
├── venv/
├── .env
├── requirements.txt
├── Dockerfile
└── docker-compose.yml


```

- `main.py` : FastAPI() 생성, 필요한 router 관리
- `core/` : 공통 설정, 보안관련로직, 인증 헬퍼 함수
- `db/` : DB연결, 세션
- `models/`: SQLAlchemy ORM 모델
- `chemas/`: Pydantic 데이터 검증 / 직렬화 모델
- `crud/` : DB Access 로직, 캡슐화
- `api/`: FastAPI 라우팅 코드, 엔드포인트(Controller)집합
- `tests/` : pytest 기반 테스트
