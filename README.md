# Title: DynamoDB util code

### Description: This code was used in another project this folder is an attempt to extract it so it can be used in other places.

Note: The following ENV are expected.

`AWS_ACCESS_KEY_ID`
`AWS_SECRET_ACCESS_KEY`
`DYNAMO_TABLE_NAME`

```
source ~/work/Keys/AWS_auth_microservice.sh
```


boto3 library is needed


from boto3.dynamodb.conditions import Key, Attr



dynamo.py is the enterpoint

```
import dynamo
db = dynamo.DB('USER')
```


db.table.query(IndexName="three-two-index", KeyConditionExpression=Key('three').eq('three'))

# success
db.table.query(TableName="USER", KeyConditionExpression=Key('PK').eq('one'))
# fail
db.table.query(TableName="USER", KeyConditionExpression=Key('one').eq('one'))




db.table.query(IndexName="three-two-index", KeyConditionExpression=Key('three').eq('three'))['Items']


db.table.query(TableName="USER", KeyConditionExpression=Attr('one').eq('one'))


db.table.query(IndexName="three-two-index", KeyConditionExpression=Key('three').eq('three') & Key('two').begins_with('two2'))['Items']

Note: you can only Scan or Query a GSI index
You may perform Scan or Query operation on GSI index



db.table.query(IndexName="three-two-index", KeyConditionExpression='three = three')['Items']


db.table.query(TableName="USER", KeyConditionExpression='PK = :PK', ExpressionAttributeValues={':PK': {'S': 'hello'}})


db.table.query(TableName="USER", KeyConditionExpression='PK = :PK', ExpressionAttributeValues={':PK': 'example' } )['Items']
db.table.query(IndexName="three-two-index", KeyConditionExpression='three = :three', ExpressionAttributeValues={':three': 'three' })['Items']


db.table.query(TableName="USER", KeyConditionExpression=Key('PK').eq('hello'))['Items']
db.table.query(TableName="USER", IndexName="three-two-index", KeyConditionExpression=Key('three').eq('three'))['Items']


https://www.fernandomc.com/posts/ten-examples-of-getting-data-from-dynamodb-with-python-and-boto3/