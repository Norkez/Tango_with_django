import os
import json
import urllib.parse
import urllib.request

def read_webhose_key():
    """
    'search.key'라는 파일로부터 Webhose API 키를 읽어온다.
    None 이나 key 문자열을 반환함.
    search.key를 .gitignore 파일에 포함하도록.
    """

    webhose_api_key = None

    try:
        if os.path.isfile("search.key"):
            with open('search.key', 'r') as f:
                webhose_api_key = f.readline().strip()
        else:
            with open('../search.key', 'r') as f:
                webhose_api_key = f.readline().strip()

    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    """
    Given a string contatining search terms (query), and a number of results to
    return (default of 10), returns a list of results from the Wehose API,
    with each result consisting of a title, link and summary.
    """
    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'

    query_string = urllib.parse.quote(search_terms)

    search_url = ('{root_url}?token={key}&format=json&q={query}'
                    '&sort=relevancy&size={size}').format(
                        root_url=root_url,
                        key=webhose_api_key,
                        query=query_string,
                        size=size)
    results = []

    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    return results

if __name__ == "__main__":
    search_terms = input("Please write search terms: ")
    results = json.dumps(run_query(search_terms, size=10))
    try:
        with open('results.txt', 'w') as f:
            f.write(results)
        print("'results.txt' saved successfuly.")
    except:
        Print("error occured.")

    