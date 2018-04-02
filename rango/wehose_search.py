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
        with open('search.key', 'r') as f:
            webhose_api_key = f.readline().strip()
    
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, szie=10):
    """
    """
    webhose_api_key = read_webhose_key

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'

    query_string = urllib.parse.quote(search_terms)

    search_url = ('{root_url}?token={key}&foramt=json&q={query}'
                    '&sort=relevancy&size={size}').foramt(
                        root_url=root_url,
                        key=webhose_api_key,
                        query=query_string,
                        size=size)
    results = []

    try:
        reponse = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    return results
    