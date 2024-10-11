from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
import torch

def vectorize_data(df, method="tfidf"):
    text_column = 'text_column'

    if method == "tfidf":
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(df[text_column]).toarray()

    elif method == "bert":
        # Load pre-trained BERT model and tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')

        # Tokenize and get embeddings
        tokens = tokenizer(df[text_column].tolist(), padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**tokens)
            vectors = outputs.last_hidden_state.mean(dim=1).numpy()

    else:
        raise ValueError("Unsupported vectorization method")

    return vectors