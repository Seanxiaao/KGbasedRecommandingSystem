from django.test import TestCase
import pickle
import numpy as np
from ampligraph.utils import restore_model

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

def side_of_plane_matrix(P, v):
    dotproduct = np.dot(P, v.T)
    sign_of_dot_product = np.sign(dotproduct)
    return sign_of_dot_product

def hash_multi_plane_matrix(P, v, num_planes):
    sides_matrix = side_of_plane_matrix(P, v) # Get the side of planes for P and v
    hash_value = 0
    for i in range(num_planes):
        sign = sides_matrix[i].item() # Get the value inside the matrix cell
        hash_i = 1 if sign >=0 else 0
        hash_value += 2**i * hash_i # sum 2^i * hash_i
    return hash_value


if __name__ == '__main__':

    np.random.seed(0)
    num_dimensions = 700
    num_planes = 25
    total_song_list = pickle_in('total_song_list')
    model = restore_model(model_path = './model/complex_model_opt_lf.pkl')

    random_planes_matrix = np.random.normal(size=(num_planes, num_dimensions))

    song_hash = {}
    for song in total_song_list:
        v = model.get_embeddings([song])
        hash_value = hash_multi_plane_matrix(random_planes_matrix, v, num_planes)
        if hash_value in song_hash:
        song_hash[hash_value].append(song)
        else:
            song_hash[hash_value] = [song]

    pickle_out('song_hash', song_hash)
