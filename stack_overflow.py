import requests
import csv

CSV_FILENAME = 'stackoverflow.csv'

class Criteria:
    SCORE = 'score'
    IS_ANSWERED = 'is_answered'
    ANSWER_COUNT = 'answer_count'

class CriteriaValue:
    SCORE = 5
    IS_ANSWERED = True
    ANSWER_COUNT = 2

def fetch_stackoverflow_posts(tag, pagesize=10, page=1):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        'order': 'desc',
        'sort': 'activity',
        'tagged': tag,
        'site': 'stackoverflow',
        'pagesize': pagesize,
        'page': page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def filter_stackoverflow_posts(posts):
    filtered_posts = []
    for post in posts['items']:
        if post[Criteria.SCORE] < CriteriaValue.SCORE:
            continue
        if post[Criteria.IS_ANSWERED] != CriteriaValue.IS_ANSWERED:
            continue
        if post[Criteria.ANSWER_COUNT] < CriteriaValue.ANSWER_COUNT:
            continue
        filtered_posts.append(post)
    return filtered_posts

def write_to_csv(posts, filename):
    # Find if the file exists
    # If it does, append to it
    # If it doesn't, create it and write to it
    with open(filename, mode='a') as file:
        writer = csv.writer(file)
        for post in posts:
            writer.writerow([post['title'], post['link']])

def main():
    tag = 'llama'  # Change this to your desired tag
    # iterate over pages
    page = 1
    while True:
        posts = fetch_stackoverflow_posts(tag, pagesize=100, page=page)
        filtered_posts = filter_stackoverflow_posts(posts)
        write_to_csv(filtered_posts, CSV_FILENAME)
        if not posts['has_more']:
            break
        print(f"Page: {page}")
        page += 1

if __name__ == "__main__":
    main()