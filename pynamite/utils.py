from datetime import datetime
import secrets
from decimal import Decimal
import string
import json
from copy import deepcopy

from os import getenv

"""
Utils for dynamite library

- timestamp
- iso_time
- make_uuid
- generate_membership_id
- display_changes_between_dicts
- MyJSONEncoder
- function_name
- function_details
- function_args
- try_error_message

"""

# 1636266897
# regex_timestamp_check = r'142006680d|14200668[1-9]d|14200669d{2}|142006[7-9]d{3}|14200[7-9]d{4}|14201[0-4]d{4}|142015[0-2]d{3}|1420153[0-1]d{2}'

# https://www.alexdebrie.com/posts/dynamodb-condition-expressions/

# 1636266353
# [1636266353]
# --11636266353--

from datetime import datetime, timedelta
from functools import wraps

from cachetools import cached, LRUCache, TTLCache
import cachetools

from pprint import pprint

LRU_CACHE_MAXSIZE=10
LRU_CACHE_TTL=12


def debug(*args, pretty=False):
	""" Print only is DEBUG env is True

		EXAMPLE:
			>>> debug("debug message")

		export DEBUG="True"
		
		REQUIRES:
		from pprint import pprint
	"""
	if getenv("DEBUG") in ["1", 1, "True", "DEBUG", "TRUE", "true", "debug", "Debug"]:
		if pretty is True:
			from pprint import pprint
			pprint(*args)
		print(*args)


def lru_cache(f):
	""" Custom lru cache decorator using cachetools to refresh a single cache result
		with out affecting the other cached items.
	"""
	_cache = TTLCache(maxsize=LRU_CACHE_MAXSIZE, ttl=timedelta(hours=LRU_CACHE_TTL), timer=datetime.now) 
	# _cache = LRUCache(maxsize=LRU_CACHE_MAXSIZE) #> runs once per function
	@wraps(f)
	def wrapper(*args, cache_bust=False, **kwargs):
		if cache_bust is True:
			_cache.pop(cachetools.keys.hashkey(*args, **kwargs), None)
		# can add more flags here to interact with the _cache object. _cache.clear() for example
		return cached(_cache)(f)(*args, **kwargs)
	return wrapper


@lru_cache
def so(n):
	debug('...')
	return n + 2


timestamp = lambda: int(datetime.timestamp(datetime.utcnow()))
iso_time = lambda: str(datetime.utcnow().isoformat())





def get_index(data, index=0, _default=None):
	""" Get an arbitrary index from a list like object, if it exists.

		# attempt to find a index if it exists or return _default.
		# key[0:1] is always a list with 0 or 1 items.
	"""
	return data[index:index+1 or None][0] if data[index:index+1 or None] else _default

def first(data, _default=None):
	""" Collect the first index if it exists.
	"""
	# return data[0:1][0] if data[0:1] else _default
	return get_index(data, index=0, _default=_default)

def second(data, _default=None):
	""" Collect the second index if it exists.
	"""
	# return data[1:2][0] if data[1:2] else _default
	return get_index(data, index=1, _default=_default)

def last(data, _default=None):
	""" Collect the second index if it exists.
	"""
	# return data[1:2][0] if data[1:2] else _default
	return get_index(data, index=-1, _default=_default)


def str_to_decimal(string, _default=None):
	""" Converts a string to a decimal, output is a float | None | `_default`.

		EXAMPLE:
			>>> str_to_decimal('100')
			100.0
			>>> str_to_decimal('100.00')
			100.0
			>>> str_to_decimal('100.00038402')
			100.00038402
			>>> str_to_decimal('d100')
			None
			"Using _default: could not convert string to float: 'd100'"
			>>> str_to_decimal('')
			None
			>>> str_to_decimal('0')
			0.0
			>>> str_to_decimal('', _default=100)
			100

		TODO: could add regex to extract numbers.
	"""
	try:
		return float(string)
	except ValueError as error:
		debug("Using _default: " + error) #> Using _default: could not convert string to float:
	# return float(_default) #> If you want to force default to be a float
	return _default


def read_timestamp(timestamp, strftime="isoformat"):
	""" Takes a timestamp (str, int, float) and makes it readable isoformat

		EXAMPLE:
			>>> read_timestamp()

		REQUIRES:
			from datetime import datetime

		SEE ALSO:
			<str_to_decimal>
	"""
	decimal_ts = str_to_decimal(timestamp)
	if strftime == "isoformat":
		readable_ts = datetime.fromtimestamp(decimal_ts).isoformat()
	else: 
		readable_ts = datetime.fromtimestamp(decimal_ts).strftime(strftime)
	return readable_ts


# regex-for-timestamp
# https://stackoverflow.com/questions/11665582/regex-for-timestamp

