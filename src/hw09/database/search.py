import os
import redis
from redis_lru import RedisLRU
import re

from database.models import Authors, Quotes


REDIS_HOST = os.getenv('REDIS_HOST', "localhost")
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=None)
cache = RedisLRU(client)
print("REDIS:", client)


@cache
def find_by_name(name: str) -> list:
    result = []
    author = Authors.objects(fullname__iregex=name).first()
    if author:
        author_fullname = author.fullname
        author_id = author.id
        records = Quotes.objects(author=author_id)
        for record in records:
            r_dict = record.to_mongo().to_dict()
            author_fullname = record.author.fullname
            if author_fullname:
                r_dict["author"] = author_fullname
            del r_dict["_id"]
            result.append(r_dict)
    return result


@cache
def find_tags(tag_str: str) -> list:
    tags = tag_str.split(",")
    tags_full = []
    for tag in tags:
        tag_q = Quotes.objects(tags__iregex=tag)
        if tag_q:
            tag_r = tag_q.first().tags
            tags_full.extend([r for r in tag_r if re.search(tag, r)])
    return tags_full


@cache
def find_by_tag(tag_str: str) -> list:
    result = []
    tags_full = find_tags(tag_str)
    if tags_full:
        # print(tags_full)
        records = Quotes.objects(tags__in=tags_full)
        for record in records:
            r_dict = record.to_mongo().to_dict()
            author_fullname = record.author.fullname
            if author_fullname:
                r_dict["author"] = author_fullname
            del r_dict["_id"]
            result.append(r_dict)
    return result


if __name__ == "__main__":
    from hw08.database.connect import connect_db

    if connect_db():
        # print(find_by_name("eins"))
        print(find_by_tag("li,succ"))
