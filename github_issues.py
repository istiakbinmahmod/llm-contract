import requests
import csv

# Constants
GITHUB_TOKEN = "<GITHUB_TOKEN>"  # Replace with your token
REPO_OWNER = "meta-llama"  # Replace with the repository owner
REPO_NAME = "codellama"  # Replace with the repository name
OUTPUT_FILE = "github_issues_comments.csv"

# GitHub API URLs
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
ISSUES_URL = f"{BASE_URL}/issues"

# Headers for authentication
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

def fetch_issues_with_comments():
    """Fetches issues with comments from a GitHub repository."""
    page = 1

    while True:
        # Fetch issues (only open issues with pagination)
        response = requests.get(
            ISSUES_URL,
            headers=HEADERS,
            params={"state": "all", "per_page": 100, "page": page},
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            break  # Break if no more issues

        for issue in data:
            if issue.get("comments", 0) > 0:
                yield issue
        
        page += 1

def fetch_comments(issue_number):
    """Fetches comments for a given issue."""
    comments_url = f"{BASE_URL}/issues/{issue_number}/comments"
    page = 1

    while True:
        response = requests.get(
            comments_url,
            headers=HEADERS,
            params={"per_page": 100, "page": page},
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            break  # Break if no more comments
        
        yield from data
        page += 1

def write_to_csv(data, filename, headers):
    """Writes a row to a CSV file, appending if the file exists."""
    write_header = False
    try:
        with open(filename, 'r'):
            pass
    except FileNotFoundError:
        write_header = True

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if write_header:
            writer.writeheader()
        writer.writerow(data)

def main():
    # Define CSV headers
    headers = ["Issue Number", "Issue Title", "Issue Body", "Comment Author", "Comment Body"]

    # Process issues and write incrementally
    for issue in fetch_issues_with_comments():
        issue_number = issue["number"]
        issue_title = issue["title"]
        issue_body = issue["body"]

        for comment in fetch_comments(issue_number):
            data = {
                "Issue Number": issue_number,
                "Issue Title": issue_title,
                "Issue Body": issue_body,
                "Comment Author": comment["user"]["login"],
                "Comment Body": comment["body"],
            }
            write_to_csv(data, OUTPUT_FILE, headers)

if __name__ == "__main__":
    main()
