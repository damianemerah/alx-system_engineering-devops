#!/usr/bin/python3
""" Module for a function that queries the Reddit API recursively."""

import requests

def count_words(subreddit, word_list, after=None, count={}):
    """ A function that queries the Reddit API parses the title of
    all hot articles, and prints a sorted count of given keywords
    (case-insensitive, delimited by spaces.
    Javascript should count as javascript, but java should not).
    If no posts match or the subreddit is invalid, it prints nothing.
    """

    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://www.reddit.com/r/' + subreddit + '/hot.json'
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'error' in data:
        print("Invalid subreddit or no posts found.")
        return

    posts = data['data']['children']
    for post in posts:
        title = post['data']['title'].lower()
        for word in word_list:
            count[word] = count.get(word, 0) + title.count(word.lower())

    after = data['data']['after']
    if after is None:
        sorted_count = sorted(count.items(), key=lambda x: (-x[1], x[0]))
        for word, frequency in sorted_count:
            print(word + ': ' + str(frequency))
        return

    count_words(subreddit, word_list, after, count)
