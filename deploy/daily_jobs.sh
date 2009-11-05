#!/bin/bash
# Run daily jobs

echo "** setting virtualenv **"
source /home/udbhav/ts-env/bin/activate
echo "** running daily jobs **"
python /home/udbhav/www/django/twinsister/src/manage.py runjobs daily

echo "** re-indexing search database **"
python /home/udbhav/www/django/twinsister/src/manage.py reindex

echo "** deactivating virtualenv **"
deactivate

echo "** daily jobs complete! **"