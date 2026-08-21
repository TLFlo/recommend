from app.utils.serilizer import serialize_mongo
from app.database.mongodb import reviews_collection

async def create_review(review_data: dict) -> dict:

    result = await reviews_collection.insert_one(
        review_data
    )

    review = await reviews_collection.find_one(
        {"_id": result.inserted_id}
    )

    return serialize_mongo(review)