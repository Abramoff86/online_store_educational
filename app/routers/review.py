from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, or_
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.auth import get_current_user


from app.backend.db_depends import get_db
from app.schemas import CreateReview
from app.models.products import Product
from app.models.category import Category
from app.models.review import Review

router = APIRouter(prefix='/review', tags=['review'])




@router.get('/')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    reviews = await db.scalars(select(Review).join(Product).where(Product.is_active == True, Review.is_active == True))
    if reviews:
        return reviews.all()

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='0 reviews'
    )

@router.get('/{product_id}')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_id: int):
    reviews = await db.scalars(select(Review).join(Product).where(Review.product_id == product_id, Product.is_active == True, Review.is_active == True))
    if reviews:
        return reviews.all()

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='This product has no reviews'
    )

@router.post('/{product_id}')
async def add_review(db: Annotated[AsyncSession, Depends(get_db)], product_id: int, create_review: CreateReview, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_customer'):
        product = await db.scalar(select(Product).where(Product.id == product_id, Product.is_active == True))
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no product found'
            )

        await db.execute(insert(Review).values(user_id=get_user.get('id'),
                                            product_id=product_id,
                                            comment=create_review.comment,
                                            grade=create_review.grade,))

        new_review = await db.scalars(select(Review.grade).where(Review.product_id == product_id, Review.is_active == True))
        new_review = list(new_review.all())
        product_update = await db.scalar(select(Product).where(Product.id == product_id))
        product_update.rating = sum(new_review) // len(new_review)

        await db.commit()

        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )


@router.delete('/{product_id}/{review_id}')
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_id: int, review_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        del_reviwe = await db.scalar(select(Review).where(Review.product_id == product_id, Review.id == review_id, Review.is_active == True))
        if del_reviwe:
            del_reviwe.is_active = False
            await db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'Review delete is successful'
            }

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no review found'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )
