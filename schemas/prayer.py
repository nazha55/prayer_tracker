from pydantic import BaseModel
from typing import Literal

class UpdatePrayerRequest(BaseModel):
    prayer: Literal["fajr", "dhuhr", "asr", "maghrib", "isha"]
    status: Literal["on_time", "late", "missed"]