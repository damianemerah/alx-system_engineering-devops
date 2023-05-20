#!/usr/bin/python3

import requests

def count_words(subreddit, word_list, after=None, count_dict={}):
    url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()
        posts = data.get('data', {}).get('children', [])
        for post in posts:
            title = post.get('data', {}).get('title', '').lower()
            for word in word_list:
                count = title.count(word.lower())
                if count > 0:
                    count_dict[word] = count_dict.get(word, 0) + count

        after = data.get('data', {}).get('after')
        if after:
            count_words(subreddit, word_list, after, count_dict)
        else:
            sorted_counts = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print('{}: {}'.format(word, count))
    else:
        print('Invalid subreddit or unable to fetch data.')

# Example usage:
count_words('programming', ['react', 'python', 'java', 'javascript', 'scala', 'no_results_for_this_one'])
