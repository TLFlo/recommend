from app.database.mongodb import providers_collection
from app.utils.serilizer import serialize_mongo

async def create_provider(provider: dict) -> dict:

    result = await providers_collection.insert_one(provider)

    provider["_id"] = result.inserted_id

    return serialize_mongo(provider)


async def get_provider(provider_id):
    return await providers_collection.find_one({"_id": provider_id})
