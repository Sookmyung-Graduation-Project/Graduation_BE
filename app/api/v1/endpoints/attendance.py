from fastapi import APIRouter
from app.models.attendance import Attendance
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from beanie import PydanticObjectId
from zoneinfo import ZoneInfo

router = APIRouter()
KST = ZoneInfo("Asia/Seoul")

@router.get("", summary="출석정보 로드")
async def get_attendance_status(user_id: PydanticObjectId):
    consecutive_days = await calculate_consecutive_attendance(user_id)

    attendance_records = await Attendance.find(
        Attendance.user_id == user_id,
        Attendance.is_present == True
    ).to_list()

    attended_days = [rec.date.strftime("%Y-%m-%d") for rec in attendance_records]

    return {
        "consecutive_days": int(consecutive_days or 0), 
        "attended_days": attended_days
    }


class AttendanceRequest(BaseModel):
    user_id: PydanticObjectId
    is_present: bool  

@router.post("", summary="출석정보 업로드 및 갱신")
async def mark_attendance(attendance: AttendanceRequest):
    user_id = attendance.user_id
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    tomorrow_start = today_start + timedelta(days=1)

    existing_attendance = await Attendance.find_one(
        Attendance.user_id == user_id,
        Attendance.date >= today_start,
        Attendance.date < tomorrow_start
    )
    
    if existing_attendance:
        existing_attendance.is_present = attendance.is_present
        await existing_attendance.save()  
    else:
        new_attendance = Attendance(user_id=user_id, date=now, is_present=attendance.is_present)
        await new_attendance.insert()  

    
    consecutive_days = await calculate_consecutive_attendance(user_id)

    return {"status": "success", "consecutive_days": consecutive_days}


async def calculate_consecutive_attendance(user_id: PydanticObjectId) -> int:
    today_kst = datetime.now(tz=KST).date()
    today_start = datetime.combine(today_kst, datetime.min.time())
    today_end = datetime.combine(today_kst, datetime.max.time())

    today_attended = await Attendance.find_one(
        Attendance.user_id == user_id,
        Attendance.is_present == True,
        Attendance.date >= today_start,
        Attendance.date < today_end
    )

    # 기준일 : 오늘 출석 시 오늘부터, 미출석 시 어제부터
    current_day = today_kst if today_attended else (today_kst - timedelta(days=1))
    
    streak = 0

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