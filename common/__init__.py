from redis import Redis


# 连接redis
from Boyuan import settings

rds = Redis(**settings.REDIS)