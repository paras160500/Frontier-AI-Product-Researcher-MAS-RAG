#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

import os 
from dotenv import load_dotenv
from open_search_client import get_opensearch_client
from db_search_orchestrator import search_orchestrator

load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

#----------------------------------------------------------------------------------------
#                                   Main_orchastrator func
#----------------------------------------------------------------------------------------

def main_orchastrator(query : str):

    # First Lets have the database connection client object
    client = get_opensearch_client("localhost" , 9200)
    
    # Lets check wheather the query have simmilar chunks in the database already or not
    search_orchestrator(client = client , query = query)

if __name__ == "__main__":
    main_orchastrator("Lithium Battery")