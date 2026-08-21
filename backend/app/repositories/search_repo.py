from bson import ObjectId

from app.database.mongodb import searches_collections


async def get_most_searched_categories(
    user_id: ObjectId,
    limit: int = 3,
) -> list[dict]:

    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "category_id": {"$ne": None},
            }
        },
        {
            "$group": {
                "_id": "$category_id",
                "search_count": {"$sum": 1},
            }
        },
        {
            "$sort": {
                "search_count": -1
            }
        },
        {
            "$limit": limit
        },
    ]

    return await searches_collections.aggregate(
        pipeline
    ).to_list(length=limit)