def remove_keys(data, ingore):
	""" Return a new dict without the keys in the ingore list. 

		EXAMPLE:
			>>> remove_keys({'one': '1', 'four': '4', 'five': '5'}, ingore=['four','five'])
			{'one': '1'}

		REQUIRES:
			from copy import deepcopy
	"""
	if data:
		return {k:v for k,v in deepcopy(data).items() if k not in ingore}
	return data


def strict_keys(data, allow):
	""" Return a new dict with only the keys in the allow list. 
		
		EXAMPLE:
			>>> strict_keys({'one': '1', 'four': '4', 'five': '5'}, allow=['four','five'])
			{'four': '4', 'five': '5'}

		REQUIRES:
			from copy import deepcopy
	"""
	if data:
		return {k:v for k,v in deepcopy(data).items() if k in allow}
	return data


def make_uuid(prefix=None, suffix=None, sep="_", chars=None, n=14):
	""" Make a uuid or a token. 
		
		EXAMPLE:
			>>> make_uuid(prefix="BOX")
			BOX_k59Gks8fjf92bD
			>>> make_uuid(suffix="REF_112", sep="-")
			ks892bfjfk59GD-REF_112
			>>> make_uuid(prefix="M", sep="", chars="0123456789" n=8)
			M30071522
	
		REQUIRES:
			import string
			import secrets
	"""
	if chars is None:
		chars = string.ascii_letters + string.digits

	token = ''.join(secrets.choice(chars) for i in range(n))
	return sep.join(e for e in (prefix, token, suffix) if e)


def generate_membership_id(sep="M"):
	""" Generate Membership ID -->  M30071522
		
		EXAMPLE:
			>>> generate_membership_id()
			M30071522

		REQUIRES:
			import secrets
	"""
	return sep + ''.join(secrets.choice('0123456789') for i in range(8))


def display_changes_between_dicts(d1, d2, keep_extra_keys=False):
	""" The purpose of this function is for database updaing only values that have changed. (deletes are ingored.)
	  
		 d1 (orginal) --> { "One": 1, "Two": 2, "Three": 3 }
		 d2 (new)     --> { "One": 1, "Two": 2, "Three": 4 }
	
		 >>> display_changes_between_dicts(d1, d2) 
		 {"Three": 4}
		 
		 d1 (orginal) --> { "One": 1, "Two": 2, "Three": 3 }
		 d2 (new)     --> { "One": 1, "Two": 2, "Three": 4, "Hello": "World!" }

		 >>> display_changes_between_dicts(d1, d2, keep_extra_keys=True) 
		 {"Three": 4, "Hello": "World!"}

	"""
	if keep_extra_keys is False:
		# Only accept keys that appear in the orginal dict (d1)
		dict_difference = {k: d2[k] for k,v in d1.items() if d2.get(k) and d2.get(k) != d1.get(k)}
	else:
		# Keep keys that don't exist in orginal dict (d1)
		dict_difference = {k:v for k,v in d2.items() if d2.get(k) and d2.get(k) != d1.get(k)}
	return dict_difference



class MyJSONEncoder(json.JSONEncoder):
	""" Allow flask json to encode Decimal() which is used in dynamodb
	"""
	# from decimal import Decimal
	# from flask import json
	# https://stackoverflow.com/questions/24706951/how-to-convert-all-decimals-in-a-python-data-structure-to-string
	# useage: app.json_encoder = MyJSONEncoder
	def default(self, obj):
		if isinstance(obj, Decimal):
			# Convert decimal instances to strings.
			return str(obj)
		return super(MyJSONEncoder, self).default(obj)


def function_name(n=1):
	""" Return the current function name
	
		https://docs.python.org/3/library/inspect.html

		FrameInfo class has the following attrs: 'code_context', 'count', 'filename', 'frame', 'function', 'index', 'lineno'
		
	"""
	import inspect
	stack = inspect.stack() #> list(FrameInfo)
	return [e.function for e in stack][n]


def function_details(args=locals()):
	""" Return the current function details
		
		EXAMPLE:
			>>> hello(three=hello, two=None, one=1) @ test.py:60
			>>> hello() @ test.py:49


		FrameInfo class has the following attrs: 'code_context', 'count', 'filename', 'frame', 'function', 'index', 'lineno'
		https://docs.python.org/3/library/inspect.html
	"""
	import inspect
	
	stack = inspect.stack() #> list(FrameInfo)
	stack_detailed = [f"{e.function}() @ {e.filename}:{e.lineno}" for e in stack]
	if args:
		return stack_detailed[1].replace('()', function_args(args))  
		#> hello(three=hello, two=None, one=1) @ test.py:60
	else:
		return stack_detailed[1]  
		#> hello() @ test.py:49


def function_args(data=locals()):
	""" Used within a function to get the args of that function as a string 
	
		(one='one', _default=magic)
	"""
	return '(' + ', '.join([f"{k}={v}" for k,v in data.items()]) + ')'


error_name = lambda e: type(e).__name__


