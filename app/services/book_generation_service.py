from typing import Optional
from beanie import PydanticObjectId
from app.models.book import Book
from app.schemas.book_generation import BookGenerationRequest, BookGenerationResponse, BookContent
from app.services.chatgpt_service import chatgpt_service
import logging

logger = logging.getLogger(__name__)


class BookGenerationService:
    def __init__(self):
        self.chatgpt_service = chatgpt_service
    
    async def generate_book(self, user_id: PydanticObjectId, request: BookGenerationRequest) -> BookGenerationResponse:
        """사용자 요청에 따라 동화를 생성하고 데이터베이스에 저장합니다."""
        
        try:
            # ChatGPT를 통해 동화 생성
            logger.info(f"사용자 {user_id}의 동화 생성 시작: {request}")
            story_content = await self.chatgpt_service.generate_story(request)
            
            # 데이터베이스에 책 저장
            book = await self._save_book_to_db(user_id, request, story_content)
            
            logger.info(f"동화 생성 완료: 책 ID {book.id}")
            
            return BookGenerationResponse(
                success=True,
                message="동화가 성공적으로 생성되었습니다.",
                book_id=str(book.id),
                story_content=self._format_story_for_response(story_content)
            )
            
        except Exception as e:
            logger.error(f"동화 생성 실패: {str(e)}")
            return BookGenerationResponse(
                success=False,
                message="동화 생성 중 오류가 발생했습니다.",
                error=str(e)
            )
    
    async def _save_book_to_db(self, user_id: PydanticObjectId, request: BookGenerationRequest, story_content: BookContent) -> Book:
        """생성된 동화를 데이터베이스에 저장합니다."""
        
        # 연령대를 숫자로 변환
        age = self._convert_age_group_to_number(request.age_group)
        
        book = Book(
            user_id=user_id,
            book_title=story_content.title,
            book_author="AI 동화 작가",
            book_contents=self._combine_pages(story_content.pages),
            age=age,
            
            # 사용자 입력 정보
            gender=request.gender,
            age_group=request.age_group,
            lesson=request.lesson,
            animal=request.animal,
            voice_option=request.voice_option,
            
            # 생성된 동화 내용
            pages=story_content.pages,
            summary=story_content.summary,
            characters=story_content.characters,
            setting=story_content.setting
        )
        
        await book.insert()
        return book
    
    def _convert_age_group_to_number(self, age_group: str) -> int:
        """연령대 문자열을 숫자로 변환합니다."""
        age_mapping = {
            "1세 이하": 1,
            "1~2세": 2,
            "3~4세": 4,
            "5~6세": 6,
            "7~8세": 8,
            "9~10세": 10
        }
        return age_mapping.get(age_group, 5)  # 기본값 5세
    
    def _combine_pages(self, pages: list[str]) -> str:
        """페이지들을 하나의 문자열로 결합합니다."""
        return "\n\n".join([f"페이지 {i+1}: {page}" for i, page in enumerate(pages)])
    
    def _format_story_for_response(self, story_content: BookContent) -> str:
        """응답용으로 동화 내용을 포맷팅합니다."""
        formatted_content = f"제목: {story_content.title}\n\n"
        formatted_content += f"요약: {story_content.summary}\n\n"
        formatted_content += f"등장인물: {', '.join(story_content.characters)}\n\n"
        formatted_content += f"배경: {story_content.setting}\n\n"
        formatted_content += "동화 내용:\n"
        
        for i, page in enumerate(story_content.pages, 1):
            formatted_content += f"\n페이지 {i}: {page}"
        
        return formatted_content
    
    async def get_user_books(self, user_id: PydanticObjectId) -> list[Book]:
        """사용자의 생성된 책 목록을 조회합니다."""
        books = await Book.find(Book.user_id == user_id).sort("-created_at").to_list()
        return books
    
    async def get_book_by_id(self, book_id: str, user_id: PydanticObjectId) -> Optional[Book]:
        """특정 책을 조회합니다."""
        try:
            book = await Book.get(PydanticObjectId(book_id))
            if book and book.user_id == user_id:
                return book
            return None
        except Exception:
            return None


# 싱글톤 인스턴스
book_generation_service = BookGenerationService()
