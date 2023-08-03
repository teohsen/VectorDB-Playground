"""
https://milvus.io/docs/search.md

"""
import random
import numpy as np
from pymilvus import Collection, connections, utility
import milvus.schemas.book as book

connections.connect(
  alias="default",
  user='username',
  password='password',
  host='localhost',
  port='8082'
)

if utility.has_collection(book.collection_name):
    collection = Collection(book.collection_name)      # Get an existing collection, deprecated in milvus v2
else:
    # Create a collection in Milvus.
    collection = Collection(name=book.collection_name,
                            schema=book.schema,
                            using="default",
                            shards_num=2)


def generate_data():
    # Generate the book data.
    for i in range(100):
        data = {
            "book_id": i,
            "book_name": f"Book {i}",
            "word_count": random.randint(10, 1000),
            "book_intro": np.random.rand(2)
        }
        # Insert the book data into the collection.
        data = [[i], [f"book {i}"], [random.randint(10, 1000)], [np.random.rand(2)]]

        collection.insert(data)

    # Index needs to be built
    index_params = {
      "metric_type":"L2",
      "index_type":"IVF_FLAT",
      "params":{"nlist":1024}
    }
    collection.create_index(
      field_name="book_intro",
      index_params=index_params
    )

    utility.index_building_progress("book")


def search():
    collection.load()

    search_params = {
        "metric_type": "L2",
        "offset": 5,
        "ignore_growing": False,
        "params": {"nprobe": 10}
    }

    results = collection.search(
        data=[[0.1, 0.2]],
        anns_field="book_intro",
        # the sum of `offset` in `param` and `limit`
        # should be less than 16384.
        param=search_params,
        limit=10,
        expr=None,
        # set the names of the fields you want to
        # retrieve from the search result.
        output_fields=['book_name'],
        consistency_level="Strong"
    )

    # get the IDs of all returned hits
    print(results[0].ids)
    # get the distances to the query vector from all returned hits
    print(results[0].distances)

    # get the value of an output field specified in the search request.
    # hit = results[0][0]
    # print(hit.entity.get("book_name"))
    for h in range(results[0].ids.__len__()-1):
        _ = results[0][h]
        print(f"index = {h}, { _.entity.get('book_name') = }")


    collection.release()
    connections.disconnect("default")