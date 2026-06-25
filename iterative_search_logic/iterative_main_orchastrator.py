#----------------------------------------------------------------------------------------
#                                   Import statements
#----------------------------------------------------------------------------------------

from iterative_search_logic.iterative_search_function import iterative_function
from textwrap import dedent

#----------------------------------------------------------------------------------------
#                                   Function Logic statements
#----------------------------------------------------------------------------------------

def iterative_exploration(query : str , steps : int = 3):
    """
        Function will iterate and search query from database and take the top
        most result and add that to query and make new query using llm
        and then search again. This method will improve the search efficiency.
        Args:
            query(str) : User query
            steps(int) : No of steps need to perform
    """
    
    try:

        all_results, updated_queries = iterative_function(query, steps)

        # -----------------------------
        # Deduplicate results
        # -----------------------------
        seen = set()
        clean_results = []

        for r in all_results:
            src = r.get("_source", {})
            pid = src.get("patent_id")

            if pid and pid not in seen:
                seen.add(pid)
                clean_results.append(r)

        results = clean_results

        # -----------------------------
        # HEADER (NO INDENTATION BUG)
        # -----------------------------
        md = dedent(f"""
        # 🚀 Patent Intelligence Hub

        **Mode:** 🧠 Iterative Exploration Search  
        **Original Query:** `{query}`  
        **Iterations:** `{steps}`  
        **Results Found:** **{len(results)}**

        ---
        """)

        # -----------------------------
        # QUERY EVOLUTION
        # -----------------------------
        if updated_queries:

            md += dedent("""
            ## 🧭 Query Evolution

            """)

            for i, q in enumerate(updated_queries, start=1):

                if i == len(updated_queries):

                    md += dedent(f"""
                    **🎯 Final Query**

                    `{q}`

                    """)
                else:

                    md += dedent(f"""
                    **Step {i}**

                    `{q}`

                    ↓

                    """)

            md += "\n---\n\n"

        # -----------------------------
        # NO RESULTS CHECK
        # -----------------------------
        if not results:
            return md + "⚠️ No patents found."

        # -----------------------------
        # TOP MATCHES
        # -----------------------------
        md += dedent("""
        ## 🔍 Top Matches

        """)

        for i, hit in enumerate(results, start=1):

            src = hit.get("_source", {})

            title = src.get("title", "Untitled")[:80]
            score = round(hit.get("_score", 0), 3)
            pid = src.get("patent_id", "N/A")

            md += dedent(f"""
            **{i}. {title}**  
            🆔 `{pid}` | ⭐ `{score}`  

            """)

        md += "\n---\n\n"

        # -----------------------------
        # DETAILED RESULTS
        # -----------------------------
        md += dedent("""
        ## 📄 Detailed Results

        """)

        for i, hit in enumerate(results, start=1):

            src = hit.get("_source", {})

            title = src.get("title", "Untitled Patent")
            patent_id = src.get("patent_id", "N/A")
            date = src.get("publication_date", "N/A")
            score = round(hit.get("_score", 0), 3)

            abstract = src.get("abstract", "No abstract available.")
            abstract = abstract[:500] + "..." if len(abstract) > 500 else abstract

            md += dedent(f"""
            ---

            ### 🧾 {i}. {title}

            🆔 **Patent:** `{patent_id}`  
            📅 **Date:** `{date}`  
            ⭐ **Score:** `{score}`  

            🧠 **Abstract:**  
            {abstract}

            """)

        # -----------------------------
        # SAVE FILE (OPTIONAL BUT USEFUL)
        # -----------------------------
        with open("iterative_search_output.md", "w", encoding="utf-8") as f:
            f.write(md)

        return md

    except Exception as e:

        return dedent(f"""
        # ❌ Iterative Search Failed

        {str(e)}
        """)


if __name__ == "__main__":
    md = iterative_exploration(query = "Bio Fuel" , steps=3)