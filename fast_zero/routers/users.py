from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.exception import UserBadRequest, UserDontHavePermission, UserNotFound
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_current_user, get_password_hash
from fast_zero.service import UserService

router = APIRouter(prefix="/users", tags=["users"])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Username already exists",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Email already exists",
            )

    db_user = User(username=user.username, password=user.password, email=user.email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get("/", response_model=UserList)
def read_users(session: T_Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@router.put("/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    service = UserService(session=session, current_user=current_user)
    try:
        current_user = service.update_user(user_id, user)
    except (UserNotFound, UserDontHavePermission, UserBadRequest) as error:
        raise HTTPException(status_code=error.status_code, detail=error.message)

    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/{user_id}", response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    service = UserService(session=session, current_user=current_user)
    try:
        service.delete_user(user_id)
    except (UserNotFound, UserDontHavePermission) as error:
        raise HTTPException(status_code=error.status_code, detail=error.message)
    return {"message": "User deleted"}


@router.get("/{user_id}", response_model=UserPublic)
def get_a_user(user_id: int, session: T_Session, current_user: T_CurrentUser):
    service = UserService(session=session, current_user=current_user)
    try:
        user = service.get_user(user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=error.status_code, detail=error.message)
    return user
