from datetime import datetime, timezone

from pydantic import BaseModel, Field


class StringRaw(BaseModel):
    value: str

class Properties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: dict


class StringAnalysed(BaseModel):
    id: str
    value: str
    properties: Properties
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# # props = Properties(length=12, language="English")
# item = StringAnalysed(id="A001", value="Hello world!", properties='hi')
# print(item.model_dump())  # new in Pydantic v2

