#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

import os , requests
from .serper_helper import get_data_and_save_to_file,get_serpapi_url,fetch_insider_func


#----------------------------------------------------------------------------------------
#                                   Main Logic
#----------------------------------------------------------------------------------------

def get_and_save_data_from_query(query : str):
    """
        Function will find the query on the web and then get the raw data from them and also
        fetch the data from the patent citation from that particualar source.
        Args:
            query(str) : 
        Returns:
            Nothin, but store the file in the system.
    """
    count = 0
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    url = f"https://serpapi.com/search?engine=google_patents&q={query}&api_key={SERPER_API_KEY}"

    # Getting the response from the main URL
    try:
        main_response = requests.get(url)
    except Exception as e:
        print("Cant get data from the main URL :- " , str(e))
        raise ValueError("Cant Decode the main Response from the url")
    if main_response.status_code == 200:
        try:
            # go inside the data to get detailed data
            main_url_data = main_response.json()
            
            top_3_result = fetch_insider_func(main_url_data)
            tp_count = 0
            for tp3 in top_3_result:
                tp_count += 1
                # Main condition to break the loop and exit 
                if count == 11:
                    return

                # Go inside the main result to get the top3
                main_result_serp_url = get_serpapi_url(tp3)
                count , content_data  = get_data_and_save_to_file(main_result_serp_url , count=count , file_abb=f"patent_data__{tp_count}")

                # Go inside each of the patent for citations patent content 
                citation_arr = content_data.get("patent_citations",{}).get("original" , {})
                
                if len(citation_arr) >= 1:
                    temp = 0
                    for cit in citation_arr:
                        # print(f"For {tp_count} Patent######################################")
                        if count < 11:
                            if temp < 3:
                                citation_serp_url = get_serpapi_url(cit)
                                count , _ = get_data_and_save_to_file(citation_serp_url , count , f"citaion_data__{tp_count}")
                                temp += 1
                            else:
                                break
                        else:
                            return
                # print("============Total File Added :- " , count)
        except Exception as e:
            print("Error in converting data to JSON from main url : " , str(e))
            return 
    else:
        raise ValueError("Response Status code is not 200!!")
    

#----------------------------------------------------------------------------------------
#                                   Main Logic
#----------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     get_and_save_data_from_query(query="Lithium Battery")