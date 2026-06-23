#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

from opensearchpy import OpenSearch
from ollama_embedding import get_embedding


#----------------------------------------------------------------------------------------
#                                   Initializing Index
#----------------------------------------------------------------------------------------

def create_index_if_not_exists(client:OpenSearch , index_name):
    """
        Create an opensearch index with proper maping for vector search if its not there
        Args:
            client: Opensearch client instance
            index_name : str : Name of the index to create
    """

    # Delete the index if its already there
    if client.indices.exists(index=index_name):
        # We dont need to make another index
        print("Index is already Available...")
        return 
    
    else:    
        # If index is not there we have to make one...
        sample_embedding = "This is the sample text"
        dimensions = len(get_embedding(sample_embedding)) # e.g., 768
        print(f"Using embedding dimensions: {dimensions}")

        # Define the blueprint
        mappings = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "abstract": {"type": "text"},
                    "publication_date": {
                        "type": "date",
                        "format": "yyyy-MM-dd||yyyy||epoch_millis||strict_date_optional_time",
                    },
                    "patent_id": {"type": "keyword"},
                    "pdf": {"type": "keyword"},
                    "token_count": {"type": "integer"},
                    "embedding": {"type": "knn_vector", "dimension": dimensions},
                }
            },
            "settings": {
                "index": {
                    "knn": True,
                    "knn.space_type": "cosinesimil",  # Use cosine similarity for embeddings
                }
            },
        }

        # 4. Always create the index
        try:
            client.indices.create(index=index_name, body=mappings)
            print(f"Created index '{index_name}' successfully.")
        except Exception as e:
            print(f"Error creating index: {e}")
            raise


#----------------------------------------------------------------------------------------
#                                   Checking the Functionality
#----------------------------------------------------------------------------------------

# from open_search_client import get_opensearch_client

# if __name__ == "__main__":
#     # Get the client first 
#     client = get_opensearch_client("localhost" , 9200)
#     # Pass the client and the query to the function
#     create_index_if_not_exists(client=client , index_name= 'patents')