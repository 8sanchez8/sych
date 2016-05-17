from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import getpass
import re


class Command(BaseCommand):
    help = 'Creates a new user'

    def handle(self, *args, **options):

        username = raw_input('Enter username: ')
        while True:
            first_password = getpass.getpass(prompt='Enter password: ')
            if not len(first_password) >= 6:
                print('The password must be 6 characters or longer.\n')
                continue
            if not re.search(r'[A-Z]', first_password):
                print('The password must contain at least one upper character.\n')
                continue
            if not re.search(r'[a-z]', first_password):
                print('The password must contain at least one lower character.\n')
                continue
            if not re.search(r'[0-9]', first_password):
                print('The password must contain at least one number.\n')
                continue

            second_password = getpass.getpass(prompt='Enter password again: ')
            if first_password != second_password:
                print('Passwords don''t match.\n')
                continue
            break
        user = User.objects.create_user(username, password=second_password)
        user.save()
        self.stdout.write(self.style.SUCCESS('User created'))

