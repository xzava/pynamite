# Copyright 2020 Mike hall
#
# The following Licence applies to all files within this project.
#
# Licensed under the Software License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.thewolf.co.nz/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#######################################################################

""" Default dynamo class defaults. 
	
	USAGE:
		>>> from pynamite import dynamo
		>>> db = dynamo.DB('USER')
		>>> db.
		db.PK              db.get(            db.put(            db.table
		db.SK              db.get_partition(  db.records         db.update(
		db.delete(         db.help            db.scan(           
		db.describe        db.info(           db.status 

		>>> from pynamite import dynamo;db = dynamo.DB('USER')
		>>> import importlib;importlib.reload(dynamo);db = dynamo.DB('USER')
"""

# https://dynobase.dev/dynamodb-python-with-boto3/

print("pynamite version 0.0.1")

from os import getenv
from decimal import Decimal
import decimal 
from copy import deepcopy
from pprint import pprint
from collections import defaultdict, Counter
from functools import lru_cache
import json
import logging
import sys

import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
# from cachetools import cached, LRUCache, TTLCache

from pynamite.utils import function_name, display_changes_between_dicts, MyJSONEncoder
from pynamite.utils import error_name, error_message, timestamp, iso_time
from pynamite.utils import remove_keys
from pynamite.utils import first, second, get_index
from pynamite.utils import convert_key, confirm_dialog, _load_key_schema
from pynamite.utils import debug


# from pynamite.utils import test_this

from pynamite import utils
from pynamite import expression
# import pynamite.utils as utils
# import pynamite.expression as expression

logger = logging.getLogger(__name__)



"################"
"#     DOCS     #"
"################"

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

"#################"
"#     NOTES     #"
"#################"

"""
Note: The following ENV are expected.

export AWS_ACCESS_KEY_ID='XXXXXX'
export AWS_SECRET_ACCESS_KEY='XXXXXX/XXXXXXXXX+XXXXXXX'
export DYNAMO_TABLE_NAME='XXXXX'

"""

"#####################"
"#     FUNCTIONS     #"
"#####################"

""" 
DB:
  update(
  get(
  put(
  delete(
  get_partition(

table_connection(_

describe_all()
dynamo_connection()
table_connection()
list_tables()
create_table()
show_schema()
show_partition()
query()
user_get_attrs()
collect_expression()


"""

"############################"
"#     SIMILAR PROJECTS     #"
"############################"

"""
https://github.com/pynamodb/PynamoDB
https://github.com/stevearc/flywheel
https://github.com/serebrov/dynamo_objects
"""

"#####################"
"#     RESOURSES     #"
"#####################"


# https://www.bmc.com/blogs/dynamodb-advanced-queries/

# "Requested resource not found" -- Does this table exist?

"""


	TODO: add advanced get for assuming `get_partition`
	TODO: add support for queries
	TODO: make async --> https://pypi.org/project/aioboto3/
	TODO: Look into download_as and upload_as
	
	DONE: add support for increment  "set example.count = example.count + :n"

"""

# Default dynamodb return
RETURN_VALUES="UPDATED_NEW"

# Update records with metadata
METADATA=True

# Update this by using dynamo.DEFAULT_META = ['timestamp', '__staging__']
DEFAULT_META = getenv("DEFAULT_META", "") or [
	'updated',
	'updated_iso',
	'created',
	'timestamp',
	'created_iso',
	'__updated',
	'__updated_iso',
	'__created',
	'__created_iso',
	'_timestamp',
	'__timestamp',
	'_updated',
	'_updated_iso',
	'_created',
	'_created_iso',
	'PK',
	'SK'
]

def remove_meta(data, ignore=None, custom_meta=None):
	""" Quick function to remove meta information from db.get() returns

		data: dict
		ignore: list
		custom_meta: list

		EXAMPLES:
			>>> from pynamite import dynamo
			>>> import importlib;importlib.reload(dynamo)
			>>> dynamo.remove_meta({"timestamp": 1283920324})
			{}
			
			>>> dynamo.DEFAULT_META = ['timestamp', '__staging__']
			>>> dynamo.remove_meta({"timestamp": 1283920324, '__production__': 'PRODUCTION'})
			{'__production__': 'PRODUCTION'}
			
			>>> dynamo.DEFAULT_META = ['one']
			>>> dynamo.remove_meta({"timestamp": 1283920324, '__production__': 'PRODUCTION'})
			{"timestamp": 1283920324, '__production__': 'PRODUCTION'}
			
			>>> dynamo.DEFAULT_META = 'one,__production__'
			>>> dynamo.remove_meta({"timestamp": 1283920324, '__production__': 'PRODUCTION'})
			{"timestamp": 1283920324}


	"""
	if custom_meta is None:
		debug("remove_meta: using system defined default_meta")
		debug("create your own by dynamo.default_meta = ['timestamp']")

	default_meta = custom_meta if custom_meta else DEFAULT_META

	if isinstance(default_meta, str):
		default_meta = default_meta.split(",")

	ingore_list = default_meta + ignore if ignore else default_meta
	
	if isinstance(data, list):
		return [remove_keys(e, ingore_list) for e in data]
	return remove_keys(data, ingore_list)


def test_this(custom_meta=None):
	"""

	>>> from pynamite import dynamo
	>>> import importlib;importlib.reload(dynamo)
	>>> dynamo.test_this()
	>>> dynamo.DEFAULT_META = ['timestamp', '__staging__']
	>>> dynamo.test_this()
	>>> dynamo.DEFAULT_META = ['one']
	>>> dynamo.test_this()
	>>> dynamo.DEFAULT_META = 'one,two'

	"""
	default_meta = custom_meta if custom_meta else DEFAULT_META
	if isinstance(default_meta, str):
		default_meta = default_meta.split(",")
	print(default_meta)


