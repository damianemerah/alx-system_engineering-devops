#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""

import requests


def count_words(subreddit, word_list, count_dict=None):
    """ A function that queries the Reddit API parses the title of
    all hot articles, and prints a sorted count of given keywords
    (case-insensitive, delimited by spaces.
    Javascript should count as javascript, but java should not).
    If no posts match or the subreddit is invalid, it prints nothing.
    """

    if count_dict is None:
        count_dict = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    params = {"limit": 100}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = data.get("data", {}).get("children", [])

        if posts:
            for post in posts:
                title = post.get("data", {}).get("title", "").lower()

                for word in word_list:
                    if word.lower() in title:
                        count_dict[word] = count_dict.get(word, 0) + 1

            return count_words(subreddit, word_list, count_dict)

    sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].lower().split()
        count_words(subreddit, word_list)

