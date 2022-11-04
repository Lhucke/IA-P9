import azure.functions as func
from articles import ContentBased

# API, récupère id, appelle modèle et retourne les articles suggérés
def main(req: func.HttpRequest, embeddings, clicks) -> func.HttpResponse:

    model = ContentBased(embeddings, clicks)
    user_id = req.params.get('user_id')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('user_id')

    if user_id:
        articles = model.get_recommendations(user_id) 
        return articles
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
