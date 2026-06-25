#----------------------------------------------------------------------------------------
#                                   Import statements
#----------------------------------------------------------------------------------------
from research_fetch_logic.open_search_client import get_opensearch_client
from openai import OpenAI
import os 
from dotenv import load_dotenv
load_dotenv()

#----------------------------------------------------------------------------------------
#                                   Function Logic statements
#----------------------------------------------------------------------------------------

def query_generator_using_llm(query : str , title : str):
    """
        Query generator using llm, It will take the query and title
        and make a new query to search efficiently in the database
        Args:
            query(str) : User Query
            title(str) : title of the topmost patent
    """
    client = OpenAI(api_key=os.getenv("OPEN_AI_API"))

    prompt = f"Combine into a short, efficient search query:\n{query}; {title}\nOutput only the query."

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # fast, lightweight model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,         # keep it short
        temperature=0.2        # low randomness for consistency
    )

    refined_query = response.choices[0].message.content.strip()
    return refined_query


def iterative_function(query : str , step : int):
    """
        Main function that perform iterative search
        Args:
            query(str) : User question
            step(int) : no of steps for search perform
        Returns:
            list : Results list of retrived patents.
    """
    
    # Initialize the variables
    client = get_opensearch_client("localhost", 9200)
    index_name = "patents"
    all_results = []
    updated_quries = []

    for i in range(step):
        try:
            # Perform Search Query
            search_query = {
                "size" : 5,
                "query" : {"match" : {"abstract" : query}},
                "_source" : ['title' , 'abstract' , 'publication_date' , 'patent_id']
            }

            response = client.search(index=index_name , body=search_query)
            results = response['hits']['hits']

            # Add new result
            if len(results) > 0:
                top_result = results[0]
                top_result_title = top_result['_source']['title']
                new_query = query_generator_using_llm(query , top_result_title)
                updated_quries.append(new_query)

                query = new_query
                print(f"Iteration {i+1}: Updated Query -> {new_query}")
                all_results = results[0:3]

        except Exception as e:
            print("Error in something..." , str(e))

    return all_results , updated_quries



# if __name__ == "__main__":
#     iterative_function("Lithium Battery" , 2)