from typing import Any, Union

from fastapi import APIRouter
from sqlmodel import func, select

from app.models import Transaction, Hero

router = APIRouter()


# @router.get("/", response_model=Transaction)
# def read_items(
#     session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
# ) -> Any:
#     """
#     Retrieve items.
#     """

#     if current_user.is_superuser:
#         count_statement = select(func.count()).select_from(Item)
#         count = session.exec(count_statement).one()
#         statement = select(Item).offset(skip).limit(limit)
#         items = session.exec(statement).all()
#     else:
#         count_statement = (
#             select(func.count())
#             .select_from(Item)
#             .where(Item.owner_id == current_user.id)
#         )
#         count = session.exec(count_statement).one()
#         statement = (
#             select(Item)
#             .where(Item.owner_id == current_user.id)
#             .offset(skip)
#             .limit(limit)
#         )
#         items = session.exec(statement).all()

#     return ItemsPublic(data=items, count=count)





@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

