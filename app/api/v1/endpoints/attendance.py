from fastapi import APIRouter
from app.models.attendance import Attendance
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from beanie import PydanticObjectId
from zoneinfo import ZoneInfo

router = APIRouter()
KST = ZoneInfo("Asia/Seoul")

class AttendanceRequest(BaseModel):
    user_id: PydanticObjectId
    is_present: bool  

def kst_day_bounds_utc(d):
    start_kst = datetime.combine(d, time.min, tzinfo=KST)
    end_kst   = start_kst + timedelta(days=1)
    return start_kst.astimezone(timezone.utc), end_kst.astimezone(timezone.utc)

@router.get("", summary="출석정보 로드")
async def get_attendance_status(user_id: PydanticObjectId):
    consecutive_days = await calculate_consecutive_attendance(user_id)

    records = await Attendance.find(
        Attendance.user_id == user_id,
        Attendance.is_present == True
    ).to_list()

    # 저장은 UTC → 응답은 KST 날짜로 표시
    attended_days = [
        (rec.date.astimezone(KST)).strftime("%Y-%m-%d")
        for rec in records if rec.date is not None
    ]

    return {
        "consecutive_days": int(consecutive_days or 0),
        "attended_days": attended_days
    }

@router.post("", summary="출석정보 업로드 및 갱신")
async def mark_attendance(attendance: AttendanceRequest):
    user_id = attendance.user_id

    now_utc = datetime.now(timezone.utc)
    today_start_utc = datetime(now_utc.year, now_utc.month, now_utc.day, tzinfo=timezone.utc)
    tomorrow_start_utc = today_start_utc + timedelta(days=1)

    existing_attendance = await Attendance.find_one(
        Attendance.user_id == user_id,
        Attendance.date >= today_start_utc,
        Attendance.date < tomorrow_start_utc,
    )

    if existing_attendance:
        existing_attendance.is_present = attendance.is_present
        await existing_attendance.save()  
    else:
        new_attendance = Attendance(
            user_id=user_id, date=now_utc, is_present=attendance.is_present
        )
        await new_attendance.insert()
    
    consecutive_days = await calculate_consecutive_attendance(user_id)
    return {"status": "success", "consecutive_days": int(consecutive_days or 0)}


async def calculate_consecutive_attendance(user_id: PydanticObjectId) -> int:
    today_kst = datetime.now(tz=KST).date()

    # 오늘(KST) 출석 여부
    t_start_utc, t_end_utc = kst_day_bounds_utc(today_kst)
    today_attended = await Attendance.find_one(
        Attendance.user_id == user_id,
        Attendance.is_present == True,
        Attendance.date >= t_start_utc,
        Attendance.date <  t_end_utc,
    )

    # 기준일: 오늘 출석이면 오늘부터, 아니면 어제부터
    current_day = today_kst if today_attended else (today_kst - timedelta(days=1))

    streak = 0
    # 안전장치: 1년 상한
    for _ in range(366):
        start_utc, end_utc = kst_day_bounds_utc(current_day)
        exists = await Attendance.find_one(
            Attendance.user_id == user_id,
            Attendance.is_present == True,
            Attendance.date >= start_utc,
            Attendance.date <  end_utc,
        )
        if exists is None:
            break
        streak += 1
        current_day -= timedelta(days=1)

    return streak