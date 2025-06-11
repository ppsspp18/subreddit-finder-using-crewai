#!/usr/bin/env python
import sys
import warnings

import praw # python Reddit API Wrapper 
import os
import json
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime

from subreddit_finder.crew import SubredditFinder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def get_reddit_instance():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")
    
    if not all([client_id, client_secret, user_agent]):
        raise ValueError("Missing Reddit API credentials in .env file")

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

def search_subreddits(keyword, limit=10):
    reddit = get_reddit_instance()
    return list(reddit.subreddits.search_by_name(keyword, exact=False, include_nsfw=False))[:limit]

def get_result(topic):
    results = search_subreddits(topic)
    names = [sub.display_name for sub in results]
    #sub_list_str = ", ".join(names)
    return names #sub_list_str
'''
data in a json format
def fetch_and_store_subreddit_data(subreddit_name, post_limit=10, comment_limit=5, output_dir="reddit_data"):
    reddit = get_reddit_instance()

    try:
        subreddit = reddit.subreddit(subreddit_name)
        os.makedirs(output_dir, exist_ok=True)

        data = []

        for post in subreddit.new(limit=post_limit):
            post_data = {
                "title": post.title,
                "selftext": post.selftext,
                "url": post.url,
                "score": post.score,
                "id": post.id,
                "comments": []
            }

            post.comments.replace_more(limit=0)
            for comment in post.comments[:comment_limit]:
                post_data["comments"].append({
                    "body": comment.body,
                    "score": comment.score,
                    "id": comment.id
                })

            data.append(post_data)

        # Store as JSON
        filepath = os.path.join(output_dir, f"{subreddit_name}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Saved data to {filepath}")

    except Exception as e:
        print(f"Error fetching data for subreddit '{subreddit_name}': {e}")
'''

# fetching the newest posts and comments from a subreddit
def fetch_subreddit_data(subreddit_name, post_limit=5, comment_limit=3):
    reddit = get_reddit_instance()

    try:
        subreddit = reddit.subreddit(subreddit_name)
        data = []

        for post in subreddit.new(limit=post_limit):
            post_data = {
                "title": post.title,
                "selftext": post.selftext,
                "url": post.url,
                "score": post.score,
                "id": post.id,
                "comments": []
            }

            post.comments.replace_more(limit=0)
            for comment in post.comments[:comment_limit]:
                post_data["comments"].append({
                    "body": comment.body,
                    "score": comment.score,
                    "id": comment.id
                })

            data.append(post_data)

        return {subreddit_name: data}

    except Exception as e:
        print(f"Error fetching data for subreddit '{subreddit_name}': {e}")
        return {subreddit_name: []}


def run():
    """
    Run the crew.
    """
    print("---------------------------------------------------------------")
    print("Welcome to the Subreddit Finder!\n")
    topic_input = input("Enter a topic to search for subreddits: ")
    first_subreddit = input("Enter the subreddit to analyze: ")
    list_sub = get_result(topic_input)
    first_data = fetch_subreddit_data(first_subreddit)
    if first_subreddit in first_data:
       first_data[first_subreddit] = first_data[first_subreddit][2:]
    inputs = {
        'topic': topic_input,
        'list_sub': list_sub,
        'first_subreddit': first_subreddit,
        'first_data': first_data,
    }
    
    try:
        SubredditFinder().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        SubredditFinder().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SubredditFinder().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        SubredditFinder().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
if __name__ == "__main__":
    run()  
