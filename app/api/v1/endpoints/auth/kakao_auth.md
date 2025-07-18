# 전체 흐름 요약
1. **모바일 앱 (Flutter)**
      - 카카오 SDK를 이용해 사용자 로그인 진행

      - 로그인 성공 시, access token 혹은 **id token (OpenID Connect 사용 시)**을 얻음

      - 이 토큰을 FastAPI 백엔드에 전달

2. **FastAPI 백엔드**
      - 받은 토큰을 Kakao 서버에 검증 요청

      - 토큰이 유효하다면, 사용자 정보를 받아오고, 자체적으로 JWT 발급 등 로그인 처리

## 3. flow
```
[Flutter 앱]
   |
   |---> 카카오 SDK 로그인
   |         (KakaoTalk 앱 / 웹뷰 / 브라우저 로그인)
   |
   |---> access token 획득
   |
   |---> access token FastAPI로 전송 (/auth/kakao)
               ↓
         [FastAPI 서버]
   |---> access token 검증 요청 (카카오 REST API: /v2/user/me)
   |
   |---> 유저 정보 응답 받음
   |
   |---> 로컬 DB 사용자 등록/로그인 처리
   |
   |---> 자체 JWT 발급 및 앱에 전달

```

## 4. 현재 시점에서 access_token을 직접 넣어서 확인