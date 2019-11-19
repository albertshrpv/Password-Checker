# Passwort-Checker and Generator

Securely checks whether your password was previously exposed in data breaches. If so, it's unsuitable for ongoing usage, as hackers go through breched password lists while trying to take over accounts.
Using https://haveibeenpwned.com API.

If your password is unsafe you can automatically generate a new and safe one, where you can choose between alphanumeric passwords between 8 and 20 characters with at least one uppercase letter, one lowercase letter, three digits and whether you want to use special characters or not.


Checks as many passwords as you wish at once!

run:
python checkmypass.py "password to check" "password to check" ...

To learn more about password security visit https://haveibeenpwned.com !