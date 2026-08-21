from bson import ObjectId
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.schemas.review_schema import ReviewCreate
from app.repositories import review_repo
from app.repositories import provider_repo
from app.services.ai_service import analyze_comment
from app.services.service_service import apply_ai_service_ratings


async def create_review(
    review: ReviewCreate,
    user_id: str,
) -> dict:

    # --------------------------------
    # 1. Vérifier les IDs
    # --------------------------------

    try:
        provider_id = ObjectId(review.provider_id)
        user_object_id = ObjectId(user_id)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID.",
        ) from exc

    # --------------------------------
    # 2. Vérifier que le provider existe
    # --------------------------------

    provider = await provider_repo.get_provider(
        provider_id
    )

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider not found.",
        )

    # --------------------------------
    # 3. Mettre à jour le rating global
    #    uniquement si un rating est fourni
    # --------------------------------

    if review.rating is not None:

        await provider_repo.update_provider_rating(
            provider_id=provider_id,
            rating=review.rating,
        )

    # --------------------------------
    # 4. Préparer la review
    # --------------------------------

    review_data = {
        "provider_id": provider_id,
        "user_id": user_object_id,
        "created_at": datetime.now(timezone.utc),
    }

    # Ajouter le rating uniquement s'il existe
    if review.rating is not None:
        review_data["rating"] = review.rating

    # Ajouter le commentaire uniquement s'il existe
    if review.comment:
        review_data["comment"] = review.comment

    # --------------------------------
    # 5. Enregistrer la review
    # --------------------------------

    created_review = await review_repo.create_review(
        review_data
    )

    # --------------------------------
    # 6. Analyser le commentaire avec Gemini
    # --------------------------------

    if review.comment:

        services = provider.get("services", [])

        if services:

            try:

                ai_result = await analyze_comment(
                    comment=review.comment,
                    services=services,
                )

                await apply_ai_service_ratings(
                    provider_id=review.provider_id,
                    ai_results=ai_result,
                )

            except Exception as exc:

                # L'analyse IA ne doit pas empêcher
                # la création de la review.

                print(
                    f"AI analysis failed: {exc}"
                )

    # --------------------------------
    # 7. Retourner la review créée
    # --------------------------------

    return created_review