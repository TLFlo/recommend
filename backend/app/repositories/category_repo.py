from bson import ObjectId

from app.database.mongodb import categories_collection
from app.utils.serilizer import serialize_mongo, serialize_mongo_list


async def get_categories_by_ids(
    category_ids: list[ObjectId],
) -> list[dict]:

    cursor = categories_collection.find(
        {"_id": {"$in": category_ids}}
    )

    categories = await cursor.to_list(length=None)

    return serialize_mongo_list(categories)


async def create_category(category_data: dict) -> dict:
    result = await categories_collection.insert_one(category_data)

    category = await categories_collection.find_one({"_id": result.inserted_id})

    return serialize_mongo(category)
