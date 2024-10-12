from http.client import HTTPException
from typing import Optional, Union, Any, Dict, List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.sync import update

from app.core.exception import http_400, http_404, http_409
from app.db.tables.library import Members
from app.schemas.members import MemberRead, MemberPatch, MemberCreate


class MemberRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, member_id: Optional[UUID, str] = None, member_name: Optional[str] = None) -> Union[Any, HTTPException]:
        if member_id:
            member_id = UUID(str(member_id))
            stmt = (
                select(Members)
                .where(Members.id == member_id)
            )
        elif member_name:
            stmt = (
                select(Members)
                .where(Members.name == member_name)
            )
        else:
            return http_400(msg="Provide member id or member name")

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _extract_changes(member_patch: MemberPatch) -> Dict[str, Any]:
        if isinstance(member_patch, dict):
            return member_patch
        return member_patch.model_dump(exclude_unset=True)

    async def get_member(self, member_id: Optional[UUID] = None, member_name: Optional[str] = None) -> Union[MemberRead, HTTPException]:
        db_member = await self._get_instance(member_id=member_id, member_name=member_name)
        if db_member is None:
            return http_404(msg="Member not found")

        return MemberRead(**db_member.__dict__)

    async def get_members(self, limit: int = 10, offset: int = 0) -> Dict[str, Union[List[MemberRead], Any]]:
        stmt = (
            select(Members)
            .limit(limit)
            .offset(offset)
        )

        try:
            result = await self.session.execute(stmt)
            result_list = result.fetchall()

            for row in result_list:
                row.__dict__.pop('_sa_instance_state', None)

            result = [MemberRead(**row.__dict__) for row in result_list]
            return {
                "result": result,
                "no_of_members": len(result),
            }
        except Exception as e:
            raise http_404(msg=f"No members.") from e

    async def add_member(self, member: MemberCreate) -> Union[MemberRead, HTTPException]:
        if not isinstance(member, dict):
            db_member = Members(**member.model_dump())
        else:
            db_member = Members(**member)

        try:
            self.session.add(db_member)
            await self.session.commit()
            await self.session.refresh(db_member)
        except IntegrityError as e:
            raise http_404(msg=f"Member with details {db_member} already exists") from e

        return MemberRead(**db_member.__dict__)

    async def patch_member(self, member_id: Union[str, UUID], member: MemberPatch) -> Union[MemberRead, HTTPException]:
        db_member = await self._get_instance(member_id=member_id)
        changes = await self._extract_changes(member_patch=member)

        stmt = (
            update(Members)
            .where(Members.id == db_member.get('id'))
            .values(changes)
        )

        try:
            await self.session.execute(stmt)
        except Exception as e:
            raise http_409(msg=f"Error updating member {db_member.get('name')}") from e

        return MemberRead(**db_member.__dict__)

    async def delete_member(self, member_id: Optional[UUID] = None, member_name: Optional[str] = None) -> None:
        try:
            db_member = await self._get_instance(member_id=member_id, member_name=member_name)

            stmt = (
                delete(Members)
                .where(Members.id == db_member.get('id'))
            )

            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            raise http_409(msg=f"Error deleting member: {member_id}") from e
