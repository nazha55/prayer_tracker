from pydantic import BaseModel

class CreateRoutineRequest(BaseModel):
    title: str


class ToggleRoutineRequest(BaseModel):
    routine_id: int