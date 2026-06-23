#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

import os,requests,json

#----------------------------------------------------------------------------------------
#                                   Main logic
#----------------------------------------------------------------------------------------

def fetch_insider_func(main_data : json):
    """
        fetch the top three result from the main_data
        It will fetch the first or top three patens from the main_data 
        (Ultimately main data have 10 patent)
        Args:
            main_data(json) : JSON data from the response of the URL.
        Returns:
            will return the top three patents from the top result of the main_data
    """
    top_3_results = []
    patents = main_data.get("organic_results")
    if len(patents) > 3:
        for i in range(3):
            top_3_results.append(patents[i])
        # print("Got 3 results and returning to the main")
        return top_3_results
    else:
        raise ValueError("Cant get organic result from the data")

def get_serpapi_url(data):
    """
        Construct the serp api URL from the provided data
        Args:
            data(dict) : The data containing the serpapi url
        Returns:
            Complete serpapi url with the serpapi key as well
    """
    
    # Get the url from the data 
    serpapi_url = data['serpapi_link']
    api_key = os.getenv("SERPER_API_KEY")

    # Add Api key to URL if its not present
    if "api_key=" not in serpapi_url:
        seperator = "&" if "?" in serpapi_url else "?"
        serpapi_url = f"{serpapi_url}{seperator}api_key={api_key}"
        # print("-"*60)
        # print(serpapi_url)

    return serpapi_url


def get_data_and_save_to_file(url : str , count : int , file_abb : str):
    """
        Fetach data with serpapi_link and save as file
        Args:
            url(str) : Link of the patent_metadata + apikey of serper
            count(int) : For tracking the file count
            file_abb(str) : name diffrentiater
        Returns:
            count , response(coming from the URL)
    """
    try:
        response = requests.get(url)
    except Exception as e:
        raise ValueError("Error in save_data for fetching the data from url" , str(e))
    # Convert data into JSON
    try:
        os.makedirs("results" , exist_ok=True)
    except Exception as e:
        print("Error in Directory making")
    try:
        with open(f"results/{file_abb}_{count}.json" , "w") as f:
            json.dump(response.json() , f , indent=2) 
            count += 1
            # print("f{count} file save")
            return count , response.json()
    except Exception as e:
        raise ValueError("Error in file write...." , str(e))