class DB:
	""" Default dynamo class defaults. 
		
		Please note your table must already exist. This code interacts with an existing table 
		for safety reasons table creation should be done manually.
		
		USAGE:
			>>> from pynamite import dynamo
			>>> db = dynamo.DB('USER')
			>>> db.
			db.PK              db.get(            db.put(            db.table
			db.SK              db.get_partition(  db.records         db.update(
			db.delete(         db.help            db.scan(           
			db.describe        db.info(           db.status 

			>>> from pynamite import dynamo;db = dynamo.DB('USER')
			>>> import importlib;importlib.reload(dynamo);db = dynamo.DB('USER')
	"""
	def __init__(self, table_name=None, pk='PK', sk='SK'):
		debug(f'Connecting to dynamo <Table name="{table_name}">\n')
		self._describe = None
		self._schema = None

		self._dynamodb = dynamo_connection()
		self.table = table_connection(self._dynamodb, table_name)
		
		self.PK, self.SK = utils._load_key_schema(self.table.key_schema) #> ("PK", "SK")
		self.records = None #> Object to attach record schema
		self.describe
		debug(f'SUCCESS: connected to <Table name="{table_name}">')


	def get(self, key, attrs=None, _default=None, **kwargs):
		""" Get an item from a dynamodb table

			INPUT:
				key: dict | str | list | tuple 
	
				attrs: str
					Only return these attrs (ProjectionExpression) --> "key1,key2,key3"  

				_default: Any
					default fallback return

				kwargs: Other optional arguments to passed to .get_items()

				 .get_item(
				     Key=dict,
				     ConsistentRead=True|False,
				     ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
				     ProjectionExpression='#string',
				     ExpressionAttributeNames={'#string': 'string'}
				 )

			EXAMPLE:
			
			  # The following are the same
			  >>> location = "USER.#PROFILE#M74244398"
			  >>> location = ["USER", "#PROFILE#M74244398"]
			  >>> location = {'PK':'USER', 'SK':'#PROFILE#M74244398'}

			  >>> db.get(location)
			  >>> db.get("testing.example")
				{'mapping': {'a': Decimal('0'), 'b': 'bb', 'c': ['cc', 'cc', 'c'], 'd': {'a': 'da', 'b': 'db'}}, 'count': Decimal('89'), 'set': {'c', 'b', 'a'}, '_updated': '2022-04-17T05:01:38.883411', 'SK': 'example', 'PK': 'testing', 'list': [Decimal('11'), Decimal('22'), Decimal('33'), Decimal('8')]}

			  >>> db.get("testing.example", "mapping.a, list[2]")

			

			Error: Invalid ProjectionExpression: Attribute name is a reserved keyword; reserved keyword: data
			https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html
		
			REFERENCE:
				https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item
		"""
		# assert key, "arg missing, Expecting a PK and SK ie --> key={'PK':'USER', 'SK':'#PROFILE#M74244398'}"
		try:
			kwargs["Key"] = convert_key(key, self.PK, self.SK)
			if attrs:
				kwargs = kwargs | expression.UpdateExpression()._ProjectionExpression(attrs)
				# response = self.table.get_item(Key=key, ProjectionExpression=attrs, ExpressionAttributeNames=ExpressionAttributeNames)
				# response = self.table.get_item(Key=key, **name_mapping, **kwargs)
			# else:
			response = self.table.get_item(**kwargs)
			# debug(response)
			return response['Item']

		except KeyError as e:
			_error_name = error_name(e)
			_function_name = function_name()
			_message = f"No key 'Item' found in get_item(key={key}, attrs={attrs})"
			debug(f"{_error_name} @ {_function_name}() // {_message}")
		except ClientError as e:
			error_message(e)

		debug("WARNING: returning default response.")
		return _default


	def update(self, key, attributes_to_update, _default=None, **kwargs):
		""" Updates a item, but keeps all unsupplied keys. Will create a new Item if the Key is not found.
			
			INPUT:
			
			key: dict | str | list | tuple 
			
			attributes_to_update: dict
				key value pair

			_default: Any
				default fallback return


			**kwargs:

				.update_item(
				    TableName='string',
				    Key={    },
				    AttributeUpdates={    },
				    Expected={    },
				    ConditionalOperator='AND'|'OR',
				    ReturnValues='NONE'|'ALL_OLD'|'UPDATED_OLD'|'ALL_NEW'|'UPDATED_NEW',
				    ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
				    ReturnItemCollectionMetrics='SIZE'|'NONE',
				    UpdateExpression='string',
				    ConditionExpression='string',
				    ExpressionAttributeNames={   },
				    ExpressionAttributeValues={  }
				)


			EXAMPLE:
				>>> update(profile_record('M742443980'), data)

				>>> key = {'PK': "USER", 'SK': "#PROFILE#M742443980"}
				>>> key = "USER.#PROFILE#M742443980"
				>>> key = ["USER", "#PROFILE#M742443980"]
				>>> attributes_to_update = {
					'dob': 'MAGICDATE',
					'email': 'MAGIC@gmail.com',
					'firstname': 'MAGICNAME'
				}
				>>> db.update(key, attributes_to_update)

			ReturnValues (options): str

				"NONE" 		 - If ReturnValues is not specified, or if its value is NONE, then nothing is returned. (This setting is the default for ReturnValues.)
				"ALL_OLD" 	 - Returns all of the attributes of the item, as they appeared before the UpdateItem operation.
				"UPDATED_OLD"	 - Returns only the updated attributes, as they appeared before the UpdateItem operation.
				"ALL_NEW"		 - Returns all of the attributes of the item, as they appear after the UpdateItem operation.
				"UPDATED_NEW"	 - Returns only the updated attributes, as they appear after the UpdateItem operation.


			RAW AWS OUTPUT:
			{
				'Attributes':
				{
					'email': 'MAGIC@gmail.com',
					'firstname': 'MAGICNAME',
					'dob': 'MAGICDATE'
				},
				'ResponseMetadata':
				{
					'RequestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
					'HTTPStatusCode': 200,
					'HTTPHeaders':
					{
						'server': 'Server',
						'date': 'Mon, 11 Jun 2021 13:12:00 GMT',
						'content-type': 'application/x-amz-json-1.0',
						'content-length': '102',
						'connection': 'keep-alive',
						'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
						'x-amz-crc32': '0123456789'
					},
					'RetryAttempts': 0
				}
			}

			NOTE: Above is confidentialised 


			
			>>> from pynamite import dynamo;db = dynamo.DB('USER')
			>>> import importlib;importlib.reload(dynamo)
			>>> db = dynamo.DB('USER')
			
			>>>	db.update("testing.example", {"count": 0, "list": [11,22,33], "set": {"a", "b", "c"}, "mapping": {"a": 0, "b":"bb", "c": ["cc", "cc", "c"], "d": {"a": "da", "b": "db"}}})
			>>> db.get("testing.example")
			>>> db.delete("testing.example")
			

			db.update("testing.example", {"dict_example": {"list": [11,22,33], "set": {11,22,33}, "hello": {"a": ["a", "a"], "b": ["b"]}}})
			db.get("testing.example", {"dict_example.hello.b[0]": "B"})
			db.update("testing.example", {"count": expression.Increment("count")})
			>>> 

		"""
		assert isinstance(attributes_to_update, dict), 'attributes_to_update must be a dict'

		kwargs.setdefault("ReturnValues", getenv("RETURN_VALUES", RETURN_VALUES))
		kwargs["Key"] = convert_key(key, self.PK, self.SK)

		# assert key, "key needs to be supplied ie {'PK': 'USER', 'SK': '#PROFILE#M742443980'}"
		# assert attributes_to_update, 'attributes_to_update can not be empty or None'
	
		"Add custom metedata"
		_attributes_to_update = deepcopy(attributes_to_update)
		if METADATA is True:
			_attributes_to_update['_updated'] = utils.iso_time()
			# _attributes_to_update['_updated'] = timestamp()
			# _attributes_to_update['_updated_iso'] = iso_time()

		# expression_out = expression.update(_attributes_to_update)
		kwargs = kwargs | expression.UpdateExpression().build(_attributes_to_update)

		debug("\n")
		debug("\n")
		debug("Key: ", kwargs["Key"])
		debug("attrs: ", _attributes_to_update)
		debug("UpdateExpression: ", kwargs["UpdateExpression"])
		debug("ExpressionAttributeValues: ", kwargs["ExpressionAttributeValues"])
		debug("ExpressionAttributeNames: ", kwargs["ExpressionAttributeNames"])
		debug("kwargs: ", kwargs)
		debug("\n")
		debug("\n")
		
		try:
			# response = self.table.update_item(
			# 	# Key=key, #> {'PK': 'USER', 'SK': '#PROFILE#M742443980'}
			# 	# UpdateExpression=UpdateExpression, #> 'set #4459=:4459, #9147=:9147, #8791=:8791'
			# 	# ExpressionAttributeValues=ExpressionAttributeValues, #> {':4459': '17/01/1990', ':9147': 'hello@gmail.com', ':8791': 'ME'}
			# 	# ExpressionAttributeNames=ExpressionAttributeNames, #> {'#4459': dob, '#9147': email, '#8791': firstname}
			# 	**kwargs
			# )
			response = self.table.update_item(**kwargs)
			# debug(response)
			return response['Attributes']
		except KeyError as e:
			_error_name = error_name(e)
			_function_name = function_name()
			_message = f"No 'Attributes' found in response for {key}"
			debug(f"{_error_name} @ {_function_name}() // {_message}")
		except ClientError as e:
			error_message(e)

		debug("WARNING: returning default response.")
		return _default


	def put(self, key, data, _default=None, **kwargs):
		""" (UNSAFE) Add a new item to the database, or replace all attrs with data if found.
			
			key: dict | str | list | tuple 
			
			data: dict
				new data

			_default: Any
				default fallback return


			**kwargs: Additional attrs to sent to put_item

				.put_item(
				    TableName='string',
				    Item={    },
				    Expected={    },
				    ReturnValues='NONE'|'ALL_OLD'|'UPDATED_OLD'|'ALL_NEW'|'UPDATED_NEW',
				    ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
				    ReturnItemCollectionMetrics='SIZE'|'NONE',
				    ConditionalOperator='AND'|'OR',
				    ConditionExpression='string',
				    ExpressionAttributeNames={    },
				    ExpressionAttributeValues={}
				)



			EXAMPLES:
				>>> put({'PK':'USER', 'SK':'#PROFILE#M74244398'}, data)
				>>> put(profile_record(), data)
				>>> put(profile_record(generate_membership_id()), data)
			

			RAW AWS OUTPUT:
			{
			    'ResponseMetadata':
			    {
			        'RequestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
			        'HTTPStatusCode': 200,
			        'HTTPHeaders':
			        {
			            'server': 'Server',
			            'date': 'Thu, 11 Apr 2022 05:24:00 GMT',
			            'content-type': 'application/x-amz-json-1.0',
			            'content-length': '2',
			            'connection': 'keep-alive',
			            'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
			            'x-amz-crc32': 'xxxxxxxx'
			        },
			        'RetryAttempts': 0
			    }
			}


			NOTE: Above is confidentialised 

			https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item

		"""
		debug("""WARNING: Use db.update unless you know what you are doing.

		db.put will delete and replace all existing data for this record, 
		while db.update() will create a new record or safely update existing.
		""")

		key = convert_key(key, self.PK, self.SK)
		# debug(f"key: {key}") #> {'PK': 'magic', 'SK': 'one'}
		# debug(f"data: {data}") #> {'item': '8', 'HELLO': 'HELLO'}
		
		# assert isinstance(key, dict), "Key needs to be type dict."
		assert isinstance(data, dict), "data needs to be type dict."
		# assert self.PK not in data, "data dict can not conatin a 'PK' as it will overwrite existing"
		# assert self.SK not in data, "data dict can not conatin a 'SK' as it will overwrite existing"
		
		"One or more parameter values were invalid: Cannot update attribute SK. This attribute is part of the key"
		"data can not conatin 'PK' or 'SK' as it will overwrite existing"
		_data = deepcopy(data)
		_data.pop(self.PK, None)
		_data.pop(self.SK, None)

		# created = timestamp()
		created_iso = utils.iso_time()
		# key = {k: str(created) if v is None else v for k,v in key.items()}
		
		try:
			_replacement = deepcopy(key)
			_replacement.update(_data)
			

			if METADATA is True:
				# _key['created'] = created
				# _key['created_iso'] = created_iso
				# _key['updated'] = created
				# _key['updated_iso'] = created_iso
				_replacement['_created'] = created_iso
				_replacement['_updated'] = created_iso

			kwargs["Item"] = _replacement
			kwargs["ConditionExpression"] = "attribute_not_exists(SK)"
			
			"Success if record does not already exist."
			response = self.table.put_item(**kwargs)
			
			debug("response: ", response)
			debug("key: ", key)

			if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
				return {
					self.PK: _replacement.get(self.PK),
					self.SK: _replacement.get(self.SK),
					"size": sys.getsizeof(json.dumps(list(_replacement.values())))
				}
		except (ClientError, Exception) as e:
			error_message(e)

		debug("WARNING: returning default response.")
		return _default


	def delete(self, key, _default=None, soft_delete=False, **kwargs):
		""" Delete a item from the database 

			key: dict | str | list | tuple 

			_default: Any

			soft_delete: bool

			**kwargs: 
				.delete_item(
				    TableName='string',
				    Key={    },
				    Expected={    },
				    ConditionalOperator='AND'|'OR',
				    ReturnValues='NONE'|'ALL_OLD'|'UPDATED_OLD'|'ALL_NEW'|'UPDATED_NEW',
				    ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
				    ReturnItemCollectionMetrics='SIZE'|'NONE',
				    ConditionExpression='string',
				    ExpressionAttributeNames={    },
				    ExpressionAttributeValues={    }
				)

			RAW AWS OUTPUT:
			{
				'ResponseMetadata': {
					'HTTPHeaders': {
						'connection': 'keep-alive',
						'content-length': '2',
						'content-type': 'application/x-amz-json-1.0',
						'date': 'Wed, 01 Jun 2020 07:21:30 GMT',
						'server': 'Server',
						'x-amz-crc32': 'xxxxxxxxxxx',
						'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxx'
					},
					'HTTPStatusCode': 200,
					'RequestId': 'xxxxxxxxxxxxxxxxxxxxxx',
					'RetryAttempts': 0
				}
			}

			NOTE: Above is confidentialised 
			https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_item

		"""
		key = convert_key(key, self.PK, self.SK)
		assert isinstance(key, dict), "Key needs to be type dict."
		try:
			# Example with no conditions, will delete item if found.
			response = self.table.delete_item(
				Key=key,
				# ConditionExpression="info.rating <= :val",
				# ExpressionAttributeValues={
				#   ":val": Decimal(rating)
				# }
			)
			if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
				return {
					self.PK: key.get(self.PK),
					self.SK: key.get(self.SK)
				}

		except ClientError as e:
			if e.response['Error']['Code'] == "ConditionalCheckFailedException":
				error_message(e)
				debug({self.PK: key.get(self.PK), self.SK: key.get(self.SK)})
			else:
				raise
				error_message(e)
		else:
			return response

		debug("WARNING: returning default response.")
		return _default


	def get_partition(self, bucket, startswith=None, _default=None, **kwargs):
		""" Get all records in a partition_key
			
			EXAMPLE:
				>>> db.get_partition("House")
				>>> db.get_partition("House", startswith="#FOR_SALE")
		"""
		try:
			if startswith:
				response = self.table.query(
					KeyConditionExpression=Key(self.PK).eq(bucket) & Key(self.SK).begins_with(startswith)
				)
			else:
				response = self.table.query(
					KeyConditionExpression=Key(self.PK).eq(bucket)
				)
			return response['Items']
		
		except KeyError as e:
			_error_name = error_name(e)
			_function_name = function_name()
			_message = f"No 'Items' found in response for Key({self.PK}).eq({bucket})"
			debug(f"{_error_name} @ {_function_name}() // {_message}")
		except ClientError as e:
			error_message(e)

		debug("WARNING: returning default response.")
		return _default


	def scan(self, confirm=False, _default=None, **kwargs):
		""" Returns all items in the whole database
			
			EXAMPLE:
				>>> db.scan(confirm=True)
				>>>
				>>>

		# db.table.scan(ProjectionExpression="PK, SK")['Items']
		# [{'PK': 'example', 'SK': 'name'}, {'PK': 'example', 'SK': 'name2'}]

		https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan
		"""
		debug("", 'WARNING: This function is returning/reading a full database record (expensive).')
		if confirm is False:
			debug('Please confirm: use db.scan(confirm=True)')
			return None

		try:
			result = self.table.scan(**kwargs)
			return result['Items']
		except KeyError as e:
			_error_name = error_name(e)
			_function_name = function_name()
			_message = f"No 'Items' found in response for Key({self.PK}).eq({bucket})"
			debug(f"{_error_name} @ {_function_name}() // {_message}")
		except ClientError as e:
			error_message(e)

		debug("WARNING: returning default response.")
		return _default


	@property
	def describe(self):
		""" Describe a table
			>>> self._dynamodb.meta.client.describe_table(TableName="USER")
			>>> dynamodb.meta.client.describe_table(TableName="USER")
			{'Table': {
				'AttributeDefinitions': [{'AttributeName': 'PK', 'AttributeType': 'S'}, {'AttributeName': 'SK', 'AttributeType': 'S'}], 
				'TableName': 'USER', 
				'KeySchema': [
					{'AttributeName': 'PK', 'KeyType': 'HASH'}, 
					{'AttributeName': 'SK', 'KeyType': 'RANGE'}
				], 
				'TableStatus': 'ACTIVE', 
				'CreationDateTime': datetime.datetime(2021, 9, 28, 12, 15, 59, 759000, tzinfo=tzlocal()), 
				'ProvisionedThroughput': {
					'NumberOfDecreasesToday': 0, 
					'ReadCapacityUnits': 5,
					'WriteCapacityUnits': 5
				}, 
				'TableSizeBytes': 1424, 
				'ItemCount': 7, 
				'TableArn': 'arn:aws:dynamodb:us-east-1:xxxxxxxxxxxxxx:table/USER', 
				'TableId': 'xxxxxxxxxxxxxxxx'
			}, 
			'ResponseMetadata': {
				'RequestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 
				'HTTPStatusCode': 200, 
				'HTTPHeaders': {'server': 'Server', 'date': 'Mon, 11 Jan 2022 13:17:00 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '542', 'connection': 'keep-alive', 'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'x-amz-crc32': 'xxxxxxxxxxxxxxx'}, 
				'RetryAttempts': 0
			}}

			NOTE: Above is confidentialised 
		"""
		if self._describe is None:
			describe_table = self._dynamodb.meta.client.describe_table(TableName="USER")["Table"]
			self._describe = describe_table
			debug("Running first time..", "")
			return self._describe
		return self._describe


	@property
	def status(self):
		""" Get current status of a table eg 'ACTIVE'
		"""
		return self.table.table_status


	def info(self):
		""" General info about a dynamodb table.
		"""
		return {
			"name": self.table.name,
			"id": self.table.table_id,
			'arn': self.table.table_arn, #> 'arn:aws:dynamodb:us-west-2:xxxxxxxxxxxxxxxx:table/USER'
			"provisioned_throughput": self.table.provisioned_throughput,
			'created': self.table.creation_date_time,
			'size_bytes': self.table.table_size_bytes,
			'items': self.table.item_count
		}


	@property
	def help(self):
		""" help information
		"""
		debug("This is a helper class for dynamodb")
		return 


	def __repr__(self):
		return f'<Table name="{self.table.name}">'


