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
    