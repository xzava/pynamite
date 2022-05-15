# source credentials.sh

# This is used as an example, this should be moved outside of your project folder.

# REQUIRED..
export AWS_ACCESS_KEY_ID='XXXXXXX__YOUR_KEY__XXXXXXX' 
export AWS_SECRET_ACCESS_KEY='xxxxxxxxxxx__YOUR_SECRET__xxxxxxxxxxxxxx'
export AWS_REGION_NAME='us-east-1'
export DEBUG='development'

# OPTIONAL..
export DYNAMO_TABLE_NAME='TABLE_NAME' 
export AWS_DEFAULT_REGION='us-east-1'

echo "SUCCESS: AWS KEYS HAVE BEEN LOADED"