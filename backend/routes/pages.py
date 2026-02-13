from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Any
from uuid import UUID

from database import get_db
from models.user import User
from models.page import Page
from schemas.page import PageCreate, PageUpdate, PageResponse
from core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
async def create_page(
    page_data: PageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(
        select(Page).filter(Page.instagram_username == page_data.instagram_username)
    )
    existing_page = result.scalar_one_or_none()

    if existing_page:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram username already registered"
        )

    new_page = Page(
        user_id=current_user.id,
        instagram_username=page_data.instagram_username,
        bio=page_data.bio
    )

    db.add(new_page)
    await db.commit()
    await db.refresh(new_page)

    return new_page


@router.get("/", response_model=List[PageResponse])
async def get_pages(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(
        select(Page).filter(Page.user_id == current_user.id).order_by(Page.created_at.desc())
    )
    pages = result.scalars().all()
    return pages


@router.get("/{page_id}", response_model=PageResponse)
async def get_page(
    page_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(
        select(Page).filter(Page.id == page_id, Page.user_id == current_user.id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    return page


@router.put("/{page_id}", response_model=PageResponse)
async def update_page(
    page_id: UUID,
    page_data: PageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(
        select(Page).filter(Page.id == page_id, Page.user_id == current_user.id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    update_data = page_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(page, field, value)

    await db.commit()
    await db.refresh(page)

    return page


@router.delete("/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    page_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    result = await db.execute(
        select(Page).filter(Page.id == page_id, Page.user_id == current_user.id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found"
        )

    await db.delete(page)
    await db.commit()
