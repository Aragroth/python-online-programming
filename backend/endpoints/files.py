"""
Раздаёт картинки, которые находятся в описании к заданиям и опросникам
"""
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from core.config import database

router = APIRouter()


# pylint: disable=W0707
@router.get("/{image_id}")
async def image_endpoint(image_id: str):
    """Возвращает фотографию по её айди в mongoDB"""
    grid_filesystem = AsyncIOMotorGridFSBucket(database.files_conn(), collection="images")
    try:
        _id = ObjectId(image_id)
        grid_out = await grid_filesystem.open_download_stream(_id)
        contents = await grid_out.read()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такой картинки не существует",
        )

    return Response(content=contents, media_type=grid_out.content_type)
