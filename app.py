from flask import Flask
import os
import redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

cache = redis.Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True
)

@app.route("/")
def home():
    return "Jenkins Docker CI/CD Application is running!"

@app.route("/health")
def health():
    try:
        cache.ping()
        return {
            "status": "healthy",
            "redis": "connected"
        }, 200
    except Exception:
        return {
            "status": "unhealthy",
            "redis": "disconnected"
        }, 503

@app.route("/counter")
def counter():
    count = cache.incr("counter")
    return {
        "counter": count
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
