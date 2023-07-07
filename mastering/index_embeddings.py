from annoy import AnnoyIndex
import glob
import json
from mastering import constants
from mastering import feature_embedding
from mastering import audio_utils


class IndexEmbeddings:
    def __init__(self, n):
        self.n = n

    def create_index(self):
        """
        creates an index file for embeddings of the reference tracks in dir mastered_embeddings
        creates a json file mapping the indexes to the file names in dir mastered_embeddings
        :return:
        """
        t = AnnoyIndex(self.n, 'euclidean')
        name_index_mapping = {}

        for i, filepath in enumerate(glob.iglob('../tracks/reference_tracks/*.mp3')):
            audio, sr = audio_utils.load_audio_file(filepath)
            audio, _ = audio_utils.preprocess_audio(audio, sr, constants.DURATION)
            feature_vector = feature_embedding.FeatureEmbedding(audio, sr).feature_vector
            t.add_item(i, feature_vector)
            name_index_mapping[i] = filepath

        with open(constants.PATH_TO_MASTERED_EMBEDDINGS + '/name_index_mapping.json', 'w') as f:
            json.dump(name_index_mapping, f)

        t.build(10)
        t.save(constants.PATH_TO_MASTERED_EMBEDDINGS + '/embed.ann')

    def find_closest(self, audio, sr, n_closest):
        """
        finds the n_closest reference tracks to the audio file at path_to_audio
        :param audio: np array of mono audio to which closest reference should be found
        :param n_closest: number of closest reference tracks to find
        :return: list of names of closest reference tracks
        """
        u = AnnoyIndex(self.n, 'euclidean')
        u.load(constants.PATH_TO_MASTERED_EMBEDDINGS + '/embed.ann')

        new_vector = feature_embedding.FeatureEmbedding(audio, sr).feature_vector

        closest_indices = u.get_nns_by_vector(new_vector, n_closest)

        with open(constants.PATH_TO_MASTERED_EMBEDDINGS + '/name_index_mapping.json', 'r') as f:
            name_index_mapping = json.load(f)

        return [name_index_mapping[str(i)] for i in closest_indices]

#IndexEmbeddings(38).create_index()