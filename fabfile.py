from fabric.api import local

def test_e2e():
    local('python manage.py test --attr=e2e --nologcapture')
