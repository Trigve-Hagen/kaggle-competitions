# https://www.youtube.com/watch?v=E4l91XKQSgw

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
from pathlib import Path

script_dir = Path(__file__).parent
DATA = script_dir / "dataset" / "realistic_restaurant_reviews.csv"

df = pd.read_csv(DATA)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
  documents = []
  ids = []

  for i, row in df.iterrows():
    document = Document(
      page_content=row["Title"] + " " + row["Review"],
      metadata={"rating": row["Rating"], "date": row["Date"]},
      id=str(i)
    )
    ids.append(str(i))
    documents.append(document)

vectore_store = Chroma(
  collection_name="restaurant_reviews",
  persist_directory=db_location,
  embedding_function=embeddings
)

if add_documents:
  vectore_store.add_documents(documents=documents, ids=ids)

retriever = vectore_store.as_retriever(
  search_kwargs={"k": 5}
)

# https://ollama.com/download
# pip install pandas langchain langchain-ollama langchain-chroma
# used in langchain_rag1
