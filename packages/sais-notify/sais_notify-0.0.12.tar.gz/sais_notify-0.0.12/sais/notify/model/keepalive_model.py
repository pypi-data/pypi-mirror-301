from pydantic import BaseModel, Field


class KeepAliveModel(BaseModel):
    redis_key: str = Field(default=None, alias='redisKey', description='Redis key field')
    redis_value: str = Field(default=None, alias='redisValue', description='Redis value field')
    ttl_secs: int = Field(default=None, alias='ttlSecs', description='expire time in seconds')
