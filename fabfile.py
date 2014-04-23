from fabric.api import local

def test_e2e():
    # This will run all E2E tests... when it works, for some reason it doesn't find any of the E2E tests
    #local('python manage.py test -a e2e --nologcapture')
    local('python manage.py test sparrow_bleu --nologcapture')
