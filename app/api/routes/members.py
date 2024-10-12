from typing import List, Union, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, HTTPException
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repository.members import MemberRepository
from app.schemas.members import MemberRead, MemberCreate, MemberPatch

router = APIRouter(tags=["Members"])


@router.post(
    "",
    response_model=MemberRead,
    status_code=status.HTTP_201_CREATED,
    name="add_member",
)
async def add_book(
        member: MemberCreate = Body(...),
        repository: MemberRepository = Depends(get_repository(MemberRepository)),
) -> MemberRead:

    return await repository.add_member(member)


@router.get(
    "/{member}/detail",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="get_member",
)
async def get_member(
        member: Union[str, UUID],
        repository: MemberRepository = Depends(get_repository(MemberRepository)),
) -> Union[MemberRead, HTTPException]:

    return await repository.get_member(member_id=member)


@router.get(
    "",
    response_model=Dict[str, Union[List[MemberRead], Any]],
    status_code=status.HTTP_200_OK,
    name="get_members",
)
async def get_members(
        limit: int = Query(default=10, lt=100),
        offset: int = Query(default=0),
        repository: MemberRepository = Depends(get_repository(MemberRepository)),
) -> Dict[str, Union[List[MemberRead], Any]]:

    return await repository.get_members(limit=limit, offset=offset)


@router.put(
    "/{member}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="update_member",
)
async def update_member(
        member: Union[str, UUID],
        member_patch: MemberPatch = Body(...),
        repository: MemberRepository = Depends(get_repository(MemberRepository)),
) -> Union[MemberRead, HTTPException]:

    await repository.get_member(member_id=member)

    return await repository.patch_member(
        member_id=member,
        member=member_patch,
    )


@router.delete(
    "/{member}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_member",
)
async def delete_member(
        member: Union[str, UUID],
        repository: MemberRepository = Depends(get_repository(MemberRepository)),
) -> None:

    await repository.delete_member(member_id=member)
