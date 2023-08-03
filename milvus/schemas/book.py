from pymilvus import CollectionSchema, FieldSchema, DataType

book_id = FieldSchema(
  name="book_id",
  dtype=DataType.INT64,
  is_primary=True,
)
book_name = FieldSchema(
  name="book_name",
  dtype=DataType.VARCHAR,
  max_length=200,
)
word_count = FieldSchema(
  name="word_count",
  dtype=DataType.INT64,
)
book_intro = FieldSchema(
  name="book_intro",
  dtype=DataType.FLOAT_VECTOR,
  dim=2
)
schema = CollectionSchema(
  fields=[book_id, book_name, word_count, book_intro],
  description="Test book search",
  enable_dynamic_field=True
)
collection_name = "book"