@lru_cache(5)
def describe_all():
	""" Describe all dynamo tables listed on a user account 

		Note: This method of getting table names is better than `dynamodb.tables.all()`
	"""
	dynamodb = dynamo_connection()
	table_names = dynamodb.meta.client.list_tables().get("TableNames", [])
	return {e: dynamodb.meta.client.describe_table(TableName=e)["Table"] for e in table_names}


def dynamo_connection(dynamodb=None):
	""" Establish aws dynamoDB connection

		>>> import dynamo
		>>> dynamo = dynamo_connection()

		This dynamodb account has the following tables..
		- Movies
		- USER

		>>> type(dynamo)
		<class 'boto3.resources.factory.dynamodb.ServiceResource'>

	"""
	if dynamodb:
		return dynamodb

	dynamodb = boto3.resource('dynamodb',
		aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
		aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY')
	)
	assert dynamodb, "No connection established with AWS.."
	debug("", "This dynamodb account has the following tables..")
	# dynamodb.meta.client.list_tables()
	for each in list_tables(dynamodb):
		debug(f"- {each}")
	debug("")
	return dynamodb


def table_connection(dynamodb=None, table_name=None):
	""" Repeat of the config set up, inside a function. 
		
		NOTE: Two environment variables are expected.
		
		aws_access_key_id=''
		aws_secret_access_key=''
		
		>>> import dynamo
		>>> dynamo = table_connection()
	"""
	dynamodb = dynamo_connection(dynamodb)

	target_table = table_name or getenv('DYNAMO_TABLE_NAME')
	assert target_table, "A table name is required in either: env 'DYNAMO_TABLE_NAME=<TABLE>' or the 'table_name' arg of this function."
	return dynamodb.Table(target_table)


