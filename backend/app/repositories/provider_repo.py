from app.database.mongodb import providers_collection


async def create_provider(provider: dict):

    result = await providers_collection.insert_one(provider)

    return result.inserted_id


async def get_provider(provider_id):

    return await providers_collection.find_one({
        "_id": provider_id
    })