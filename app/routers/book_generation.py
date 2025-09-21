from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId
from app.schemas.book_generation import BookGenerationRequest, BookGenerationResponse
from app.services.book_generation_service import book_generation_service
from app.core.security import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()


@router.post("/generate", response_model=BookGenerationResponse)
async def generate_book(
    request: BookGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """
    사용자 입력에 따라 동화를 생성합니다.
    
    - **gender**: 성별 (남아/여아)
    - **age_group**: 연령대 (1세 이하 ~ 9~10세)
    - **lesson**: 교훈 (10가지 중 선택)
    - **animal**: 주인공 동물 (12가지 중 선택)
    - **voice_option**: 목소리 옵션 (보호자1/2/3)
    """
    try:
        result = await book_generation_service.generate_book(
            user_id=current_user.id,
            request=request
        )
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.error
            )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"동화 생성 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/books", response_model=List[dict])
async def get_user_books(
    current_user: User = Depends(get_current_user)
):
    """
    사용자가 생성한 책 목록을 조회합니다.
    """
    try:
        books = await book_generation_service.get_user_books(current_user.id)
        
        # 응답용으로 데이터 변환
        book_list = []
        for book in books:
            book_data = {
                "id": str(book.id),
                "title": book.book_title,
                "author": book.book_author,
                "age_group": book.age_group,
                "lesson": book.lesson,
                "animal": book.animal,
                "summary": book.summary,
                "created_at": book.created_at.isoformat(),
                "page_count": len(book.pages) if book.pages else 0
            }
            book_list.append(book_data)
        
        return book_list
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"책 목록 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/books/{book_id}", response_model=dict)
async def get_book_detail(
    book_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    특정 책의 상세 정보를 조회합니다.
    """
    try:
        book = await book_generation_service.get_book_by_id(book_id, current_user.id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="책을 찾을 수 없습니다."
            )
        
        return {
            "id": str(book.id),
            "title": book.book_title,
            "author": book.book_author,
            "gender": book.gender,
            "age_group": book.age_group,
            "lesson": book.lesson,
            "animal": book.animal,
            "voice_option": book.voice_option,
            "pages": book.pages,
            "summary": book.summary,
            "characters": book.characters,
            "setting": book.setting,
            "created_at": book.created_at.isoformat(),
            "updated_at": book.updated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"책 상세 정보 조회 중 오류가 발생했습니다: {str(e)}"
        )


