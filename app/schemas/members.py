from app.schemas.bands import MemberBase


class MemberRead(MemberBase):
    ...


class MemberCreate(MemberBase):
    ...


class MemberPatch(MemberBase):
    name: str = None
    email: str = None
    address: str = None
    debt: int = None
