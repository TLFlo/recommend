from google import genai

from app.core.config import settings
from app.schemas.ia_schema import CommentAnalysis


client = genai.Client(
    api_key=settings.API_KEY
)


async def analyze_comment(
    comment: str,
    services: list[dict],
) -> CommentAnalysis:

    services_text = "\n".join(
        [
            f"""
            ID: {service["id"]}
            Nom: {service["name"]}
            Description: {service.get("description", "")}
            """
            for service in services
        ]
    )

    prompt = f"""
Tu es un système d'analyse de commentaires pour une plateforme
de recommandation de services.

Voici les services proposés par un établissement :

{services_text}

Voici le commentaire laissé par un utilisateur :

"{comment}"

Ta tâche :

1. Identifie uniquement les services réellement concernés
   par le commentaire.

2. Pour chaque service concerné, attribue un score :

   +2 = très positif
   +1 = positif
    0 = neutre
   -1 = négatif
   -2 = très négatif

3. Si le commentaire ne permet pas d'évaluer un service,
   ne retourne PAS ce service.

4. Utilise uniquement les IDs des services fournis.

5. N'invente jamais de service.

Retourne uniquement les données correspondant au schéma demandé.
"""

    response = await client.aio.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CommentAnalysis,
        },
    )

    return CommentAnalysis.model_validate_json(
        response.text
    )