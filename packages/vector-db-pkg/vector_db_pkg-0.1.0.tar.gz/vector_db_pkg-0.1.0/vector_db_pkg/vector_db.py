import faiss
import numpy as np

def build_vector_db(vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    return index

def save_vector_db(index, path):
    faiss.write_index(index, path)

def load_vector_db(path):
    return faiss.read_index(path)

def search_vector_db(index, query_vector, top_k=5):
    distances, indices = index.search(np.array([query_vector]), top_k)
    return distances, indices