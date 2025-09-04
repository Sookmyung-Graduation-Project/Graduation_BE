from fastapi import APIRouter
from app.models.attendance import Attendance
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from beanie import PydanticObjectId
from zoneinfo import ZoneInfo

router = APIRouter()
KST = ZoneInfo("Asia/Seoul")

# 출석 현황 조회 (연속출석일, 금주 출석 요일)
@router.get("")
@router.get("/")
async def get_attendance_status(user_id: PydanticObjectId):
    # 연속 출석일 계산
    consecutive_days = await calculate_consecutive_attendance(user_id)

    # 이번 주 월요일 ~ 일요일 범위를 계산
    # 오늘 00:00 ~ 23:59:59 범위
    now = datetime.now(tz=KST)
    today_start = datetime(now.year, now.month, now.day)
    week_start = today_start - timedelta(days=today_start.weekday())  # 월요일 00:00
    week_end = week_start + timedelta(days=7)  # 다음주 월요일 00:00 (미만 비교)

    # 금주 출석 요일(출석 true인 날만)
    weekly_records = await Attendance.find(
        Attendance.user_id == user_id,
        Attendance.is_present == True,
        Attendance.date >= week_start,
        Attendance.date < week_end
    ).to_list()

    attended_days = sorted({rec.date.weekday() for rec in weekly_records}) if weekly_records else []

    return {"consecutive_days": int(consecutive_days or 0), "attended_days": attended_days}

# 출석 체크 (출석 여부 저장)
class AttendanceRequest(BaseModel):
    user_id: PydanticObjectId
    is_present: bool  # 출석 여부

@router.post("")
@router.post("/")
async def mark_attendance(attendance: AttendanceRequest):
    user_id = attendance.user_id
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    tomorrow_start = today_start + timedelta(days=1)

    # 출석 여부 갱신 (AND 조건으로 결합)
    existing_attendance = await Attendance.find_one(
        Attendance.user_id == user_id,
        Attendance.date >= today_start,
        Attendance.date < tomorrow_start
    )
    
    if existing_attendance:
        existing_attendance.is_present = attendance.is_present
        await existing_attendance.save()  # 이미 출석이 기록된 경우 업데이트
    else:
        # 새로운 출석 기록 추가
        new_attendance = Attendance(user_id=user_id, date=now, is_present=attendance.is_present)
        await new_attendance.insert()  # 새로운 출석 기록 저장

    # 연속 출석일 계산
    consecutive_days = await calculate_consecutive_attendance(user_id)

    return {"status": "success", "consecutive_days": consecutive_days}


# 연속 출석일 계산 함수
async def calculate_consecutive_attendance(user_id: PydanticObjectId) -> int:
    today_kst = datetime.now(tz=KST).date()
    today_start = datetime.combine(today_kst, datetime.min.time())
    today_end = datetime.combine(today_kst, datetime.max.time())

    # 오늘 출석 여부 확인
    today_attended = await Attendance.find_one(
        Attendance.user_id == user_id,
        Attendance.is_present == True,
        Attendance.date >= today_start,
        Attendance.date < today_end
    )

    # 기준일 : 오늘 출석 시 오늘부터, 미출석 시 어제부터
    current_day = today_kst if today_attended else (today_kst - timedelta(days=1))
    
    streak = 0

    # 연속 출석일 계산
    while True:
        current_start = datetime.combine(current_day, datetime.min.time())
        current_end = datetime.combine(current_day, datetime.max.time())
        
        exists = await Attendance.find_one(
            Attendance.user_id == user_id,
            Attendance.is_present == True,
            Attendance.date >= current_start,
            Attendance.date < current_end
        )
        
        
        if exists is None:
            # 출석하지 않은 날을 만나면 중단
            break
            
        streak += 1
        current_day -= timedelta(days=1)
        
    return streak