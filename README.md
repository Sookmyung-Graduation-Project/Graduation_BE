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

# ChatGPT API 설정 (책 생성 기능용)
OPENAI_API_KEY="your-openai-api-key"
OPENAI_MODEL="gpt-3.5-turbo"
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

---

## 📚 책 생성 기능 API

### 책 생성 프로세스

사용자가 4단계 입력을 통해 맞춤형 동화를 생성할 수 있습니다:

1. **성별과 연령대 선택**
2. **교훈 선택** (10가지 중 선택)
3. **주인공 동물 선택** (12가지 중 선택)
4. **목소리 선택** (보호자1/2/3)

### API 엔드포인트

#### 1. 동화 생성
```http
POST /api/v1/books/generate
```

**요청 본문:**
```json
{
  "gender": "남아",
  "age_group": "5~6세",
  "lesson": "우정의 소중함",
  "animal": "토끼",
  "voice_option": "보호자1(기본)"
}
```

**응답:**
```json
{
  "success": true,
  "message": "동화가 성공적으로 생성되었습니다.",
  "book_id": "64f8a1b2c3d4e5f6a7b8c9d0",
  "story_content": "제목: 토끼의 우정...\n\n요약: ...\n\n동화 내용:\n페이지 1: ..."
}
```

#### 2. 사용자 책 목록 조회
```http
GET /api/v1/books/books
```

#### 3. 특정 책 상세 조회
```http
GET /api/v1/books/books/{book_id}
```

#### 4. 생성 옵션 조회
```http
GET /api/v1/books/options
```

### 사용 가능한 옵션들

- **성별**: 남아, 여아
- **연령대**: 1세 이하, 1~2세, 3~4세, 5~6세, 7~8세, 9~10세
- **교훈**: 우정의 소중함, 용기와 자신감, 용서와 이해, 인내와 겸손, 열린 마음과 배려, 창의성과 상상력, 책임감과 신뢰, 성실한 노력의 가치, 타인에 대한 이해, 공평함과 정의
- **동물**: 곰, 공룡, 사자, 토끼, 고양이, 거북, 사슴, 돼지, 말, 코끼리, 원숭이, 강아지
- **목소리**: 보호자1(기본), 보호자2, 보호자3
