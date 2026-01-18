import requests
import json

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"  # Replace with your token
GITHUB_REPO_URL = "chrismdp/ralph"
GRAPHQL_URL = "https://api.github.com/graphql"

REPO_STATS_QUERY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    createdAt
    stargazerCount
    watchers {
      totalCount
    }
    forkCount
    defaultBranchRef {
      target {
        ... on Commit {
          history {
            totalCount
          }
        }
      }
    }
  }
}
"""

def fetch_github_repo_data(repo_full_name: str):
    """Makes the GraphQL API request and returns the raw data."""
    try:
        owner, name = repo_full_name.split("/")
    except ValueError:
        raise ValueError("Repo name must be in 'owner/repo' format")
    
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    variables = {"owner": owner, "name": name}
    
    response = requests.post(GRAPHQL_URL, headers=headers, json={"query": REPO_STATS_QUERY, "variables": variables})
    
    if response.status_code != 200:
        raise Exception(f"GitHub API query failed: {response.text}")
    
    return response.json()["data"]["repository"]

def parse_repo_stats(raw_data):
    """Parses raw GitHub repository data into a clean JSON object."""
    return {
        "Date Created": raw_data["createdAt"],
        "Commits": raw_data["defaultBranchRef"]["target"]["history"]["totalCount"] if raw_data["defaultBranchRef"] else 0,
        "Stars": raw_data["stargazerCount"],
        "Watchers": raw_data["watchers"]["totalCount"],
        "Forks": raw_data["forkCount"]
    }

def get_github_repo_stats(repo_full_name: str):
    raw_data = fetch_github_repo_data(repo_full_name)
    parsed_data = parse_repo_stats(raw_data)
    return json.dumps(parsed_data, indent=2)

# Example usage:
print(get_github_repo_stats(GITHUB_REPO_URL))