@lru_cache(5)
def list_tables(dynamodb=None):
	""" List all table names

		EXAMPLE:
			>>> list_tables(db._dynamodb)
	
			>>> dynamodb.meta.client.list_tables()
			{
				'TableNames': ['USER'], 
				'ResponseMetadata': {'RequestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 10 Apr 2022 22:49:28 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '23', 'connection': 'keep-alive', 'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'x-amz-crc32': 'xxxxxxxxxxxx'}, 
				'RetryAttempts': 0}
			}
	"""
	dynamodb = dynamo_connection(dynamodb)

	if hasattr(dynamodb, "_dynamodb"):
		dynamodb = dynamodb._dynamodb

	table_names = dynamodb.meta.client.list_tables()
	return table_names.get("TableNames", [])
	# return [e.name for e in dynamodb.tables.all()]


def create_table(
		dynamodb=None,
		table_name=None,
		ReadCapacityUnits=5,
		WriteCapacityUnits=5,
	):
	""" Manually run function: Create a new dynamo db table in aws
		
		>>> from pynamite import dynamo
		>>> db = dynamo.create_table()
	"""

	# assert table_name, "ERROR: create_table() -> arg `table_name` is required to create a table."
	confirm_dialog(
		action="Create new dynamodb table.",
		warning="You are creating a NEW dynamodb table in AWS, please confirm as this is a billable action. This library is built around using existing tables, rather than creating new ones."
	)
	
	dynamodb = dynamo_connection(dynamodb)

	if table_name is None:
		table_name = input("Enter TableName, default is 'example': ").strip() or "example"

	if ReadCapacityUnits is None:
		ReadCapacityUnits = int(input("Enter ReadCapacityUnits, default is 5: ").strip()) or 5

	if WriteCapacityUnits is None:
		WriteCapacityUnits = int(input("Enter ReadCapacityUnits, default is 5: ").strip()) or 5

	table = dynamodb.create_table(
		TableName=table_name,
		KeySchema=[
			{
				'AttributeName': 'PK',
				'KeyType': 'HASH'  # Partition key
			},
			{
				'AttributeName': 'SK',
				'KeyType': 'RANGE'  # Sort key
			}
		],
		AttributeDefinitions=[
			{
				'AttributeName': 'PK',
				'AttributeType': 'S' # string
			},
			{
				'AttributeName': 'SK',
				'AttributeType': 'S' # string
			},
		],
		ProvisionedThroughput={
			'ReadCapacityUnits': ReadCapacityUnits,
			'WriteCapacityUnits': WriteCapacityUnits
		}
	)

	# table = dynamodb.create_table(
	# 	TableName=table_name,
	# 	KeySchema=[
	# 		{
	# 			'AttributeName': 'PK',
	# 			'KeyType': 'HASH'  # Partition key
	# 		},
	# 		{
	# 			'AttributeName': 'SK',
	# 			'KeyType': 'RANGE'  # Sort key
	# 		}
	# 	],
	# 	AttributeDefinitions=[
	# 		{
	# 			'AttributeName': 'PK',
	# 			'AttributeType': 'S' # string
	# 		},
	# 		{
	# 			'AttributeName': 'SK',
	# 			'AttributeType': 'S' # string
	# 		},
	# 	],
	# 	ProvisionedThroughput={
	# 		'ReadCapacityUnits': 5,
	# 		'WriteCapacityUnits': 5
	# 	}
	# )

	debug('SUCCESS: <Table name="{table_name}">')
	debug("To delete table use.. ")
	return table



