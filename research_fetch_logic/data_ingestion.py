#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

import json 
import os 
import tiktoken 
from .ollama_embedding import get_embedding
from .open_search_client import get_opensearch_client


#----------------------------------------------------------------------------------------
#                                   Ingestion Logic
#----------------------------------------------------------------------------------------

def load_patent_data(dir_path):
    """
        Load patent data from a json file in the specified directory
        Args:
            dir_path(str) : path to the directory containnig the JSON file 
        Returns:
            list : a List of dict containing the patent data
    """

    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"The folder you wrote is not availbale")
    
    all_files = os.listdir(dir_path)
    chunks = [] 

    for file in all_files:
        if file.endswith(".json"):
            file_path = os.path.join(dir_path , file)
            with open(file_path , "r") as f:
                data = json.load(f)

            if data:
                title = data.get("title")
                pdf = data.get("pdf")
                publication_date = data.get("publication_date")
                patent_id = data.get("search_parameters", {}).get("patent_id", None)
                abstract = data.get("abstract", "")
                token_count = len(
                    tiktoken.encoding_for_model("gpt-3.5-turbo").encode(abstract)
                )
                embedding = get_embedding(abstract)

                chunks.append(
                    {
                        "title": title,
                        "pdf": pdf,
                        "publication_date": publication_date,
                        "patent_id": patent_id,
                        "abstract": abstract,
                        "token_count": token_count,
                        "embedding": embedding,
                    }
                )
    
    return chunks 


# Index opensearch data
def index_patent_data(client ,index_name , patent_data):
    """
        Index Patent Data to opensearch
        Args:
            client : Opensearch client instance.
            index_name : Name of the index to store the data
            patent_data : list of Dict containning patent data
    """
    for patent in patent_data:
        client.index(index=index_name , body = patent)
    print(f"Indexed {len(patent_data)} patents data into {index_name} index.")


def integrate_push_to_db():
    """
        Combining both of the above function to first make chunks
        and store that chunks into the database index.
        Required Folder:
            It will only rin right after the fetch. There should be results dir
            in this current directory in order to run this.
    """
    dir_path = "results"
    host = 'localhost'
    port = 9200
    client = get_opensearch_client(host , port)
    index_name = "patents"

    try:
        patent_data = load_patent_data(dir_path)
        print(f"Loaded {len(patent_data)} patents from '{dir_path}'")
        index_patent_data(client,index_name,patent_data)
        print(f"Indexed {len(patent_data)} patents into '{index_name}' index.")
    except Exception as e:
        print(f"Error : {e}")
        

#----------------------------------------------------------------------------------------
#                                 Checking Implementation
#----------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     dir_path = "results"
#     host = 'localhost'
#     port = 9200 
#     client = get_opensearch_client(host , port)
#     index_name = "patents"

#     try:
#         patent_data = load_patent_data(dir_path)
#         print(f"Loaded {len(patent_data)} patents from '{dir_path}'")
#         index_patent_data(client,index_name,patent_data)
#         print(f"Indexed {len(patent_data)} patents into '{index_name}' index.")
#     except Exception as e:
#         print(f"Error : {e}")



#results