def error_message(e):
	""" Try print a error message, helper function for dynamodb.
	"""
	try:
		debug(e.response['Error']['Message'])
	except Exception as e:
		debug(e)



def convert_key(key, PK='PK', SK='SK'):
	""" Clean a key into required dict format.
		
		Allows the key to be expressed in different ways.
		- dot notation
		- dict
		- list / tuple
		
		key: 
		PK: <str>
			Partition key
		SK: <str>
			Sort Key

	EXAMPLE:
		>>> convert_key('pk.sk') 					
		{'PK': 'pk', 'SK': 'sk'}
		>>> convert_key({'PK': 'pk', 'SK': 'sk'})   
		{'PK': 'pk', 'SK': 'sk'}
		>>> convert_key(['pk', 'sk']) 				
		{'PK': 'pk', 'SK': 'sk'}
		>>> convert_key('pk.s.k') 					
		{'PK': 'pk', 'SK': 's.k'}
		>>> convert_key(['pk', 'sk', 'three']) 		
		{'PK': 'pk', 'SK': 'sk'}
		>>> convert_key(['pk']) 					
		{'PK': 'pk', 'SK': None}
		>>> convert_key(None) 						
		None
		>>> convert_key({'PK': 'pk', 'SK': 'sk', "three": "three"})
		{'PK': 'pk', 'SK': 'sk'}
		>>> convert_key(['pk', 'sk', 'three'])
		{'PK': 'pk', 'SK': 'sk'}
		>>> convert_key('pk.s.k')
		{'PK': 'pk', 'SK': 's.k'}				


	TODO: if PK is provided without range (when sork key is used on table) assume user wants to get all in target partition
	ie use get_partition() in the background 
	"""
	if isinstance(key, str):
		# pk, sk = key.split('.') #> ValueError
		pk, _, sk = key.partition('.') #> {'PK': 'pk', 'SK': 's.k'}
		assert isinstance(pk, str) or isinstance(pk, int) and isinstance(sk, str)
		return {PK: pk, SK: sk}
	if isinstance(key, list) or isinstance(key, tuple):
		# "Collect only the first two indexes if they exist"
		# pk, sk = key
		pk = first(key) # first index if it exists
		sk = second(key) # second index if it exists
		assert isinstance(pk, str) or isinstance(pk, int) and isinstance(sk, str)
		return {PK: pk, SK: sk}
	if isinstance(key, dict):
		# TODO: Figure out if this is the way I want it
		# return {k:v for k,v in key.items() if k in [PK, SK]}
		return key


def confirm_dialog(action, warning="You are attempting to do something that needs confirmation"):
	""" CLI confirm dialog

		USEAGE:
			>>> confirm_dialog(
				  action="Create new dynamodb table.",
				  warning="You are creating a NEW dynamodb table in AWS, please confirm as this is a billable action."
				)

	"""
	warning = action if action else warning
	debug("")
	debug(f"Please Confirm.. '{action}'")
	debug("")
	debug(f"WARNING: {warning}")
	confirm = input("Enter 'YES' to continue or 'NO' to exit safely: ").lower().strip()
	debug(f"User entered: {confirm} - {action}")
	debug("")
	if confirm in {"y", "yes", "1", "true", "confirm", "affirmative", "okay", "yeah", "yip", "ye", "aprove"}:
		return True
	raise ValueError(f"Action: '{action}' not approved by user.")


def _load_key_schema(key_schema):
	""" helper function to load `key_schema` for aws dynamodb table

		EXAMPLE:
			>>> key_schema = [{'AttributeName': 'PK', 'AttributeType': 'S'}, {'AttributeName': 'SK', 'AttributeType': 'S'}]
			>>> _load_key_schema(key_schema)
			("PK", "SK")

		USAGE:
			# Used in DB.__init__
			self.PK, self.SK = _load_key_schema(self.table.key_schema)

		SEE ALSO:
			<DB>

	"""
	# pk, *sk = [e['AttributeName'] for e in self.table.key_schema]
	key_schema = [e['AttributeName'] for e in key_schema]
	# >>> db.table.attribute_definitions
	# [{'AttributeName': 'PK', 'AttributeType': 'S'}, {'AttributeName': 'SK', 'AttributeType': 'S'}]
	# >>> db.table.key_schema
	# [{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}]
	PK = first(key_schema) # first index if it exists
	SK = second(key_schema) # second index if it exists
	return PK, SK


def remove_meta(data, ignore=None):
	""" Quick function to remove meta information from db.get() returns
	"""
	default_meta = [
		'updated',
		'updated_iso',
		'created',
		'created_iso',
		'__updated',
		'__updated_iso',
		'__created',
		'__created_iso',
		'PK',
		'SK'
	]
	ingore_list = default_meta + ignore if ignore else default_meta
	if isinstance(data, list):
		return [remove_keys(e, ingore_list) for e in data]
	return remove_keys(data, ingore_list)