def show_schema(db):
	""" Show all the partitions and sort keys
		
		EXAMPLE:
			>>> show_schema(db) 
			{'example': ['name', 'name2']}
		
		SAMPLE:
			{
				'123': ['CUST#123', 'https://aws.amazon.com', 'https://console.aws.amazon.com'],
				'321': ['CUST#321', 'https://aws.amazon.com', 'https://docs.aws.amazon.com'],
				'example': ['hello']
			}
		
		REQUIRES:
			from collections import defaultdict

		TODO: I would like it to show a grid view overview of all keys for each similar to this
			  https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/images/tabledesign.png
	"""
	debug("WARNING: return value can be very large, this function is only meant for debugging.")
	data = db.table.scan(ProjectionExpression="PK, SK")['Items']
	out = defaultdict(list)
	[out[e['PK']].append(e["SK"]) for e in data]
	return debug(dict(out))


def show_partition(db, count=True):
	""" Show all the partitions
		
		INPUT:
			db: <dynamo.DB>, or <dynamodb.Table>
			count: bool
				Return a counter of the result 
		
		EXAMPLE:
			>>> import dynamo
			>>> dynamo.show_partition(db)
			Counter({'123': 3, '321': 3, 'example': 1})
			>>> dynamo.show_partition(db, count=False)
			{'123', '321', 'example'}
		
		REQUIRES:
			from collections import Counter
	"""
	if isinstance(db, DB):
		data = db.table.scan(ProjectionExpression="PK")['Items']
	else:
		data = db.scan(ProjectionExpression="PK")['Items']

	if count is True:
		# return Counter([r for e in [list(e.items()) for e in data] for r in e])
		# Counter({('PK', '123'): 3, ('PK', '321'): 3, ('PK', 'example'): 1})
		return Counter([first(list(e.values())) for e in data]) #> Counter({'123': 3, '321': 3, 'example': 1})
	return {e['PK'] for e in data}



