from flask import Flask

api = Flask(__name__)


@api.get("/")
def route_main():
    """Return a simple greeting message."""
    return "Hello there."


if __name__ == "__main__":
    api.run(port=5000)
