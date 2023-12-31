# FastAPI is a framework for building server, like Flask.

from fastapi import FastAPI
app = FastAPI(
    title="CS Tutor",
    description="Use a real-world example to explain various concepts.",
)

@app.get("/example")
def get_example():
    return 