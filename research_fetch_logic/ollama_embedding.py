#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------
import ollama


#----------------------------------------------------------------------------------------
#                                   Embedding Logic
#----------------------------------------------------------------------------------------

def get_embedding(query : str):
    """
        Give the embeddings for the give prompt
        Args:
            query(str) : the string or para which we want to make embeddings of 
        Returns:
            list of embedding vector 
    """

    # Invoke Ollama first in PC then this will work 
    try:
        # Init and getting the ollama response
        response = ollama.embed(
            model='nomic-embed-text',
            input=query
        )
        # Getting embeddings
        embeddings = response['embeddings'][0]
        return embeddings
    except Exception as e:
        print("Error in embeddings : ",str(e))


#----------------------------------------------------------------------------------------
#                                   Checking the Functionality
#----------------------------------------------------------------------------------------

# Just for a quick check
# if __name__ == "__main__":
#     sample_prompt = "The invention provides a lithium secondary battery including an ionic provider added to the positive electrode. The ionic provider does not involve in the electrochemical reaction of the lithium secondary battery during charging and discharging. The ionic provider can absorb thermal energy caused"
#     embeddings = get_embedding(sample_prompt)
#     print("Length :- ", len(embeddings))
#     print(embeddings)