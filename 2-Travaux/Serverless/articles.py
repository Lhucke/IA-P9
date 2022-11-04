# Import des librairies
import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

# Classe des modèles des réseaux de neurones pour l'analyse du texte
class ContentBased:
    
    # Initialisation
    def __init__(self, embeddings, clicks):
        self.articles_embeddings = pd.read_pickle(embeddings)
        self.clicks = pd.read_pickle(clicks)
    
    # Sort un dataframe comprenant les 5 articles les plus proches de l'article ainsi que leur score
    def get_best_articles(self, id_article):
        similarities = np.squeeze(cosine_similarity(self.articles_embeddings.to_numpy()[:,:], self.articles_embeddings.to_numpy()[id_article,:].reshape(1, 30)))
        indices_max = np.argsort(-similarities)[1:6]
        return pd.DataFrame([indices_max, similarities[indices_max]], index=['article', 'score'])

    # Obtient les recommandations pour un utilisateur
    def get_recommendations(self, user_id):
        # Liste des articles vus par un utilisateur
        user_articles = self.clicks.loc[self.clicks['user_id']==int(user_id)]['click_article_id']

        # Création du dataframe contenant les recommandations
        df_best_articles = pd.DataFrame()

        # Parcours des articles vus par l'utilisateur
        for i, article in user_articles.iteritems():
            # Récupère 5 plus proches articles et les concatène dans un df
            df = self.get_best_articles(article)
            df_best_articles = pd.concat([df_best_articles, df], axis=1)

        # Tri de tous les articles de l'utilsateur selon leur score
        df_best_articles.sort_values(by=['score'], axis=1, ascending=False)
        df_best_articles.columns = range(len(df_best_articles.columns))

        # Liste des 5 meilleures recommandations 
        results = []
        i = 0
        j = 0
        while j < 5:
            if  not df_best_articles[i]["article"] in user_articles.unique():
                results.append(int(df_best_articles[i]["article"]))
                j = j + 1
            i = i + 1
        return json.dumps(results)