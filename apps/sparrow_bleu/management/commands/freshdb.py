import os
from django.core.management.base import NoArgsCommand
from subprocess import call
from django.db import DEFAULT_DB_ALIAS as database
from django.contrib.auth.models import User


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

        # drop user if exists
        run(
            ['psql', '-d', 'sbp', '-c DROP ROLE IF EXISTS postgres'],
            'dropping db user'
        )

        # create database super user
        run(
            ['psql', '-d', 'sbp', '-c', "CREATE ROLE postgres PASSWORD 'admin' SUPERUSER CREATEROLE CREATEDB LOGIN;"],
            'creating db user'
        )

        # sync db & make super user
        run(
            ['python', 'manage.py', 'syncdb', '--migrate', '--noinput'],
            'syncing db and making superuser'
        )
        create_super_user('admin', 'admin@sparrowbleuphotography.com', 'admin')

        write('=============================================')
        write("\n  It's on Donkey Kong!\n")


def run(command, friendly_output):
    write('...' + friendly_output)
    call(command)


def write(string):
    os.sys.stdout.write(string + '\n')


def create_super_user(name, email, password):
    User.objects.db_manager(database).create_superuser(name, email, password)
