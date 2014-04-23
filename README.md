Setup
===========
1. Clone repo
2. Rename /settings/development(dot).py to development.py
    - *If you use virtualenvs make one now and activate it.*
3. Install the requirements `pip install -r <path_to_the_repo>/requirements.dev.txt`
4. Install jpeg support for PIL `brew install libjpeg`
5. Install PostgreSQL `brew install postgres`
    - *If you do not have homebrew: http://brew.sh/*
6. Create and sync a database: ```python manage.py freshdb```
    - *If you get libssl errors try [this blog post](http://joshuakehn.com/2013/10/13/Postgresapp-and-psycopg2-on-OS-X.html)*
    - *If you get postgres errors, make sure postgres is running!  Try `brew info postgres` for help*

**AWS Config**

Set the following AWS environment variables on virtualenv activate (remember to clear them on deactivate):
```
set AWS_ACCESS_KEY_ID=<your_s3_access_id>
set AWS_SECRET_ACCESS_KEY=<your_s3_secret_access_key>
set AWS_STORAGE_BUCKET_NAME=<your_s3_bucket_name>
```

# JavaScript Unit Testing

This project runs [Jasmine 2.0.0](https://github.com/pivotal/jasmine/).

Simply open the spec runner `tests/SpecRunner.html`


# Goals
The goal of this web app is to make online proofing galleries dead simple for both the photographer and client.  It will allow clients to select images from their photo shoots which they would like the photographer to further process.

## Photographer should be able to:

- Create price proofing galleries with
    - a name
    - a passcode
    - a number of images the client can choose to have processed
    - unlimited number of images

- Edit proofing galleries
    - Name, passcode, and number of selectable images
    - Add and delete images from the gallery

- Delete the entire gallery

- Drag and drop images from their desktop to the gallery add/edit form

## Client should be able to:

- Access a client access page with:
    - a passcode field
    - a "Go to gallery" button

- Enter a valid access code, click go to gallery and be taken directly to their private gallery craeted by the photographer

- Inside the Gallery
    - Click/Tap to choose images for further processing by the photographer
    - See which images they have selected
    - See the total number of images they can select
    - See how many images they have remaining to select
