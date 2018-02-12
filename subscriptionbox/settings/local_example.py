"""
These settings overrides the ones in settings/base.py
"""

SECRET_KEY = 'somestring'
# you can also use environment variables to store secret values
# import os
# SECRET_KEY = os.environ['SECRET_KEY']

INSTAMOJO = {
    'API_KEY': 'test_xxxxxx',
    'AUTH_TOKEN': 'test_xxxx',
    'SALT': 'testsalt',
    'TEST': True #Whether these are test.instamojo.com keys or live production ones
}
