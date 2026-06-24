#----------------------------------------------------------------------------------------
#                                   Import Statements
#----------------------------------------------------------------------------------------

from research_fetch_logic.open_search_client import get_opensearch_client
from search_patents_logic.retrival_methods import hybrid_search,keyword_search,semantic_search

#----------------------------------------------------------------------------------------
#                                   Function Logic statements
#----------------------------------------------------------------------------------------

def search_patents(query: str, search_option: int) -> str:
    """
    Clean, modern patent search UI (Streamlit Markdown)
    """

    try:
        client = get_opensearch_client("localhost", 9200)

        # -----------------------------
        # Select Search Type
        # -----------------------------
        if search_option == "1":
            search_type = "🔎 Keyword Search"
            results = keyword_search(query, client, 10)

        elif search_option == "2":
            search_type = "🧠 Semantic Search"
            results = semantic_search(query, client, 10)

        else:
            search_type = "⚡ Hybrid Search"
            results = hybrid_search(query, client, 10)

        # -----------------------------
        # Deduplicate results
        # -----------------------------
        seen = set()
        clean_results = []

        for r in results:
            src = r.get("_source", {})
            pid = src.get("patent_id")

            if pid and pid not in seen:
                seen.add(pid)
                clean_results.append(r)

        results = clean_results
        # print(results)

        # -----------------------------
        # HEADER (clean + compact)
        # -----------------------------
        md = f"""
# 📚 Patent Intelligence Hub

**Mode:** {search_type}  
**Query:** `{query}`  
**Results Found:** **{len(results)}**

---

"""

        if not results:
            return md + "⚠️ No patents found."

        # -----------------------------
        # 🔎 CLEAN LIST VIEW (IMPORTANT)
        # -----------------------------
        md += "## 🔍 Top Matches\n\n"

        for i, hit in enumerate(results, start=1):
            src = hit.get("_source", {})

            title = src.get("title", "Untitled")[:80]
            score = round(hit.get("_score", 0), 3)
            pid = src.get("patent_id", "N/A")

            md += f"""
**{i}. {title}**  
🆔 `{pid}` | ⭐ `{score}`  
"""

        md += "\n---\n\n"

        # -----------------------------
        # 📄 DETAILS (clean cards)
        # -----------------------------
        md += "## 📄 Detailed Results\n\n"

        for i, hit in enumerate(results, start=1):
            src = hit.get("_source", {})

            title = src.get("title", "Untitled Patent")
            patent_id = src.get("patent_id", "N/A")
            date = src.get("publication_date", "N/A")
            score = round(hit.get("_score", 0), 3)

            abstract = src.get("abstract", "No abstract available.")
            abstract = abstract[:500] + "..." if len(abstract) > 500 else abstract

            md += f"""
---

### 🧾 {i}. {title}

🆔 **Patent:** `{patent_id}`  
📅 **Date:** `{date}`  
⭐ **Score:** `{score}`  

🧠 **Abstract:**  
{abstract}

"""

        return md

    except Exception as e:
        return f"""
# ❌ Search Failed
{str(e)} """