from pydantic import BaseModel, Field
from typing import Optional


class KeepAliveModel(BaseModel):
    redis_key: str = Field(default=None, alias='redisKey', description='Redis key field')
    redis_value: Optional[str] = Field(default="1", alias='redisValue', description='Redis value field')
    ttl_secs: Optional[int] = Field(default=60, alias='ttlSecs', description='expire time in seconds')