def query(db, **kwargs):
	"""
	
	.query(
	    TableName='string',
	    IndexName='string',
	    Select='ALL_ATTRIBUTES'|'ALL_PROJECTED_ATTRIBUTES'|'SPECIFIC_ATTRIBUTES'|'COUNT',
	    Limit=123,
	    ConsistentRead=True|False,
	    ScanIndexForward=True|False,
	    ExclusiveStartKey={	    },
	    ReturnConsumedCapacity='INDEXES'|'TOTAL'|'NONE',
	    ProjectionExpression='string',
	    FilterExpression='string',
	    KeyConditionExpression='string',
	    ExpressionAttributeNames={	    },
	    ExpressionAttributeValues={}
	)

	https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query
	

	kwargs["ExclusiveStartKey"] = LastEvaluatedKey


	RAW AWS OUTPUT:

	{
	    'Items': [ {  } ],
	    'Count': 123,
	    'ScannedCount': 123,
	    'LastEvaluatedKey': {    },
	    'ConsumedCapacity': {
	        'TableName': 'string',
	        'CapacityUnits': 123.0,
	        'ReadCapacityUnits': 123.0,
	        'WriteCapacityUnits': 123.0,
	        'Table': {
	            'ReadCapacityUnits': 123.0,
	            'WriteCapacityUnits': 123.0,
	            'CapacityUnits': 123.0
	        },
	        'LocalSecondaryIndexes': {
	            'string': {
	                'ReadCapacityUnits': 123.0,
	                'WriteCapacityUnits': 123.0,
	                'CapacityUnits': 123.0
	            }
	        },
	        'GlobalSecondaryIndexes': {
	            'string': {
	                'ReadCapacityUnits': 123.0,
	                'WriteCapacityUnits': 123.0,
	                'CapacityUnits': 123.0
	            }
	        }
	    }
	}

	DynamoDB.Client.exceptions.ProvisionedThroughputExceededException
	DynamoDB.Client.exceptions.ResourceNotFoundException
	DynamoDB.Client.exceptions.RequestLimitExceeded
	DynamoDB.Client.exceptions.InternalServerError
	"""
	response = db.table.query(**kwargs)
	return response

	

