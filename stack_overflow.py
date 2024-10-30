import requests
import csv

# CSV_FILENAME = 'stackoverflow.csv'

# STACK_OVERFLOW_TAGS = ["llama", "huggingface-transformers", "camel", "vicuna", "guanaco"]
STACK_OVERFLOW_TAGS = ["openai-api"]


class Criteria:
    SCORE = "score"
    IS_ANSWERED = "is_answered"
    ANSWER_COUNT = "answer_count"


class CriteriaValue:
    SCORE = 5
    IS_ANSWERED = True
    ANSWER_COUNT = 1


def fetch_stackoverflow_posts(tag, pagesize=10, page=1):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "activity",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": pagesize,
        "page": page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def filter_stackoverflow_posts(posts):
    filtered_posts = []
    for post in posts["items"]:
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
    with open(filename, mode="a") as file:
        writer = csv.writer(file)
        for post in posts:
            writer.writerow([post["title"], post["link"]])


def main():
    for tag in STACK_OVERFLOW_TAGS:
        query = f"https://api.stackexchange.com/2.3/tags/{tag}/info?site=stackoverflow"
        response = requests.get(query)
        if response.status_code == 200:
            if len(response.json()["items"]):
                count = response.json()["items"][0]["count"]
            else:
                count = 0
            if count > 0:
                page_count = 20
                pagesize = count // page_count
                page = 1
                posts = []
                filtered_posts = []
                while True:
                    posts = fetch_stackoverflow_posts(tag, pagesize, page)
                    if posts["has_more"] == False:
                        break
                    filtered_posts.extend(filter_stackoverflow_posts(posts))
                    page += 1
                write_to_csv(filtered_posts, f"{tag}.csv")

            print(f"Tag: {tag}")
            print(f"Count: {count}")
        else:
            response.raise_for_status()


if __name__ == "__main__":
    main()
