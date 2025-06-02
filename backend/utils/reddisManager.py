import redis.asyncio as redis


class RedisManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str):
        await self.redis.set(key, value)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0

    async def close(self):
        await self.redis.close()

    async def get_all_keys(self):
        return await self.redis.keys("*")
