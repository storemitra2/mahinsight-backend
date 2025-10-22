import numpy as np
from typing import List, Dict

try:
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class VectorRAGService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.use_transformer = SentenceTransformer is not None
        if self.use_transformer:
            self.model = SentenceTransformer(model_name)
        else:
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
        self.index = None
        self.texts = []
        self.metadata = []
        self.embeddings = None

    def build_index(self, texts: List[str], metadata: List[Dict]):
        self.texts = texts
        self.metadata = metadata
        if self.use_transformer:
            embeddings = self.model.encode(texts)
            self.embeddings = np.array(embeddings).astype('float32')
            if _HAS_FAISS:
                dim = self.embeddings.shape[1]
                self.index = faiss.IndexFlatIP(dim)
                self.index.add(self.embeddings)
            else:
                self.index = None
        else:
            # TF-IDF fallback
            self.embeddings = self.vectorizer.fit_transform(texts)
            self.index = None

    def search(self, query: str, k: int = 5):
        if self.embeddings is None:
            return []
        if self.use_transformer:
            q_emb = np.array(self.model.encode([query])).astype('float32')
            if self.index is not None and _HAS_FAISS:
                distances, indices = self.index.search(q_emb, k)
                results = []
                for idx, dist in zip(indices[0], distances[0]):
                    if idx < len(self.texts):
                        results.append({"text": self.texts[idx], "metadata": self.metadata[idx], "score": float(dist)})
                return results
            else:
                # Numpy brute force cosine
                def normalize(x):
                    norms = np.linalg.norm(x, axis=1, keepdims=True)
                    norms[norms == 0] = 1.0
                    return x / norms

                emb_norm = normalize(self.embeddings)
                q_norm = normalize(q_emb)
                scores = np.dot(emb_norm, q_norm.T).squeeze()
                topk_idx = np.argsort(-scores)[:k]
                results = []
                for idx in topk_idx:
                    results.append({"text": self.texts[idx], "metadata": self.metadata[idx], "score": float(scores[idx])})
                return results
        else:
            q_vec = self.vectorizer.transform([query])
            # cosine similarities via linear_kernel
            scores = linear_kernel(q_vec, self.embeddings).flatten()
            topk_idx = np.argsort(-scores)[:k]
            results = []
            for idx in topk_idx:
                results.append({"text": self.texts[idx], "metadata": self.metadata[idx], "score": float(scores[idx])})
            return results
