from fabric.api import local

def test_e2e():
    local('python manage.py test --attr=e2e --nologcapture')

def deploy():
    # run tests
    # run e2e tests
    # run jasmine tests
    # run pep8
    # git push
    # git push heroku master
    pass
