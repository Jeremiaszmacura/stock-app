if [ ${ENV} = "DEV" ] ; then
    pip install --no-cache-dir -r requirements-dev.txt
if [ ${ENV} = "PROD" ] ; then
    pip install --no-cache-dir -r requirements.txt
else
    pip install --no-cache-dir -r requirements-dev.txt
fi
