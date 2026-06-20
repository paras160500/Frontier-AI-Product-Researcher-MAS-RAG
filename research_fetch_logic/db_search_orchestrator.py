#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

from opensearchpy import OpenSearch
from db_index_initializer import create_index_if_not_exists
from hybrid_search_logic import hybrid_search
from open_search_client import get_opensearch_client

#----------------------------------------------------------------------------------------
#                                   Orchestrating Search
#----------------------------------------------------------------------------------------

def search_orchestrator(client : OpenSearch , query : str):
    
    # Check if there is namespace available or not and if not create one
    create_index_if_not_exists(client=client , index_name="patents")
    print("Got Query :- " , query)

    # Perform the Hybrid search on the vectorstore.
    chunks = hybrid_search(query=query,top_k=12)

    # Deciding wheather to call the serper or not
    if len(chunks) < 8:
        print("Call Serper API")
    else:
        top_score = chunks[0]['_score']
        second_top_score = chunks[1]['_score']
        diff = top_score - second_top_score
        print(top_score , second_top_score)

        if top_score < 0.9:
            print("+++++++++++---------------------------+++++++We have to call Serper")

        elif (top_score < 1.0 and diff < 0.15):
            print("+++++++++++++++++++++++++++++++++++++++++++++++++We have to call Serper")

        else:
            print("---------------------------------------------------------------------------OPEN SEARCH")


if __name__ == "__main__":
    client = get_opensearch_client("localhost" , 9200)
    search_orchestrator(client=client , query = "Condom Battery")