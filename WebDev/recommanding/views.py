from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from neo4j import GraphDatabase
from WebDev.settings import driver
from ampligraph.utils import restore_model
from sklearn.neighbors import NearestNeighbors
import pickle
import pandas as pd

class RecommendingView(View):

    TEMPLATE = 'recommending.html'
    def __init__(self):
        np.random.seed(0)
        self.num_dimensions = 700

        self.df_merged = pickle_in('df_merged')

        self.song_hash = pickle_in('song_hash')
        self.y_pred = pickle_in('y_pred_user_8332014')
        self.unseen_predict = pickle_in('unseen_predict')
        #self.default_user_id = 'user_8332014'

        user_recommend_list = [(t_item[2], score) for t_item, score in zip(self.unseen_predict, self.y_pred)]
        self.user_recommend_list = sorted(user_recommend_list, key=lambda KV: KV[1], reverse=True)
        self.model = restore_model(model_name_path = './model/complex_model_opt_lf.pkl')
        pass

    def pickle_out(name, obj, default_path='./data/'):
        pickle_out = open(default_path + name + '.pickle','wb')
        pickle.dump(obj, pickle_out)
        pickle_out.close()
        return

    def pickle_in(name, default_path='./data/'):
        pickle_in = open(default_path + name + '.pickle','rb')
        obj = pickle.load(pickle_in)
        pickle_in.close()
        return obj

    @staticmethod
    def _get_movie_of(tx, name):
        """

        :param tx:
        :param name:
        :return:
        """
        movies = []
        result = tx.run("MATCH (a:Person)-[:ACTED_IN]->(f) "
                        "WHERE a.name = $name "
                        "RETURN f.title AS movie", name=name)
        for movie in result:
            movies.append(movie)
        return movies


    @staticmethod
    def _get_frist_25(tx):
        """

        :param tx:
        :return:
        """
        result = []
        r = tx.run("MATCH (n:Music) RETURN n.hasKeyword AS keyword, n.id AS id, n.hasTag as tag LIMIT 25")
        for record in r:
            temp = {'tagline': record['tag'], 'keyword': record['keyword'], 'id': record['id']}
            result.append(temp)
        return result



    def get(self, request):
        # to do, add music, add table
        with driver.session() as session:
            data = session.read_transaction(self._get_frist_25)

        return render(request, self.TEMPLATE, {'data': data})

    def get_recommend_by_user(self, request):

        k = request.data.get('k')
        #user_recommend_list is the list of song_id (recommendation)
        #if you need additional information of each song_id, then, 
        #you can search self.df_merged with the song_id
        #it will give you title, genre, # of listen, author, etc.
        return render(request, self.TEMPLATE, {'data': self.user_recommend_list[:k]})

    def get_recommend_by_song(self, request):
        # finding candidates list from the hash table
        track_id = request.data.get('track_id')
        k = request.data.get('k')

        recommend_list = None
        for key in self.song_hash.keys():
            if track_id in self.song_hash[key]:
                track_id_idx = self.song_hash[key].index(track_id)
                recommend_list = self.song_hash[key]
                break

        embedding_array = np.zeros((len(recommend_list), self.num_dimensions))
        for i, rec in enumerate(recommend_list):
            embedding_array[i, :] = self.model.get_embeddings(rec)

        # finding the k nearest neighbors
        nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(embedding_array)
        distances, indices = nbrs.kneighbors(embedding_array)
        nbrs_songs = [recommend_list[idx] for idx in indices[track_id_idx]]
        nbrs_songs.pop(nbrs_songs.index(track_id))

        #nbrs_songs is the list of song_id (recommendation)
        #if you need additional information of each song_id, then, 
        #you can search self.df_merged with the song_id
        #it will give you title, genre, # of listen, author, etc.
        return render(request, self.TEMPLATE, {'data': nbrs_songs[:k]})