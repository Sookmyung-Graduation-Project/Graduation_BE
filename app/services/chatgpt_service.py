import openai
from typing import Dict, List
import json
import os
from app.core.config import settings
from app.schemas.book_generation import BookGenerationRequest, BookContent


class ChatGPTService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is not set")
        # httpx 클라이언트를 직접 생성하여 프록시 문제 해결
        import httpx
        http_client = httpx.Client()
        self.client = openai.OpenAI(api_key=settings.openai_api_key, http_client=http_client)
        self.model = settings.openai_model
    
    async def generate_story(self, request: BookGenerationRequest) -> BookContent:
        """사용자 입력을 바탕으로 동화를 생성합니다."""
        
        # 개발 환경에서는 Mock 데이터 사용 (환경변수로 제어 가능)
        use_mock = os.getenv("USE_MOCK_STORY", "false").lower() == "true"
        
        if use_mock:
            return self._generate_mock_story(request)
        
        # 프롬프트 생성
        prompt = self._create_story_prompt(request)
        
        try:
            response = await self._call_openai_api(prompt)
            return self._parse_story_response(response)
        except Exception as e:
            # OpenAI 할당량 초과 시 Mock 데이터 반환
            if "insufficient_quota" in str(e) or "429" in str(e):
                print(f"OpenAI 할당량 초과로 Mock 데이터 사용: {str(e)}")
                return self._generate_mock_story(request)
            raise Exception(f"동화 생성 중 오류가 발생했습니다: {str(e)}")
    
    def _generate_mock_story(self, request: BookGenerationRequest) -> BookContent:
        """할당량 초과 시 사용할 Mock 동화 데이터"""
        # 한국어 옵션을 영어로 변환
        animal_map = {
            "곰": "bear", "공룡": "dinosaur", "사자": "lion", "토끼": "rabbit",
            "고양이": "cat", "거북": "turtle", "사슴": "deer", "돼지": "pig",
            "말": "horse", "코끼리": "elephant", "원숭이": "monkey", "강아지": "puppy"
        }
        lesson_map = {
            "우정의 소중함": "the value of friendship",
            "용기와 자신감": "courage and confidence",
            "용서와 이해": "forgiveness and understanding",
            "인내와 겸손": "patience and humility",
            "열린 마음과 배려": "open mind and care",
            "창의성과 상상력": "creativity and imagination",
            "책임감과 신뢰": "responsibility and trust",
            "성실한 노력의 가치": "the value of honest effort",
            "타인에 대한 이해": "understanding others",
            "공평함과 정의": "fairness and justice"
        }
        
        english_animal = animal_map.get(request.animal, request.animal)
        english_lesson = lesson_map.get(request.lesson, request.lesson)
        
        return BookContent(
            title=f"{english_animal.title()} and the {english_lesson.title()}",
            pages=[
                f"Once upon a time, there was a little {english_animal}.",
                f"The {english_animal} lived in a beautiful forest.",
                f"One day, the {english_animal} met a friendly child.",
                f"They became the best of friends.",
                f"The {english_animal} and the child played together.",
                f"They helped each other when they had problems.",
                f"Their friendship grew stronger every day.",
                f"They learned to trust and care for each other.",
                f"Now they are forever friends.",
                f"From this story, we learn about {english_lesson}."
            ],
            summary=f"A story about a {english_animal} and a child learning about {english_lesson}.",
            characters=[english_animal, "child"],
            setting="magical forest"
        )
    
    def _create_story_prompt(self, request: BookGenerationRequest) -> str:
        """동화 생성용 프롬프트를 생성합니다."""
        
        # 한국어 옵션을 영어로 변환
        gender_map = {"남아": "boy", "여아": "girl"}
        age_map = {
            "1세 이하": "under 1 year old",
            "1~2세": "1-2 years old", 
            "3~4세": "3-4 years old",
            "5~6세": "5-6 years old",
            "7~8세": "7-8 years old",
            "9~10세": "9-10 years old"
        }
        animal_map = {
            "곰": "bear", "공룡": "dinosaur", "사자": "lion", "토끼": "rabbit",
            "고양이": "cat", "거북": "turtle", "사슴": "deer", "돼지": "pig",
            "말": "horse", "코끼리": "elephant", "원숭이": "monkey", "강아지": "puppy"
        }
        lesson_map = {
            "우정의 소중함": "the value of friendship",
            "용기와 자신감": "courage and confidence",
            "용서와 이해": "forgiveness and understanding",
            "인내와 겸손": "patience and humility",
            "열린 마음과 배려": "open mind and care",
            "창의성과 상상력": "creativity and imagination",
            "책임감과 신뢰": "responsibility and trust",
            "성실한 노력의 가치": "the value of honest effort",
            "타인에 대한 이해": "understanding others",
            "공평함과 정의": "fairness and justice"
        }
        
        english_gender = gender_map.get(request.gender, request.gender)
        english_age = age_map.get(request.age_group, request.age_group)
        english_animal = animal_map.get(request.animal, request.animal)
        english_lesson = lesson_map.get(request.lesson, request.lesson)
        
        prompt = f"""
You are a children's story writer. Please create a 10-page story that meets the following conditions.

**Target Reader:**
- Gender: {english_gender}
- Age: {english_age}

**Main Character:**
- Animal: {english_animal}

**Lesson/Moral:**
- {english_lesson}

**Requirements:**
1. A story consisting of 10 pages total
2. Each page should be 2-3 sentences
3. Use vocabulary and sentence length appropriate for the age group
4. Incorporate the selected lesson naturally into the story
5. Positive and educational content
6. Include a summary of the lesson in the final page

**Response Format:**
Please respond in the following JSON format:
{{
    "title": "Story Title",
    "pages": [
        "Page 1 content",
        "Page 2 content",
        ...
        "Page 10 content"
    ],
    "summary": "Story summary (2-3 sentences)",
    "characters": ["Main character", "Supporting character 1", "Supporting character 2"],
    "setting": "Background setting (when and where)"
}}

Please create the story:
"""
        return prompt
    
    async def _call_openai_api(self, prompt: str) -> str:
        """OpenAI API를 호출합니다."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 어린이를 위한 동화 작가입니다. 주어진 조건에 맞는 교육적이고 재미있는 동화를 생성해주세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API 호출 실패: {str(e)}")
    
    def _parse_story_response(self, response: str) -> BookContent:
        """OpenAI 응답을 파싱하여 BookContent 객체로 변환합니다."""
        try:
            # JSON 부분만 추출 (```json으로 감싸져 있을 수 있음)
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            # JSON 파싱
            story_data = json.loads(json_str)
            
            return BookContent(
                title=story_data.get("title", "동화"),
                pages=story_data.get("pages", []),
                summary=story_data.get("summary", ""),
                characters=story_data.get("characters", []),
                setting=story_data.get("setting", "")
            )
        except json.JSONDecodeError as e:
            raise Exception(f"동화 응답 파싱 실패: {str(e)}")
        except Exception as e:
            raise Exception(f"동화 데이터 처리 실패: {str(e)}")


# 싱글톤 인스턴스
chatgpt_service = ChatGPTService()
