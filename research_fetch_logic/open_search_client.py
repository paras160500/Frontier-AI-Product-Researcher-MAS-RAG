
#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

from opensearchpy import OpenSearch


#----------------------------------------------------------------------------------------
#                                   Get Client function
#----------------------------------------------------------------------------------------

def get_opensearch_client(host , port):
    """
        Get cleint of the opensearch
        Args:
            host: The host we want to give 
            port : Port number 
        Returns:
            Returns the client object
    """
    client = OpenSearch(
        hosts=[{'host' : host , "port" : port}],
        http_compress = True,
        timeout = 30,
        max_retries = 3,
        retry_on_timeout = True
    )

    # Check wheather we can ping or not
    if client.ping():
        print("Connected to opensearch")
        info = client.info()
        print(f"Cluster name : {info['cluster_name']}")
        print(f"Opensearch version : {info['version']['number']}")
    else:
        print("Connection Failed")
        raise ConnectionError("failed to connect to Opensearch")
    
    # Returning the client back
    return client