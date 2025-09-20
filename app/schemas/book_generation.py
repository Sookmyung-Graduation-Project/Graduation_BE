from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum


class Gender(str, Enum):
    MALE = "남아"
    FEMALE = "여아"


class AgeGroup(str, Enum):
    UNDER_1 = "1세 이하"
    AGE_1_2 = "1~2세"
    AGE_3_4 = "3~4세"
    AGE_5_6 = "5~6세"
    AGE_7_8 = "7~8세"
    AGE_9_10 = "9~10세"


class Lesson(str, Enum):
    FRIENDSHIP = "우정의 소중함"
    COURAGE_CONFIDENCE = "용기와 자신감"
    FORGIVENESS_UNDERSTANDING = "용서와 이해"
    PATIENCE_HUMILITY = "인내와 겸손"
    OPEN_MIND_CARE = "열린 마음과 배려"
    CREATIVITY_IMAGINATION = "창의성과 상상력"
    RESPONSIBILITY_TRUST = "책임감과 신뢰"
    HONEST_EFFORT = "성실한 노력의 가치"
    UNDERSTANDING_OTHERS = "타인에 대한 이해"
    FAIRNESS_JUSTICE = "공평함과 정의"


class Animal(str, Enum):
    BEAR = "곰"
    DINOSAUR = "공룡"
    LION = "사자"
    RABBIT = "토끼"
    CAT = "고양이"
    TURTLE = "거북"
    DEER = "사슴"
    PIG = "돼지"
    HORSE = "말"
    ELEPHANT = "코끼리"
    MONKEY = "원숭이"
    DOG = "강아지"


class VoiceOption(str, Enum):
    GUARDIAN_1 = "보호자1(기본)"
    GUARDIAN_2 = "보호자2"
    GUARDIAN_3 = "보호자3"


class BookGenerationRequest(BaseModel):
    """책 생성 요청 스키마"""
    gender: Gender
    age_group: AgeGroup
    lesson: Lesson
    animal: Animal
    voice_option: VoiceOption
    
    class Config:
        use_enum_values = True


class BookGenerationResponse(BaseModel):
    """책 생성 응답 스키마"""
    success: bool
    message: str
    book_id: Optional[str] = None
    story_content: Optional[str] = None
    error: Optional[str] = None


class BookContent(BaseModel):
    """생성된 책 내용 스키마"""
    title: str
    pages: list[str]  # 10페이지 분량
    summary: str
    characters: list[str]
    setting: str
