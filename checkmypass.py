import requests
import sys
import hashlib
import secrets
import string


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {response.status_code}, check the api and try again.')
    return response


def get_pw_leaks_count(hashes, hash_to_check):
    # splits alle Zeilen an ':', gibt Tupel zurück
    hashes = (line.split(':') for line in hashes.text.splitlines())
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
            print(
                f'{password} was found {count} times. You should change your password.')

            x = input('Generate safe password? (y/n):  ')
            while x != 'n' and x != 'y':
                print('Invalid input.')
                x = input('Generate safe password? (y/n):  ')
            else:
                if(x == 'n'):
                    break
                else:
                    chars = int(input('How many characters? (8-20)  '))
                    while chars < 8 or chars > 20:
                        print('Invalid length.')
                        chars = int(input('How many characters? (8-20)  '))
                    else:
                        special_chars = input(
                            'Use special characters? (y/n)  ')
                        while special_chars != 'n' and special_chars != 'y':
                            print('Invalid input.')
                            special_chars = input(
                                'Use special characters? (y/n)  ')
                        else:
                            if special_chars == 'y':
                                new_pw = generate(chars, 1)
                                while pwned_api_check(new_pw):
                                    new_pw = generate(chars, 1)
                                print(new_pw)
                            else:
                                new_pw = generate(chars, 0)
                                while pwned_api_check(new_pw):
                                    new_pw = generate(chars, 0)
                                print(new_pw)

        else:
            print(f'{password} was not found!')
    return 'done!'


def generate(length, special_chars):

    alphabet_an = string.ascii_letters + string.digits
    special_characters = r"_.*-+:#!?%{}|@[];=“&$\/,()"
    alphabet_sc = string.ascii_letters + string.digits + r"_.*-+:#!?%{}|@[];=“&$\/,()"


    if special_chars:
        while True:
            password = ''.join(secrets.choice(alphabet_sc) for i in range(length))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3
                    and any(c in special_characters for c in password)):
                break
    else:
        while True:
            password = ''.join(secrets.choice(alphabet_an) for i in range(length))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break

    return password


if __name__ == '__main__':
    main(sys.argv[1:])
    