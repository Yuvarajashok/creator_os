from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Any
from uuid import UUID

from database import get_db
from models.user import User
from models.page import Page
from models.post import Post
from schemas.post import PostCreate, PostUpdate, PostResponse
from core.security import get_current_user

router = APIRouter()


async def verify_page_ownership(page_id: UUID, user_id: UUID, db: AsyncSession) -> Page:
    result = await db.execute(
        select(Page).filter(Page.id == page_id, Page.user_id == user_id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found or access denied"
        )

    return page


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    await verify_page_ownership(post_data.page_id, current_user.id, db)

    result = await db.execute(
        select(Post).filter(Post.instagram_post_id == post_data.instagram_post_id)
    )
    existing_post = result.scalar_one_or_none()

    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post already exists"
        )

    new_post = Post(**post_data.model_dump())

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@router.get("/page/{page_id}", response_model=List[PostResponse])
async def get_page_posts(
    page_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    await verify_page_ownership(page_id, current_user.id, db)

    result = await db.execute(
        select(Post).filter(Post.page_id == page_id).order_by(Post.timestamp.desc())
    )
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    await verify_page_ownership(post.page_id, current_user.id, db)

    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: UUID,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    await verify_page_ownership(post.page_id, current_user.id, db)

    update_data = post_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    await verify_page_ownership(post.page_id, current_user.id, db)

    await db.delete(post)
    await db.commit()
