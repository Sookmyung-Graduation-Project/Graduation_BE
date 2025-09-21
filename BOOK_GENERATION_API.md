# 📚 책 생성 API 문서

## 기본 정보
- **Base URL**: `http://localhost:8000`
- **인증**: JWT Bearer Token 필요 (일부 엔드포인트 제외)

---

## 1. 동화 생성

### `POST /book_generation/generate`

사용자 입력에 따라 영어 동화를 생성합니다.

#### Headers
```
Content-Type: application/json
Authorization: Bearer {JWT_TOKEN}
```

#### Request Body
```json
{
  "gender": "남아",
  "age_group": "5~6세",
  "lesson": "우정의 소중함",
  "animal": "토끼",
  "voice_option": "보호자1(기본)"
}
```

#### Response (Success - 200)
```json
{
  "success": true,
  "message": "동화가 성공적으로 생성되었습니다.",
  "book_id": "68cea84883bd2463a92169f2",
  "story_content": "제목: Rabbit and the Value of Friendship\n\n요약: A story about a rabbit and a child learning about the value of friendship.\n\n등장인물: rabbit, child\n\n배경: magical forest\n\n동화 내용:\n\n페이지 1: Once upon a time, there was a little rabbit...\n페이지 2: The rabbit lived in a beautiful forest...\n..."
}
```

#### Response (Error - 500)
```json
{
  "success": false,
  "message": "동화 생성 중 오류가 발생했습니다.",
  "error": "Error details"
}
```

---

## 2. 사용자 책 목록 조회

### `GET /book_generation/books`

사용자가 생성한 모든 책 목록을 조회합니다.

#### Headers
```
Authorization: Bearer {JWT_TOKEN}
```

#### Response (Success - 200)
```json
[
  {
    "id": "68cea84883bd2463a92169f2",
    "title": "Rabbit and the Value of Friendship",
    "author": "AI 동화 작가",
    "age_group": "5~6세",
    "lesson": "우정의 소중함",
    "animal": "토끼",
    "summary": "A story about a rabbit and a child learning about the value of friendship.",
    "created_at": "2024-01-15T10:30:00.000Z",
    "page_count": 10
  }
]
```

---

## 3. 특정 책 상세 조회

### `GET /book_generation/books/{book_id}`

특정 책의 상세 정보를 조회합니다.

#### Headers
```
Authorization: Bearer {JWT_TOKEN}
```

#### Path Parameters
- `book_id`: 책의 고유 ID

#### Response (Success - 200)
```json
{
  "id": "68cea84883bd2463a92169f2",
  "title": "Rabbit and the Value of Friendship",
  "author": "AI 동화 작가",
  "gender": "남아",
  "age_group": "5~6세",
  "lesson": "우정의 소중함",
  "animal": "토끼",
  "voice_option": "보호자1(기본)",
  "pages": [
    "Once upon a time, there was a little rabbit.",
    "The rabbit lived in a beautiful forest.",
    "One day, the rabbit met a friendly child.",
    "They became the best of friends.",
    "The rabbit and the child played together.",
    "They helped each other when they had problems.",
    "Their friendship grew stronger every day.",
    "They learned to trust and care for each other.",
    "Now they are forever friends.",
    "From this story, we learn about the value of friendship."
  ],
  "summary": "A story about a rabbit and a child learning about the value of friendship.",
  "characters": ["rabbit", "child"],
  "setting": "magical forest",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

#### Response (Error - 404)
```json
{
  "detail": "책을 찾을 수 없습니다."
}
```

---

## 사용 가능한 옵션 상세

### 성별 (Gender)
- `남아`: Boy
- `여아`: Girl

### 연령대 (Age Group)
- `1세 이하`: Under 1 year old
- `1~2세`: 1-2 years old
- `3~4세`: 3-4 years old
- `5~6세`: 5-6 years old
- `7~8세`: 7-8 years old
- `9~10세`: 9-10 years old

### 교훈 (Lesson)
- `우정의 소중함`: The value of friendship
- `용기와 자신감`: Courage and confidence
- `용서와 이해`: Forgiveness and understanding
- `인내와 겸손`: Patience and humility
- `열린 마음과 배려`: Open mind and care
- `창의성과 상상력`: Creativity and imagination
- `책임감과 신뢰`: Responsibility and trust
- `성실한 노력의 가치`: The value of honest effort
- `타인에 대한 이해`: Understanding others
- `공평함과 정의`: Fairness and justice

### 동물 (Animal)
- `곰`: Bear
- `공룡`: Dinosaur
- `사자`: Lion
- `토끼`: Rabbit
- `고양이`: Cat
- `거북`: Turtle
- `사슴`: Deer
- `돼지`: Pig
- `말`: Horse
- `코끼리`: Elephant
- `원숭이`: Monkey
- `강아지`: Puppy

### 목소리 옵션 (Voice Option)
- `보호자1(기본)`: Guardian 1 (Default)
- `보호자2`: Guardian 2
- `보호자3`: Guardian 3

---

## 프론트엔드 구현 가이드

### 1. 동화 생성
```javascript
const generateStory = async (userInput) => {
  const response = await fetch('/book_generation/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${jwtToken}`
    },
    body: JSON.stringify(userInput)
  });
  return response.json();
};
```

### 2. 책 목록 조회
```javascript
const getUserBooks = async () => {
  const response = await fetch('/book_generation/books', {
    headers: {
      'Authorization': `Bearer ${jwtToken}`
    }
  });
  return response.json();
};
```

### 3. 책 상세 조회
```javascript
const getBookDetail = async (bookId) => {
  const response = await fetch(`/book_generation/books/${bookId}`, {
    headers: {
      'Authorization': `Bearer ${jwtToken}`
    }
  });
  return response.json();
};
```

---

## 주의사항

1. **인증**: 대부분의 엔드포인트는 JWT 토큰이 필요합니다.
2. **영어 동화**: 생성되는 동화는 모두 영어로 작성됩니다.
3. **페이지 구조**: 각 동화는 10페이지로 구성됩니다.
4. **에러 처리**: API 호출 시 적절한 에러 처리를 구현해주세요.
5. **로딩 상태**: 동화 생성은 시간이 걸릴 수 있으므로 로딩 상태를 표시해주세요.

