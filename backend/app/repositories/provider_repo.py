from app.database.mongodb import providers_collection
from app.utils.serilizer import serialize_mongo
from bson import ObjectId

async def create_provider(provider: dict) -> dict:

    result = await providers_collection.insert_one(provider)

    provider["_id"] = result.inserted_id

    return serialize_mongo(provider)


async def get_provider(provider_id):
    return await providers_collection.find_one({"_id": provider_id})


async def get_top_providers_by_categories(
    category_ids: list[ObjectId],
    limit: int = 10,
) -> list[dict]:

    cursor = (
        providers_collection
        .find(
            {
                "categories.id": {
                    "$in": category_ids
                },
                "status": "active",
            }
        )
        .sort(
            "rating.average",
            -1
        )
        .limit(limit)
    )

    return await cursor.to_list(length=limit)


async def update_provider_rating(
    provider_id: ObjectId,
    rating: float,
) -> None:

    await providers_collection.update_one(
        {"_id": provider_id},
        [
            {
                "$set": {
                    "rating.sum": {
                        "$add": [
                            {"$ifNull": ["$rating.sum", 0]},
                            rating,
                        ]
                    },
                    "rating.count": {
                        "$add": [
                            {"$ifNull": ["$rating.count", 0]},
                            1,
                        ]
                    },
                }
            },
            {
                "$set": {
                    "rating.average": {
                        "$divide": [
                            "$rating.sum",
                            "$rating.count",
                        ]
                    }
                }
            },
        ],
    )