import requests
import sys
import hashlib



def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again.')
    return response


def get_pw_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines()) # splits alle Zeilen an ':', gibt Tupel zurück
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return None


def pwned_api_check(password):
    # check passwort, if exists in API - response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_pw_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times. You should change your password.')
        else:
            print(f'{password} was not found!')
    return 'done!'
    
if __name__ == '__main__':
    main(sys.argv[1:])