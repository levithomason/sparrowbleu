import sys
from fabric.api import local, hide

def test():
    local('python manage.py test --attr=!e2e')

def test_e2e():
    local('python manage.py test --attr=e2e --nologcapture')

def push():
    local('git push')

def push_heroku():
    local('git push heroku master')

def deploy():
    print "%" * 80
    print " Deploying Sparrow Bleu, me lord!"
    print "%" * 80
    print ""

    with hide('running', 'output', 'stdout'):
        _fancy_output("Running python unit tests", test)
        _fancy_output("Running python E2E tests", test_e2e)

        # run jasmine tests
        # run pep8

        _fancy_output("Pushing to GitHub", push)
        _fancy_output("Pushing to Heroku", push_heroku)

def _fancy_output(message, func):
    sys.stdout.write("%s..." % message)
    func()
    print "done"
