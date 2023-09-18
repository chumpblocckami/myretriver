from langchain.embeddings import HuggingFaceEmbeddings

hf_embedding_functions = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": False},
)
