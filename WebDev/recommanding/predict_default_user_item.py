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


if __name__ == '__main__':
    default_user_id = 'user_8332014'
    df_triples = pickle_in('df_triples')
    model = restore_model(model_path = './model/complex_model_opt_lf.pkl')
    listened_list = df_triples[df_triples['s']==default_user_id]['o'].unique()
    total_song_list = df_triples[df_triples['p']=='listened']['o'].unique()
    not_listened_list = list(set(total_song_list) - set(listened_list))
    unseen_predict = [(user_id, 'listened', song) for song in not_listened_list]
    y_pred = model.predict(unseen_predict)

    pickle_out('y_pred_user_8332014', y_pred)