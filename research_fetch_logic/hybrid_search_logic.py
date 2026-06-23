#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

from .open_search_client import get_opensearch_client
from .ollama_embedding import get_embedding


#----------------------------------------------------------------------------------------
#                                   Hybrid Search Logic 
#----------------------------------------------------------------------------------------

def hybrid_search(query : str , top_k = 20):
    """
        Perform semantic search using vector embeddings
        Args:
            query_text(str) : User Question
            tok_k(int) : How many top result you want

        Returns:
            list of searched results 
    """

    client = get_opensearch_client("localhost" , 9200)
    index_name = "patents"

    try:
        # Get embedding of the query
        query_embedding = get_embedding(query)

        # Create a hybrid search query
        search_query = {
            "size" : top_k,
            "query" : {
                "bool" : {
                    "should" : [
                        {"knn" : {"embedding" : {"vector" : query_embedding , "k" : top_k}}},
                        {"match" : {"abstract" : query}}
                    ]
                }
            },
            "_source" : ["title" , "abstract","publication_date","patent_id" , "claims","classifications","concepts" , "cited_by"]
        }

        response = client.search(index=index_name , body=search_query)
        return response['hits']['hits']
    except Exception as e:
        print("Hybrid Search Fail : " , str(e))
        
        # Fall back to keyword search
        try:
            fallback_query = {
                "size" : top_k,
                "query" : {"match" : {"abstract" : query}},
                "_source" : ["title" , "abstract","publication_date","patent_id" , "claims","classifications","concepts" , "cited_by"]
            }
            response = client.search(index = index_name , body=fallback_query)
            return response['hits']['hits']
        except Exception as e2:
            print(f"fallback search error : " , str(e2))
            return []
        

#----------------------------------------------------------------------------------------
#                                   Checking the Functionality
#----------------------------------------------------------------------------------------


# if __name__ == "__main__":
#     print("Searching the database..................")
#     chunks = hybrid_search(query="Condom Battery" , top_k=8)
#     print("Searching the database")
#     top_score = chunks[0]['_score']
#     second_top_score = chunks[1]['_score']
#     diff = top_score - second_top_score
#     print(top_score , second_top_score)

#     if top_score < 0.9:
#         print("+++++++++++---------------------------+++++++We have to call Serper")

#     elif (top_score < 1.0 and diff < 0.15):
#         print("+++++++++++++++++++++++++++++++++++++++++++++++++We have to call Serper")

#     else:
#         print("---------------------------------------------------------------------------OPEN SEARCH")
