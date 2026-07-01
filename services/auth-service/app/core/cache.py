import json
from app.core.redis_com import redis_client

def get_user_cache(user_id:str):
    return  redis_client.get(f"user:{user_id}")

def set_user_cache(user_id:str, data:dict):
    redis_client.set(f"user:{user_id}", json.dumps(data), ex = 300)

def delete_user_cache(user_id:str):
    redis_client.delete(f"user:{user_id}")