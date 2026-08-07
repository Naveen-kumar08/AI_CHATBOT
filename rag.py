import chromadb
from embeddings import create_embedding


client = chromadb.PersistentClient(
    path="vectors"
)


collection = client.get_or_create_collection(
    name="documents"
)



def add_document(text):

    chunks = split_text(text)


    for i, chunk in enumerate(chunks):

        vector = create_embedding(
            chunk
        )


        collection.add(
            ids=[str(i)],
            embeddings=[vector],
            documents=[chunk]
        )



def split_text(
    text,
    size=500
):

    words = text.split()

    chunks=[]

    for i in range(
        0,
        len(words),
        size
    ):

        chunks.append(
            " ".join(
                words[i:i+size]
            )
        )


    return chunks



def search_document(
    query,
    count=3
):

    query_vector = create_embedding(
        query
    )


    result = collection.query(
        query_embeddings=[
            query_vector
        ],
        n_results=count
    )


    return result["documents"][0]