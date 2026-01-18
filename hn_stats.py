import requests
from datetime import datetime

HACKER_NEWS_URL_ROOT = "https://hn.algolia.com/api/v1/search"

def fetch_hn_stats(query):
    """
    Searches Hacker News via Algolia API and returns stats for posts matching the query.

    Args:
        query (str): Tool name or keyword to search.

    Returns:
        list[dict]: List of posts with points, author, post_date, number_of_comments, last_updated_comment_date.
    """
    
    # Stories between X and Y
    # http://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=created_at_i>X,created_at_i<Y`
    
    
    url = HACKER_NEWS_URL_ROOT
    params = {        
        #"numericFilters": 'created_at_i>1764590400,created_at_i<1768651200',  # DIDNT WORK
        #"dateEnd": 1768651200,
        #"dateRange": "custom",
        #"dateStart": 1764590400,
        #"page": 0,
        #"prefix": "false",
        "query": query,
        "tags": "story",
        "hitsPerPage": 20,  # Adjust if needed
        #"sort":"byPopularity"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for hit in data.get("hits", []):
        post = {
            "title": hit.get("title"),
            "points": hit.get("points", 0),
            "author": hit.get("author"),
            "post_date": datetime.fromtimestamp(hit.get("created_at_i")).isoformat() if hit.get("created_at_i") else None,
            "created_at_i" : hit.get("created_at_i"),
            "number_of_comments": hit.get("num_comments", 0),
            "last_updated_comment_date": None  # Placeholder
        }

        # If comments exist, find the latest comment timestamp
        comment_ids = hit.get("children", [])
        try:
            last_comment_ts = ""
            if comment_ids:
                # last_comment_ts = max([child.get("created_at_i", 0) for child in hit.get("_highlightResult", {}).get("children", []) if child])
                if last_comment_ts:
                    post["last_updated_comment_date"] = datetime.fromtimestamp(last_comment_ts).isoformat()
        finally:
            results.append(post)

    return results

# Example usage
if __name__ == "__main__":
    stats = fetch_hn_stats("ralph loop")
    import json
    print(json.dumps(stats, indent=2))