def user_get_attrs(db, KeyConditionExpression=None, ProjectionExpression="email, SK"):
	""" Get a user by their email address.

		>>> from pynamite import dynamo;db = dynamo.DB('USER')
		>>> import importlib;importlib.reload(dynamo);db = dynamo.DB('USER')
		>>> dynamo.user_get_attrs(db, 'PK = USER')

		https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query
	"""
	"1. check email is a vaild email"
	try:
		response = db.table.query(
			# KeyConditionExpression=Key('PK').eq('USER'),
			KeyConditionExpression=KeyConditionExpression,
			ProjectionExpression=ProjectionExpression)
		return response['Items']
	except KeyError as e:
		_error_name = error_name(e)
		_function_name = function_name()
		_message = "No `Items` found in response for KeyConditionExpression=Key('PK').eq('USER'), ProjectionExpression='email, SK'"
		debug(f"{_error_name} @ {_function_name}() // {_message}")
	except ClientError as e:
		error_message(e)


def collect_expression(condition):
    """ For creating the string version of 'KeyConditionExpression'
        
        >>> from boto3.dynamodb.conditions import Key, Attr
        >>> collect_expression("PK")
        "PK"
        >>> collect_expression(Key('PK').eq('USER'))
        'PK = USER'
        >>> collect_expression(Key('PK').eq('USER') & Key('SK').begins_with('test'))
        (PK = USER AND begins_with(SK, test))
        >>> collect_expression(Key('SK').begins_with('test'))
        'begins_with(SK, test)'
        >>> collect_expression(Key('PK').eq('USER') & Key('SK').between('11.11.11', "11.11.12"))
        '(PK = USER AND SK BETWEEN 11.11.11 AND 11.11.12)'

        >>> Key.
        Key.begins_with(  Key.eq(           Key.gte(          Key.lte(
        Key.between(      Key.gt(           Key.lt(           Key.mro(

    """
    if isinstance(condition, str):
        return condition
    #
    if isinstance(condition, Key):
        return condition.name
    #
    ce = getattr(condition, "get_expression", lambda x: None)()
    # ce #> {'format': '{0} {operator} {1}', 'operator': '=', 'values': (<boto3.dynamodb.conditions.Key object at 0x7fcec3889f40>, 'USER')}
    if ce:
        print(ce)
        values = tuple(collect_expression(e) for e in ce["values"])
        # print(values)
        return ce['format'].format(*values, operator=ce["operator"])
    #
    return "Error.."
	


