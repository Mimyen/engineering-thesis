from typing import Annotated, Literal, Optional
from fastapi import APIRouter, Depends, Response, Form, HTTPException, Path, Body, Query, status, File, UploadFile
from sqlalchemy.orm import Session
from app.dependencies import DefaultResponseModel, Authorize, DBSessionProvider, validate_password, CreateExampleResponse, Example, DefaultErrorModel, Responses, CreateAuthResponses, CreateAuthorizeResponses, CreateInternalErrorResponse
from app.config import SECRET_KEY, ENCRYPTION_ALGORITHM, IP_ADDRESS, IMAGE_DIR, IMAGE_URL
from pydantic import BaseModel, Field
from uuid import uuid4
import jwt
import re
from fastapi_pagination import Page, paginate
from app.bot import bot
import asyncio

router = APIRouter(
    prefix="/manager",
    tags=["Manager"],
    responses=Responses(
        CreateInternalErrorResponse()
    )
)

class ServerModel(BaseModel):
    id: str | int
    name: str

@router.post(
    "/test-bot",
    responses=Responses(
        CreateExampleResponse(
            code=200,
            content_type="application/json",
            examples=[
                Example(name="Correct response", summary="Correct response", value=[ServerModel(id="1234567890", name="Powazny serwer"), ServerModel(id="0987654321", name="Super serwer")])
            ]
        )
    )
)
async def test_bot(
    db: Annotated[Session, Depends(DBSessionProvider)]
) -> list[ServerModel]:
    
    guilds = bot.guilds
    output = []

    for guild in guilds:
        output.append({
            "id": str(guild.id),
            "name": guild.name
        })

    return output

async def send_message(guild_id: int, channel_id: int, message: str):
    print(f"🔍 Looking for guild {guild_id}...")
    guild = bot.get_guild(guild_id)

    if not guild:
        print(f"❌ ERROR: Bot is not in guild {guild_id}")
        return

    print(f"✅ Found guild {guild_id}")
    print(f"🔍 Looking for channel {channel_id} in guild {guild_id}...")
    channel = guild.get_channel(channel_id)

    if not channel:
        print(f"❌ ERROR: Channel {channel_id} not found in guild {guild_id}")
        return

    print(f"✅ Found channel {channel_id}")

    if not channel.permissions_for(guild.me).send_messages:
        print(f"❌ ERROR: Bot lacks permission to send messages in {channel_id}")
        return

    print(f"✅ Bot has permission to send messages in {channel_id}")

    try:
        await channel.send(content=message)
        print(f"✅ Message successfully sent to {channel_id}")
    except Exception as e:
        print(f"❌ ERROR: Failed to send message: {e}")


@router.post("/test-2")
async def test_2(
    guild_id: Annotated[str, Query()],
    channel_id: Annotated[str, Query()],
    message: Annotated[str, Query()],
    db: Annotated[Session, Depends(DBSessionProvider)]
) -> DefaultResponseModel:
    
    guild = bot.get_guild(int(guild_id))
    if not guild:
        raise HTTPException(status_code=404, detail=f"Bot is not in guild {guild_id}")

    channel = guild.get_channel(int(channel_id))
    if not channel:
        raise HTTPException(status_code=404, detail=f"Channel {channel_id} not found in guild {guild_id}")

    if not channel.permissions_for(guild.me).send_messages:
        raise HTTPException(status_code=403, detail="Bot lacks permission to send messages in this channel")

    asyncio.create_task(send_message(int(guild_id), int(channel_id), message))

    return DefaultResponseModel(message="Message scheduled")