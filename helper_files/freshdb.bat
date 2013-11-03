@echo off

echo Dropping databse...
dropdb -U postgres sbp

echo Removing gallery images...
rm /cygdrive/c/Users/Levi/projects/sbp/mediafiles/gallery_images/*

echo Removing gallery images directory...
rmdir C:\Users\Levi\projects\sbp\mediafiles\gallery_images

echo Creating new database...
createdb -U postgres -O postgres -T postgres -E UTF8 sbp

echo Syncing and migrating...
python ./manage.py syncdb --migrate --noinput

echo Creating admin/admin superuser...
echo from django.contrib.auth.models import User; su = User.objects.create_superuser('admin', 'admin@sparrowbleuphotography.com', 'admin'); exit() | python ./manage.py shell


echo -------------------------
echo Rock n' Roll Donkey Kong!