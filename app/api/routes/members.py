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
    """
    Add a new member to the repository.

    This function handles the creation of a new member by accepting the necessary member data and storing it in the repository. 
    Upon successful addition, it returns the details of the newly created member.

    Args:
        member (MemberCreate): The data for the member to be added.
        repository (MemberRepository): The repository instance used to interact with member data.

    Returns:
        MemberRead: The details of the newly created member.

    Raises:
        HTTPException: If there is an error during the member addition process.
    """

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
    """
    Retrieve the details of a specific member from the repository.

    This function processes requests to fetch the details of a member identified by their unique identifier. 
    It returns the member's information if found, or raises an exception if the member does not exist.

    Args:
        member (Union[str, UUID]): The identifier of the member to retrieve.
        repository (MemberRepository): The repository instance used to access member data.

    Returns:
        Union[MemberRead, HTTPException]: The details of the requested member or an HTTP exception if not found.

    Raises:
        HTTPException: If the member cannot be found in the repository.
    """

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
    """
    Retrieve a list of members from the repository with optional pagination.

    This function allows clients to fetch a collection of members, supporting pagination through limit and offset parameters. 
    It returns a dictionary containing the list of members and any additional information as needed.

    Args:
        limit (int): The maximum number of members to return (default is 10, must be less than 100).
        offset (int): The number of members to skip before starting to collect the result set (default is 0).
        repository (MemberRepository): The repository instance used to access member data.

    Returns:
        Dict[str, Union[List[MemberRead], Any]]: A dictionary containing a list of members and any additional information.

    Raises:
        HTTPException: If there is an error retrieving the members from the repository.
    """

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
    """
    Update the details of an existing member in the repository.

    This function processes a request to modify the information of a specific member identified by their unique identifier. 
    It applies the provided changes and returns the updated member details upon successful modification.

    Args:
        member (Union[str, UUID]): The identifier of the member to update.
        member_patch (MemberPatch): The data containing the updates to be applied to the member.
        repository (MemberRepository): The repository instance used to access and modify member data.

    Returns:
        Union[MemberRead, HTTPException]: The updated details of the member or an HTTP exception if the member cannot be found.

    Raises:
        HTTPException: If the member does not exist or if there is an error during the update process.
    """

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
    """
    Delete a specific member from the repository.

    This function handles requests to remove a member identified by their unique identifier from the repository. Upon successful deletion, it returns no content, indicating that the operation was completed.

    Args:
        member (Union[str, UUID]): The identifier of the member to be deleted.
        repository (MemberRepository): The repository instance used to access and modify member data.

    Returns:
        None

    Raises:
        HTTPException: If the member cannot be found or if there is an error during the deletion process.
    """

    await repository.delete_member(member_id=member)
