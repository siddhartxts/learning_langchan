import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import CharacterTextSplitter
from langchain_unstructured import UnstructuredLoader

load_dotenv()

if __name__ == "__main__":

    loader = UnstructuredLoader(file_path="/Users/siddharth/Desktop/langchain-course-main/mediumblog1.txt", chunking_strategy="basic", max_characters=1000000)
    document = loader.load()


    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        dimensions=512,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    )

    print(f"using embedding model: {embeddings.model} (dimensions={embeddings.dimensions})")
    sample_vector = embeddings.embed_query("dimension check")
    print(f"sample embedding has {len(sample_vector)} dimensions")

    index_name = os.environ["INDEX_NAME"]
    print(f"ingesting into Pinecone index: {index_name}")

    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=index_name
    )

