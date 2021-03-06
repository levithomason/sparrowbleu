import os
from django.core.management.base import NoArgsCommand
from subprocess import call


class Command(NoArgsCommand):
    help = 'Drop the database and create a fresh one'
        
    def handle_noargs(self, **options):
        # dropdb
        run(
            ['dropdb', '--if-exists', 'sbp'],
            'dropping db'
        )

        # create the db
        run(
            ['createdb', 'sbp'],
            'creating fresh db'
        )

        # sync db
        run(
            ['python', 'manage.py', 'syncdb', '--migrate', '--noinput'],
            'syncing db'
        )

        # make super user
        run(
            ['python', 'manage.py', 'superuser'],
            'making superuser'
        )

        write('=============================================')
        write("\n  It's on Donkey Kong!\n")


def run(command, friendly_output):
    write('...' + friendly_output)
    call(command)


def write(string):
    os.sys.stdout.write(string + '\n')
