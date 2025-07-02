# 1. Python 3.10 이미지 기반
FROM python:3.10

# 2. 컨테이너 작업 디렉토리 설정
WORKDIR /app

# 3. requirements.txt 복사 후 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 전체 소스 코드 복사
COPY . /app

# 5. uvicorn으로 FastAPI 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
