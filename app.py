from typing import Union

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    """
    http://127.0.0.1:8081/

    :return:
    """
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    """
    e.g http://127.0.0.1:8081/items/5?q=somequery

    :param item_id:
    :param q:
    :return:
    """
    return {"item_id": item_id, "q": q}
