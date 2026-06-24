from opensearchpy import OpenSearch
from research_fetch_logic.ollama_embedding import get_embedding

def keyword_search(query : str , client : OpenSearch , top_k : int = 20):
    """
        Perform Keyword search using OpenSearch.
        Args:
            query(str) : Query text to search for
            client(OpenSearch) : Client of the Database inorder to retrive the data
            top_k(int) : How many results we want from the DB
        Returns:
            list: Return a list of results
    """
    try:
        search_query = {
                    "size": top_k,
                    "query": {"match": {"abstract": query}},
                    "_source": [
                                    "title",
                                    "abstract",
                                    "publication_date",
                                    "patent_id"
                                ],
                }
        response = client.search(index="patents" , body=search_query)
        results = response['hits']['hits']
        return results
    except Exception as e:
        print("Error in the Keyword_seach Function : " , str(e))
        return []
    


def semantic_search(query : str , client : OpenSearch , top_k : int = 20):
    """
        Perfom Semantic Search using OpenSearch
        Args:
            query(str) : Query text to search for
            client(OpenSearch) : Client of the Database inorder to retrive the data
            top_k(int) : How many results we want from the DB
        Returns:
            list: Return a list of results
    """

    try:
        # Getting embedding for the query
        query_embedding = get_embedding(query)

        # Create Semantic Search Query
        search_query = {
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_embedding,
                        "k": top_k,
                    }
                }
            },
            "_source": [
                            "title",
                            "abstract",
                            "publication_date",
                            "patent_id"
                        ],
        }

        response = client.search(index="patents" , body=search_query)
        results = response['hits']['hits']
        return results
    except Exception as e:
        print("Error in Semantic Search Function : " , str(e))
        return []
    

def hybrid_search(query : str , client : OpenSearch , top_k : int = 20):
    """
        Perfom Semantic Search using OpenSearch
        Args:
            query(str) : Query text to search for
            client(OpenSearch) : Client of the Database inorder to retrive the data
            top_k(int) : How many results we want from the DB
        Returns:
            list: Return a list of results
    """
    try:
        # Getting embedding for the query
        query_embedding = get_embedding(query)

        # Create a hybrid search query
        search_query = {
            "size": top_k,
            "query": {
                "bool": {
                    "should": [
                        {"knn": {"embedding": {"vector": query_embedding, "k": top_k}}},
                        {"match": {"content": query}},
                    ]
                }
            },
            "_source": [
                            "title",
                            "abstract",
                            "publication_date",
                            "patent_id"
                        ],
        }

        response = client.search(index="patents" , body=search_query)
        return response['hits']['hits']
    except Exception as e:
        print("Error in Hybrid Search Function : " , str(e))
        return []