if __name__ == '__main__':
	""" 
		MANUAL REFERENCES:

		>>> table = boto3.resource('dynamodb').Table('USERS')
		>>> table.
		table.archival_summary             table.global_table_version         table.put_item(                    
		table.attribute_definitions        table.item_count                   table.query(                       
		table.batch_writer(                table.key_schema                   table.reload(                      
		table.billing_mode_summary         table.latest_stream_arn            table.replicas                     
		table.creation_date_time           table.latest_stream_label          table.restore_summary              
		table.delete(                      table.load(                        table.scan(                        
		table.delete_item(                 table.local_secondary_indexes      table.sse_description              
		table.get_available_subresources(  table.meta                         table.stream_specification         
		table.get_item(                    table.name                         table.table_arn                    
		table.global_secondary_indexes     table.provisioned_throughput       table.table_id 
		table.table_name  				   table.update_item(                 table.wait_until_exists(
		table.table_size_bytes             table.table_status                 table.update(   
		table.wait_until_not_exists(


		>>> from boto3.dynamodb.conditions import Key, Attr
		>>> Attr.
		Attr.attribute_type(  Attr.contains(        Attr.gt(              Attr.lt(              
		Attr.begins_with(     Attr.eq(              Attr.gte(             Attr.lte(             
		Attr.between(         Attr.exists(          Attr.is_in(           Attr.mro(             
		Attr.ne(              Attr.not_exists(      Attr.size(

		>>> Key.
		Key.begins_with(  Key.eq(           Key.gte(          Key.lte(
		Key.between(      Key.gt(           Key.lt(           Key.mro(
		

		
		>>> import dynamo
		>>> dynamodb = dynamo_connection()
		>>> type(dynamodb)
		<class 'boto3.resources.factory.dynamodb.ServiceResource'>
		>>> dynamodb. 			
		dynamodb.Table(                       dynamodb.create_table(                dynamodb.tables
		dynamodb.batch_get_item(              dynamodb.get_available_subresources(  
		dynamodb.batch_write_item(            dynamodb.meta  
		


		>>> dynamodb.meta.client.
		dynamodb.meta.client.batch_execute_statement(                 dynamodb.meta.client.get_item(
		dynamodb.meta.client.batch_get_item(                          dynamodb.meta.client.get_paginator(
		dynamodb.meta.client.batch_write_item(                        dynamodb.meta.client.get_waiter(
		dynamodb.meta.client.can_paginate(                            dynamodb.meta.client.list_backups(
		dynamodb.meta.client.create_backup(                           dynamodb.meta.client.list_contributor_insights(
		dynamodb.meta.client.create_global_table(                     dynamodb.meta.client.list_exports(
		dynamodb.meta.client.create_table(                            dynamodb.meta.client.list_global_tables(
		dynamodb.meta.client.delete_backup(                           dynamodb.meta.client.list_tables(
		dynamodb.meta.client.delete_item(                             dynamodb.meta.client.list_tags_of_resource(
		dynamodb.meta.client.delete_table(                            dynamodb.meta.client.meta
		dynamodb.meta.client.describe_backup(                         dynamodb.meta.client.put_item(
		dynamodb.meta.client.describe_continuous_backups(             dynamodb.meta.client.query(
		dynamodb.meta.client.describe_contributor_insights(           dynamodb.meta.client.restore_table_from_backup(
		dynamodb.meta.client.describe_endpoints(                      dynamodb.meta.client.restore_table_to_point_in_time(
		dynamodb.meta.client.describe_export(                         dynamodb.meta.client.scan(
		dynamodb.meta.client.describe_global_table(                   dynamodb.meta.client.tag_resource(
		dynamodb.meta.client.describe_global_table_settings(          dynamodb.meta.client.transact_get_items(
		dynamodb.meta.client.describe_kinesis_streaming_destination(  dynamodb.meta.client.transact_write_items(
		dynamodb.meta.client.describe_limits(                         dynamodb.meta.client.untag_resource(
		dynamodb.meta.client.describe_table(                          dynamodb.meta.client.update_continuous_backups(
		dynamodb.meta.client.describe_table_replica_auto_scaling(     dynamodb.meta.client.update_contributor_insights(
		dynamodb.meta.client.describe_time_to_live(                   dynamodb.meta.client.update_global_table(
		dynamodb.meta.client.disable_kinesis_streaming_destination(   dynamodb.meta.client.update_global_table_settings(
		dynamodb.meta.client.enable_kinesis_streaming_destination(    dynamodb.meta.client.update_item(
		dynamodb.meta.client.exceptions                               dynamodb.meta.client.update_table(
		dynamodb.meta.client.execute_statement(                       dynamodb.meta.client.update_table_replica_auto_scaling(
		dynamodb.meta.client.execute_transaction(                     dynamodb.meta.client.update_time_to_live(
		dynamodb.meta.client.export_table_to_point_in_time(           dynamodb.meta.client.waiter_names
		dynamodb.meta.client.generate_presigned_url(  


		>>> dynamodb.meta.client.describe_table(TableName="USER")
		{'Table': {
			'AttributeDefinitions': [{'AttributeName': 'PK', 'AttributeType': 'S'}, {'AttributeName': 'SK', 'AttributeType': 'S'}], 
			'TableName': 'USER', 
			'KeySchema': [
				{'AttributeName': 'PK', 'KeyType': 'HASH'}, 
				{'AttributeName': 'SK', 'KeyType': 'RANGE'}
			], 
			'TableStatus': 'ACTIVE', 
			'CreationDateTime': datetime.datetime(2021, 9, 28, 12, 15, 59, 759000, tzinfo=tzlocal()), 
			'ProvisionedThroughput': {
				'NumberOfDecreasesToday': 0, 
				'ReadCapacityUnits': 5,
				'WriteCapacityUnits': 5
			}, 
			'TableSizeBytes': 1424, 
			'ItemCount': 7, 
			'TableArn': 'arn:aws:dynamodb:us-west-2:xxxxxxxxxxxxxxxxxxxxx:table/USER', 
			'TableId': 'xxxx-xxxx-xxxx'
		}, 
		'ResponseMetadata': {
			'RequestId': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 
			'HTTPStatusCode': 200, 
			'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 10 Apr 2022 22:57:38 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '542', 'connection': 'keep-alive', 'x-amzn-requestid': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'x-amz-crc32': 'xxxxxxxxxxxxx'}, 
			'RetryAttempts': 0
		}}




		TEST CODE:

		import dynamo
		db = dynamo.DB('hello')
		key = {"PK": "example", "SK": "name"}
		data = {"hello": "okay"}
		db.put(key, data)

	"""