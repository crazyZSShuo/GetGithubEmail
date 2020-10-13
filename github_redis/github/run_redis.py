import redis
import six

r = redis.Redis(host="", port=6379, password="", db=15)
# r = redis.StrictRedis("redis://127.0.0.1:6379")
# r.lpush("github:start_urls","https://github.com/trending?since=daily")
# r.lpush("github:start_urls","https://github.com/trending?since=weekly")
# r.lpush("github:start_urls","https://github.com/trending?since=monthly")

def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if six.PY3 and isinstance(s, bytes):
        return s.decode(encoding)
    return s

fetch_one = r.lpop
data = fetch_one("github:start_urls")
url = bytes_to_str(data, "utf-8")
print(url)
