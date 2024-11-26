from pydantic import BaseModel


class Notifications(BaseModel):
    id: int
    type: str
    user_id: int
    data: str | int


notifications1 = Notifications(
    id=1,
    type="system",
    user_id=1,
    data="Привет",
)
notifications2 = Notifications(
    id=2,
    type="friendrequest",
    user_id=1,
    data=1,
)
