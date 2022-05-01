"""
"""

import decimal
from decimal import Decimal
import re

from pprint import pprint

from pynamite import utils
from pynamite.utils import debug

print("Loading <Module pynamite.expression>")

"""

>>> from pynamite import expression
>>> import importlib;importlib.reload(expression)
>>> expression.UpdateExpression("example.hello", {"dict_example.hello.b[1]": "B"})
>>> db.update("example.hello", {"dict_example.hello.b[1]": "B"})

"""

class ExpressionBase:
	""" Base class for the following classes, used for creation dynamodb actions

		- Increment
		- Decrement
		- ListAppend
		- ListRemove
		- IfNotExists

	"""
	action = ''
	expression_operator = ''
	expression_format = ''
	value = ''
	def build(self, key=None):
		return self.expression_format.format(
			key or self.key,
			operator=self.expression_operator,
			expression_name=self.expression_name,
			expression_value=self.value
		)


class Increment(ExpressionBase):
	""" Increment a int record on dynamodb
		
		EXAMPLE:
			>>> db.update('example.hello', {"count": 0})
	 		>>> db.update('example.hello', {'count': dynamo.Increment('count')})
	 
	"""
	def __init__(self, key, change_by=1):
		if not isinstance(change_by, decimal.Decimal):
			change_by = decimal.Decimal(change_by)

		self.action = "SET"
		self.key = key
		self.change_by = change_by
		self.expression_operator = '+'
		self.expression_name = f':I_{self.change_by}'
		self.expression_format = '{0} {operator} {expression_name}'
		self.additional_expression_attribute_values = (self.expression_name, self.change_by)


class Decrement(ExpressionBase):
	""" Decrement a int record on dynamodb

		EXAMPLE:
			>>> db.update('example.hello', {"count": 0})
			>>> db.update('example.hello', {'count': dynamo.Decrement('count')})
	"""
	def __init__(self, key, change_by=1):
		if not isinstance(change_by, decimal.Decimal):
			change_by = decimal.Decimal(change_by)

		self.action = "SET"
		self.key = key
		self.change_by = change_by
		self.expression_operator = '-'
		self.expression_name = f':D_{self.change_by}'
		self.expression_format = '{0} {operator} {expression_name}'
		self.additional_expression_attribute_values = (self.expression_name, self.change_by)


class ListAppend(ExpressionBase):
	""" Append value to a list

		EXAMPLE:
			>>> db.update('example.hello', {'my_list': [1,2]})
			>>> db.update('example.hello', {'a_list': dynamo.ListAppend('a_list', [3,4])})
	"""
	def __init__(self, key, value, start=False):
		self.action = "SET"
		self.key = key
		self.value = list(value) if isinstance(value, (list, tuple)) else [value]
		self.expression_operator = 'list_append'
		self.expression_name = ':LA_' + str(abs(hash(key)))[-10:]
		if start is True:
			"# append to the start"
			self.expression_format = '{operator}({expression_name}, {0})' #> list_append(:vals, #ri)
		else:
			# DEFAULT: append to the end of a list
			self.expression_format = '{operator}({0}, {expression_name})' #> list_append(#ri, :vals)
		# from start #> list_append(:vals, #ri)
		self.additional_expression_attribute_values = (self.expression_name, self.value)


class ListRemove(ExpressionBase):
	""" Remove list indexes from a list

		Targets the list index not the value
		
		ie 
		aws dynamodb update-item \
		    --table-name ProductCatalog \
		    --key '{"Id":{"N":"789"}}' \
		    --update-expression "REMOVE RelatedItems[1], RelatedItems[2]" \
		    --return-values ALL_NEW

		EXAMPLE:
			>>> db.update('example.hello', {'my_list': [1,2,3,4]}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListAppend('my_list', [5,6,7])})
			>>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [5,6,7])}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [1,2])}) 
		
		NOTE: Is this is not working,
		More info on how to fix this problem can be found here.
		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
	"""
	# Note this is not finished as you can't do the same as above as its under SET and joining commands doesn't have a commar.
	def __init__(self, key, value):
		self.action = "REMOVE"
		self.key = key
		self.value = value
		self.expression_operator = ''
		self.expression_name = '#' + str(abs(hash(key)))[-10:]
		# self.expression_format = '{expression_name}[{0}]'
		self.expression_format = '{expression_name}[{expression_value}]'
		# self.expression_format = '[{expression_value}]'
		self.additional_expression_attribute_values = (self.expression_name, self.value)


class SetAppend(ExpressionBase):
	""" Add a item to a set

		Targets the list index not the value
		
		ie 
		aws dynamodb update-item \
		    --table-name ProductCatalog \
		    --key '{"Id":{"N":"789"}}' \
		    --update-expression "REMOVE RelatedItems[1], RelatedItems[2]" \
		    --return-values ALL_NEW

		EXAMPLE:
			>>> db.update('example.hello', {'my_list': [1,2,3,4]}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListAppend('my_list', [5,6,7])})
			>>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [5,6,7])}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [1,2])}) 
		
		NOTE: Is this is not working,
		More info on how to fix this problem can be found here.
		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
	"""
	# Note this is not finished as you can't do the same as above as its under SET and joining commands doesn't have a commar.
	def __init__(self, key, value):
		self.action = "ADD"
		self.key = key
		self.value = list(value) if isinstance(value, (list, tuple)) else [value]
		self.expression_operator = ''
		self.expression_name = ':SR_' + str(abs(hash(key)))[-10:]
		self.expression_format = '{expression_name} {0}'
		self.additional_expression_attribute_values = (self.expression_name, self.value)


class SetRemove(ExpressionBase):
	""" Remove item from a set

		Targets the list index not the value
		
		ie 
		aws dynamodb update-item \
		    --table-name ProductCatalog \
		    --key '{"Id":{"N":"789"}}' \
		    --update-expression "REMOVE RelatedItems[1], RelatedItems[2]" \
		    --return-values ALL_NEW

		EXAMPLE:
			>>> db.update('example.hello', {'my_list': [1,2,3,4]}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListAppend('my_list', [5,6,7])})
			>>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [5,6,7])}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [1,2])}) 
		
		NOTE: Is this is not working,
		More info on how to fix this problem can be found here.
		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
	"""

	"""

	CURRENT: DELETE #0169182500 :SR_0169182500 #0169182500 SET #9293253196=:0510772436

	EXPECTED: DELETE #0169182500 :SR_0169182500, SET #9293253196=:0510772436


	>>> d = SetRemove("example", "one")
	>>> d.build()
	':SR_6551699817 example'


	>>> expression.update({"one": expression.SetRemove("key", "two")})
	'DELETE #7513818127 = :SR_1707883424'

	"""
	# Note this is not finished as you can't do the same as above as its under SET and joining commands do not have a commar.
	def __init__(self, key, value):
		self.action = "DELETE"
		self.key = key
		self.value = list(value) if isinstance(value, (list, tuple)) else [value]
		self.expression_operator = ''
		self.expression_name = ':SR_' + str(abs(hash(key)))[-10:]
		self.expression_format = '{expression_name} {0}'
		self.additional_expression_attribute_values = (self.expression_name, self.value)


class IfNotExists(ExpressionBase):
	""" Only do if attr doesn't exist

		EXAMPLE
			>>> db.update('example.hello', {'my_list': [1,2,3,4]}) 
			>>> db.update('example.hello', {'my_list': dynamo.ListAppend('my_list', [0,0,0], start=True)})
			>>> db.update('example.hello', {'my_list': dynamo.IfNotExists('my_list', [0,0,0])})
	
			>>> db.update('example.hello', {'my_list': dynamo.IfNotExists('my_list', [9,9,9])})
			>>> db.update('example.hello', {'my_list_new': dynamo.IfNotExists('my_list_new', [0,0,0])})
			>>> db.get('example.hello')
	"""
	def __init__(self, key, value):
		self.action = "SET"
		self.key = key
		self.value = list(value) if isinstance(value, (list, tuple)) else [value]
		self.expression_operator = 'if_not_exists'
		self.expression_name = ':NE_' + str(abs(hash(key)))[-10:]
		self.expression_format = '{operator}({0}, {expression_name})' #> if_not_exists(#ri, :vals)
		# from start #> list_append(:vals, #ri)
		self.additional_expression_attribute_values = (self.expression_name, self.value)


def custom_hash(string, sep=":"):
	"""

	>>> custom_expression("hello")
	:1662517072
	>>> custom_expression("one")
	:8655921785
	>>> custom_expression("hi")
	:0384822183
	"""
	hashed = sep + str(abs(hash(string)))[-10:] 
	return hashed


def process(key):
	""" Allow dynamo index lookup and dot notation, with hashing the keys in a deep structure
	
		EXAMPLE:

			>>> process("hello[0].one[2].hi")
			'#1662517072[0].#8655921785[2].#0384822183'
			>>> process("hello[0][0][1][1].one[2].hi")
			'#1662517072[0][0][1][1].#8655921785[2].#0384822183'
			>>> process("hello[0][0][1][1].one[2].hi[2][3].hello[0][1]")
			'#1662517072[0][0][1][1].#8655921785[2].#0384822183[2][3].#1662517072[0][1]'

		REQUIRES:
			import re

		SEE ALSO:
			<custom_hash>
	"""
	location = re.split(r"(\[\d])", key) #> 
	print(location) #> ['hello', '[0]', '.one', '[2]', '.hi.hello']	
	result = []
	hash_records = {}
	for each in location:
		if each:
			if '.' in each:
				result.append('.'.join(custom_hash(e, '#') if e else '' for e in each.split('.')))
			elif each.startswith("["):
				result.append(each)
			else:
				_result_item = custom_hash(each, '#')
				hash_records[each] = _result_item
				result.append(_result_item)
				# result.append(custom_hash(each, '#'))
	return ''.join(result)





class UpdateExpression(ExpressionBase):
	""" Allow dynamo index lookup and dot notation, with hashing the keys in a deep structure
	
		EXAMPLE:

			>>> UpdateExpression.process("hello[0].one[2].hi")
			'#1662517072[0].#8655921785[2].#0384822183'
			>>> UpdateExpression.process("hello[0][0][1][1].one[2].hi")
			'#1662517072[0][0][1][1].#8655921785[2].#0384822183'
			>>> UpdateExpression.process("hello[0][0][1][1].one[2].hi[2][3].hello[0][1]")
			'#1662517072[0][0][1][1].#8655921785[2].#0384822183[2][3].#1662517072[0][1]'

		REQUIRES:
			import re

		SEE ALSO:
			<custom_hash>

			>>> from pynamite import expression
			>>> import importlib;importlib.reload(expression)
			>>> expression.UpdateExpression("example.hello", {"dict_example.hello.b[1]": "B"})
			>>> db.update("example.hello", {"dict_example.hello.b[1]": "B"})


			>>> expression.UpdateExpression.process("dict_example.hello.b[1]")
			ue = expression.UpdateExpression()
			ue.process("dict_example.hello.b[1]")

		METHODS:
			.dict()
			._hash()
			custom_hash
			hash_func
			_split_location
			process

	"""
	def __init__(self, location=None):
		self.additional_attribute_values = []

		self.update_expression = str()
		self.attribute_values = dict()
		self.attribute_names = dict()

		# self._expression_actions = {
		# 	"SET": []
		# 	"ADD": []
		# 	"REMOVE": []
		# 	"DELETE": []
		# }

		# self.action = "SET"
		# self.key = key
		# self.change_by = change_by
		# self.expression_operator = '+'
		# self.expression_name = f':I_{self.change_by}'
		# self.expression_format = '{0} {operator} {expression_name}'
		# self.additional_expression_attribute_values = (self.expression_name, self.change_by)

	# def __dict__():

	def dict(self):
		""" Create a dict of the class
		"""
		return {
			"UpdateExpression": self.update_expression,
			"ExpressionAttributeValues": self.attribute_values,
			"ExpressionAttributeNames": self.attribute_names
		}

	def __repr__(self):
		return f"<UpdateExpression update_expression='{self.update_expression}', attribute_values='{self.attribute_values}', attribute_names='{self.attribute_names}'>"

	def __str__(self):
		return str(self.update_expression)


	@staticmethod
	def _hash(string, sep=":"):
		"""

			>>> custom_expression("hello")
			:1662517072
			>>> custom_expression("one")
			:8655921785
			>>> custom_expression("hi")
			:0384822183
		"""
		try:
			hashed = sep + str(abs(hash(string)))[-10:]
		except TypeError as e:
			"Input is unhashable, ie dict, list, ect.."
			hashed = sep + utils.make_uuid(prefix=type(string).__name__.upper(), n=7)
		return hashed


	def custom_hash(self, key, value=None, sep=":"):
		""" Caller of _hash() with side effects.

		>>> custom_expression("hello")
		:1662517072
		>>> custom_expression("one")
		:8655921785
		>>> custom_expression("hi")
		:0384822183
		"""

		if isinstance(value, ExpressionBase):
			expression_action = value

			k,v = expression_action.additional_expression_attribute_values
			# self.additional_attribute_values[k] = y
			# self.attribute_values[key] = hashed
			hashed = self._hash(key, "#")
			# self.attribute_values[hashed] = key
			self.attribute_values[k] = v
			# self.additional_attribute_values.append(expression_action.additional_expression_attribute_values)
			expression_hashed = expression_action.build(hashed)
			debug("ExpressionBase object: ", expression_hashed)
			return expression_hashed #> ExpressionBase object


		if sep == ":":
			hashed = self._hash(value, sep)
			self.attribute_values[hashed] = value

		if sep == "#":
			hashed = self._hash(key, sep)
			self.attribute_names[hashed] = key

		return hashed


	@staticmethod
	def _split_location(key):
		""" Split a dynamo attr path into groups, so the keys can be hashed,

			EXAMPLES:
				>>> UpdateExpression._split_location("hello")
				'#1662517072'
				>>> UpdateExpression._split_location('hello[0]')
				'#1662517072[0]'
				>>> UpdateExpression._split_location("hello[0][0][1][1].one[2].hi")
				'#1662517072[0][0][1][1].#8655921785[2].#0384822183'
				>>> process("hello[0][0][1][1].one[2].hi[2][3].hello[0][1]")
				'#1662517072[0][0][1][1].#8655921785[2].#0384822183[2][3].#1662517072[0][1]'
				>>>
		"""
		location = re.split(r"(\[\d])", key) #> 
		debug("location: ", location) #> ['hello', '[0]', '.one', '[2]', '.hi.hello']	
		return location


	def process(self, key, value=None, sep="#"):
		""" Allow dynamo index lookup and dot notation, with hashing the keys in a deep structure
		
			EXAMPLE:

				>>> process("hello[0].one[2].hi")
				'#1662517072[0].#8655921785[2].#0384822183'
				>>> process("hello[0][0][1][1].one[2].hi")
				'#1662517072[0][0][1][1].#8655921785[2].#0384822183'
				>>> process("hello[0][0][1][1].one[2].hi[2][3].hello[0][1]")
				'#1662517072[0][0][1][1].#8655921785[2].#0384822183[2][3].#1662517072[0][1]'

			REQUIRES:
				import re

			SEE ALSO:
				<custom_hash>
		"""
		location = self._split_location(key) #> ['hello', '[0]', '.one', '[2]', '.hi.hello']	
		result = []
		# hash_records = {}
		for each in location:
			if each:
				if '.' in each:
					result.append('.'.join(self.custom_hash(e, sep='#') if e else '' for e in each.split('.')))
					# result.append('.'.join(self.custom_hash(e, sep='#') if e else '' for e in each.split('.')))
				elif each.startswith("["):
					result.append(each)
				else:
					# _result_item = self.custom_hash(each, '#')
					# hash_records[each] = _result_item
					# result.append(_result_item)
					result.append(self.custom_hash(each, sep='#'))
		return ''.join(result)
		# return result


	def _ProjectionExpression(self, attrs):
		""" Used to create 'ExpressionAttributeNames' for .get_item()

			>>> from pynamite import expression
			>>> import importlib;importlib.reload(expression)
			
			>>> expression.UpdateExpression()._ProjectionExpression("mapping.a")
			{'ProjectionExpression': '#0390467094.#6039992441', 'ExpressionAttributeNames': {'#0390467094': 'mapping', '#6039992441': 'a'}}
			
			>>> expression.UpdateExpression()._ProjectionExpression("mapping.a, list[2]")
			{'ProjectionExpression': '#0390467094.#6039992441, #6387852527[2]', 
			'ExpressionAttributeNames': {'#0390467094': 'mapping', '#6039992441': 'a', '#6387852527': 'list'}}
			

			>>> expression.UpdateExpression()._ProjectionExpression("(mapping.a), (list.hello)[1], list[2]")
			
		"""

		result = ', '.join(self.process(e.strip(), sep="#") for e in attrs.split(','))

		return {
			"ProjectionExpression": result,
			"ExpressionAttributeNames": self.attribute_names
		}


	def _process_actions(self, data):
		"""
		"""

		# actions = {
		# 	"SET": []
		# 	"ADD": []
		# 	"REMOVE": []
		# 	"DELETE": []
		# }

		# try:
		# 	action = v.action
		# except AttributeError as e:
		# 	action = "SET"

		from collections import defaultdict

		actions = defaultdict(list)

		for k,v in data.items():
			# action = getattr(v, "action", lambda: "SET")()
			action = getattr(v, "action", "SET")

			if action == "SET":
				a = self.process(k, None, sep='#')
				b = self.custom_hash(k, v, sep=':')
				actions[action].append(f"{a}={b}")

			elif action == "REMOVE":
				a = self.process(k, None, sep='#')
				b = self.custom_hash(k, v, sep=':')
				actions[action].append(f"{b}")

			else:
				a = self.process(k, None, sep='#')
				b = self.custom_hash(k, v, sep=':')
				actions[action].append(f"{a} {b}")

		update_expression = ' '.join(f"{k} {', '.join(v)}" for k, v in actions.items() if v)
		print(actions)
		print(update_expression)
		return update_expression


	def build(self, data):
		""" Build the UpdateExpression and associated mapping of key value pairs

			INPUT:
				data: dict

			EXAMPLE:
				>>> from pynamite import expression
				>>> import importlib;importlib.reload(expression)
				>>> ue = expression.UpdateExpression()
				>>> ue.build({"dict_example.hello.b[1]": "B"})
				>>> expression.UpdateExpression().build({"dict_example.hello.b[1]": "B"})
				{
				    'ExpressionAttributeNames': {
				        '#2344528508': 'b',
				        '#4521760024': 'hello',
				        '#6906335747': 'dict_example'
				    },
				    'ExpressionAttributeValues': {
				        ':4403423471': 'B'
				    },
				    'UpdateExpression': 'SET #6906335747.#4521760024.#2344528508[1] = :4403423471'
				}
				>>> expression.UpdateExpression().build({"hello": "B"})
				{'ExpressionAttributeNames': {'#4521760024': 'hello'},
				 'ExpressionAttributeValues': {':4403423471': 'B'},
				 'UpdateExpression': 'SET #4521760024 = :4403423471'}
				>>> expression.UpdateExpression().build({"hello": "B", "hello2": "B"})
				{
				    'ExpressionAttributeNames': {
				        '#4521760024': 'hello',
				        '#5441070998': 'hello2'
				    },
				    'ExpressionAttributeValues': {
				        ':4403423471': 'B'
				    },
				    'UpdateExpression': 'SET #4521760024 = :4403423471, #5441070998 = :4403423471'
				}
				>>> expression.UpdateExpression().build({"hello": 1, "hello2": "B"})
				{'ExpressionAttributeNames': {'#4521760024': 'hello', '#5441070998': 'hello2'},
				 'ExpressionAttributeValues': {':1': 1, ':4403423471': 'B'},
				 'UpdateExpression': 'SET #4521760024 = :1, #5441070998 = :4403423471'}
				>>> expression.UpdateExpression().build({"hello": 1, "hello2": "B", "hello3": expression.Increment("hello3")})
				{
				    'ExpressionAttributeNames':
				    {
				        '#4521760024': 'hello',
				        '#5179455735': 'hello3',
				        '#5441070998': 'hello2'
				    },
				    'ExpressionAttributeValues':
				    {
				        ':1': 1,
				        ':4403423471': 'B',
				        ':I_1': Decimal('1')
				    },
				    'UpdateExpression': 'SET #4521760024 = :1, #5441070998 = :4403423471, #5179455735 = #5179455735 + :I_1'
				}
				>>> expression.UpdateExpression().build({"hello": 1, "hello2": "B", "hello3": expression.Decrement("hello3")})
				{
				    'ExpressionAttributeNames':
				    {
				        '#4521760024': 'hello',
				        '#5179455735': 'hello3',
				        '#5441070998': 'hello2'
				    },
				    'ExpressionAttributeValues':
				    {
				        ':1': 1,
				        ':4403423471': 'B',
				        ':D_1': Decimal('1')
				    },
				    'UpdateExpression': 'SET #4521760024 = :1, #5441070998 = :4403423471, #5179455735 = #5179455735 - :D_1'
				}
				>>> expression.UpdateExpression().build({"hello": expression.ListAppend("hello", 9)})
				{
				    'UpdateExpression': 'SET #4521760024 = list_append(#4521760024, :LA_4521760024)',
				    'ExpressionAttributeValues':
				    {
				        ':LA_4521760024': [9]
				    },
				    'ExpressionAttributeNames':
				    {
				        '#4521760024': 'hello'
				    }
				}


				WRONG
				WRONG
				>>> expression.UpdateExpression().build({"example.hello": expression.ListAppend("hello", 8), "hello": expression.ListAppend("hello", 9)})
				>>> expression.UpdateExpression().build({"example.hello": expression.ListAppend("example.hello", 8), "hello": expression.ListAppend("hello", 9)})
				{
			    'UpdateExpression': 'SET #6702710449.#4521760024 = list_append(#0977380576, :LA_4521760024), #4521760024 = list_append(#4521760024, :LA_4521760024)',
			    'ExpressionAttributeValues':
			    {
			        ':LA_4521760024': [9]
			    },
			    'ExpressionAttributeNames':
			    {
			        '#6702710449': 'example',
			        '#4521760024': 'hello'
			    }
			}


				>>> expression.UpdateExpression().build({"hello": expression.ListRemove("hello", 7)})
				>>> expression.UpdateExpression().build({"hello": expression.IfNotExists("hello")})

				Increment
				Decrement
				ListAppend
				ListRemove
				SetAppend
				SetRemove
				IfNotExists
			
			
			>>> from pynamite import dynamo;db = dynamo.DB('USER')
			>>> import importlib;importlib.reload(dynamo)
			>>> db = dynamo.DB('USER')
			>>> from pynamite import expression
			>>>	db.update("testing.example", {"count": 0, "list": [11,22,33], "set": {"a", "b", "c"}, "mapping": {"a": 0, "b":"bb", "c": ["cc", "cc", "c"], "d": {"a": "da", "b": "db"}}})
			>>> db.get("testing.example")
			>>> db.get("testing.example", filter_key="count")
			>>> db.delete("testing.example")
			
			>>> db.update("testing.example", {"count": expression.Increment("count")})
			{'count': Decimal('1')}			
			>>> db.update("testing.example", {"count": expression.Decrement("count")})
			{'count': Decimal('0')}
			>>> db.update("testing.example", {"list": expression.ListAppend("list", 8)})
			{'list': [Decimal('11'), Decimal('22'), Decimal('33'), Decimal('8')]}
			>>> db.update("testing.example", {"list": expression.ListRemove("list", 3)})
			FAIL
			>>> db.update("testing.example", {"set": expression.SetAppend("set", "new_item")})
			FAIL
			>>> db.update("testing.example", {"set": expression.SetRemove("set", "SetRemove")})
			FAIL
			>>> db.update("testing.example", {"magic": IfNotExists("magic", "MAGIC")})

			

			expression.UpdateExpression().build({"hello": expression.ListRemove("hello", 7), "hello2": expression.Increment("hello2", 7)})
			
			expression.UpdateExpression().build({"hello": expression.ListRemove("hello", "7, 1"), "hello2": expression.Increment("hello2", 7)})
			


		"""
		# _update_expression = (f"{self.process(k, None, sep='#')}={self.custom_hash(k, v, sep=':')}" for k, v in data.items())

		"This is the statement sent to dynamo, telling it what to do."
		# self.update_expression = "SET " + ", ".join(_update_expression)
		# self.update_expression = "ADD " + ", ".join(self._expression_actions["ADD"])
		# self.update_expression = "REMOVE " + ", ".join(self._expression_actions["REMOVE"])
		# self.update_expression = "DELETE " + ", ".join(self._expression_actions["DELETE"])

		self.update_expression = self._process_actions(data)

		"This represents actual values or data in a dynamodb database"
		# self.attribute_values = self.attribute_values | {self.custom_hash(k, None, sep=':'):v for k,v in data.items() if not isinstance(v, ExpressionBase)}
		# self.attribute_values = self.attribute_values | {self.process(k, None, sep='#'):v for k,v in data.items() if not isinstance(v, ExpressionBase)}
		# for key, value in self.additional_attribute_values:
		# 		self.attribute_values[key] = value
		"This represents actual locations / headers / keys in a dynamodb database"
		# self.attribute_names = self.attribute_names | {self.process(k, None, sep='#'):k for k in data}
		

		return self.dict()
		return pprint(self.dict())



def update(data):
	""" Function is not perfect but it tries to build the UpdateExpression for dynamo table.update_item

		>>> from pynamite.expression import update

		MORE INFO:
		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
	
		It's not able to update nested attributes on dynamo. It can only replace them.
		WHY?
		
		TODO: add nested attr support, ie UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a"

		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html
		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
		
		```
		update-expression ::=
		    [ SET action [, action] ... ]
		    [ REMOVE action [, action] ...]
		    [ ADD action [, action] ... ]
		    [ DELETE action [, action] ...]
		```
		
		# Appending Elements to a List
		"SET #ri = list_append(#ri, :vals)"

		Incrementing and Decrementing Numeric Attributes
		"SET Price = Price - :p"

		Adding Nested Map Attributes
		"SET #pr.#5star[1] = :r5, #pr.#3star = :r3"
		
		# Preventing Overwrites of an Existing Attribute
		"SET Price = if_not_exists(Price, :p)"

		# REMOVE—Deleting Attributes from an Item
		"REMOVE Brand, InStock, QuantityOnHand"

		# Removing Elements from a List
		"REMOVE RelatedItems[1], RelatedItems[2]"

		# Adding Elements to a Set
		"ADD Color :c"

		# DELETE—Removing Elements from a Set
		"DELETE Color :p"
	

		EXAMPLE:
			>>> data = {
				'music': 'Oneee', 
				'instructions': 'Hii', 
				'updated': 1599064200, 
				'updated_iso': '2020-09-03T04:30:00.743834'
			}
			>>> dynamo.update(data)
			(update_expression, expression_attribute_values, expression_attribute_names)
			
			IE

			update_expression
			  'SET #4661479803=:4661479803, #8309902217=:8309902217, #7680784788=:7680784788, #7939007934=:7939007934'
			expression_attribute_values
			  {':4661479803': 'Oneee', ':8309902217': 'Hii', ':7680784788': 1599064200, ':7939007934': '2020-09-03T04:30:00.743834'}
			expression_attribute_names
			  {'#4661479803': 'music', '#8309902217': 'instructions', '#7680784788': 'updated', '#7939007934': 'updated_iso'})


		# hash_func = lambda x, char=':': char + str(hash(x))[1:]  #> ':7585956570055401366'
		# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html

		

		lazy_call("pynamite.dynamo.update", {"one": dynamo.Increment("one")})
		TESTS:
			>>> from pynamite import dynamo
			>>> from pynamite import expression
			>>> expression.update({"one":"two"})
			data:  {'one': 'two'}
			 hashed : #7157953999 
			 hashed : :7157953999 
			 hashed : :7157953999 
			update_expression:  SET #7157953999=:7157953999
			ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES:  []
			expression_attribute_values:  {':7157953999': 'two'}
			 hashed : #7157953999 
			expression_attribute_names {'#7157953999': 'one'}
			
			('SET #7157953999=:7157953999', {':7157953999': 'two'}, {'#7157953999': 'one'})

			>>> expression.update({"one": dynamo.Increment("one")})
			data:  {'count': <pynamite.dynamo.Increment object at 0x7f95e8121c70>}
			 hashed : #0903196091 
			update_expression:  SET #0903196091=#0903196091+:by_one
			ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES:  [(':by_one', Decimal('1'))]
			expression_attribute_values:  {}
			 hashed : #0903196091 
			expression_attribute_names {'#0903196091': 'count'}

			('SET #0903196091=:0903196091+:by_one', {':by_one': Decimal('1')}, {'#0903196091': 'count'})





		Increment
		Decrement
		ListAppend
		ListRemove
		SetRemove
		IfNotExists

		
		>>> from pynamite import expression
		>>> import importlib;importlib.reload(expression)
		>>> 


		>>> from pynamite import dynamo.expression
		>>> from pprint import pprint
		>>> pprint(expression.update({"one":"two"}))
		{'expression_attribute_names': {'#8655921785': 'one'},
		 'expression_attribute_values': {':8655921785': 'two'},
		 'update_expression': 'SET #8655921785=:8655921785'}
		>>> pprint(expression.update({'count': expression.Decrement('count')}))
		{'expression_attribute_names': {'#3170911674': 'count'},
		 'expression_attribute_values': {':D_1': Decimal('1')},
		 'update_expression': 'SET #3170911674 = #3170911674 - :D_1'}
		>>> pprint(expression.update({'count': expression.Decrement('count', 2)}))
		{'expression_attribute_names': {'#3170911674': 'count'},
		 'expression_attribute_values': {':D_2': Decimal('2')},
		 'update_expression': 'SET #3170911674 = #3170911674 - :D_2'}
		

		db.update("example.hello", {"dict_example.hello.b[1]": "B"})


		>>> import importlib;importlib.reload(expression)
		>>> db.update("example.hello", {"dict_example.hello.b[1]": "B"})



		>>> expression.update({"one": expression.SetRemove("key", "two")})
		'DELETE #7513818127 = :SR_1707883424'


	"""

	"This is a list of tuples of key value pairs that need to be added to the alias"
	ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES = [] #>  [(':by_one', Decimal('1'))]



	def hash_func(key, value=None, sep=':'):
		""" 
			
			"#" is for 'expression_attribute_names'
			":" is for 'expression_attribute_values'

			SET #4085567360=:4085567360, #2606051061=:2606051061, #4253647420=:4253647420

			key: str
			value: ExpressionBase | None
			sep: str

			EXAMPLE:
				>>> hash_func(k, sep='#')
				'#7585956570'
				>>> hash_func(k,v)
				':7585956570'
			
			NOTE: function appends a list outside of its direct scope.

		"""
		# if issubclass(v, dynamo.ExpressionBase):
		# 	# created as a short hand to Increment & Decrement where
		# 	# db.update('count_students', Increment)
		# 	v = v(key)
		# 	# this fails on 'expression_attribute_values' TODO
		
		# debug('key', k, v, isinstance(v, ExpressionBase), type(v))
		if isinstance(value, ExpressionBase):
			# debug('hello')
			# hashed = f"#{abs(hash(key))[-10]}" #> '#0055401366'
			# hashed = f"#{abs(hash(key))[-10]}" #> '#0055401366'
			sep = "#"
			hashed = sep + str(abs(hash(key)))[-10:]

			# ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES[value.action] = value.additional_expression_attribute_values
			ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES.append(value.additional_expression_attribute_values)
			output = value.build(hashed)
			debug("ExpressionBase object: ", output)
			return output #> ExpressionBase object
		

		# hashed = f"{sep}{abs(hash(key))[-10]}" #> ':0055401366'
		hashed = sep + str(abs(hash(key)))[-10:] #> ':0055401366'
		debug('')
		debug('hashed: ', hashed, " --> ", key)
		return hashed #> ':758595657


	debug("data: ", data)

	# expression.process()
	# update_expression = "set " + ", ".join([f"{hash_func(k, '#')}={hash_func(k)}" for k in d])

	# GOOD ONE
	update_expression = "SET " + ", ".join([f"{hash_func(k, None, sep='#')} = {hash_func(k, v)}" for k, v in data.items()])
	# update_expression = "SET " + ", ".join([f"{process(k)}={hash_func(k, v)}" for k, v in data.items()])


	# update_expression = "SET " + ", ".join([f"{hash_func(k, sep='#')}={hash_func(k,v)}" for k,v in data.items()])

	# update_expression_list = []
	# update_expression_list = {
	# 	"SET": [],
	# 	"ADD": [],
	# 	"REMOVE": [],
	# 	"DELETE": [],
	# }

	""" WORKING ON THIS """
	# for key, value in data.items():
	# 	expression_key = hash_func(key, sep='#')

	# 	if isinstance(value, ExpressionBase):

	# 		ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES.append(value.additional_expression_attribute_values)
	# 		expression_value = hash_func(key, value, sep='#')
	# 		output = value.build(hashed)
	# 	else:
	# 		expression_value = hash_func(key, value, sep=':')

	# 	update_expression_item = f"{expression_value}={expression_key}"
	# 	update_expression_list.append(update_expression_list)
	""" WORKING ON THIS """

	
	# expression_attribute_values = {hash_func(k):v for k,v in d.items())}
	expression_attribute_values = {hash_func(k, None):v for k,v in data.items() if not isinstance(v, ExpressionBase)}
	# expression_attribute_values = {process(k):v for k,v in data.items() if not isinstance(v, ExpressionBase)}
	#> {':4085567360': 'Oneee', ':2606051061': 'Hii', ':4253647420': '2020-09-03T04:30:00.743834'}
	
	"This is where you add the custom ExpressionBase names - untested."
	# ExpressionBase.additional_expression_attribute_values


	"DEBUGGING"
	debug("update_expression: ", update_expression)
	#> 'SET #4085567360=:4085567360, #2606051061=:2606051061, #4253647420=:4253647420'
	# update_expression += " REMOVE my_list[0]"
	# debug("update_expression", update_expression)

	debug("ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES: ", ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES)
	# expression_attribute_values[':by_one'] = decimal.Decimal(1) 
	debug("expression_attribute_values: ", expression_attribute_values)

	# This looks like a problem.
	for each in ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES:
		expression_attribute_values[each[0]] = each[1]


	# expression_attribute_names = {hash_func(k, sep='#'):k for k in data}
	expression_attribute_names = {hash_func(k, None, sep='#'):k for k in data}
	# expression_attribute_names = {process(k): k for k in data}

	# debug("expression_attribute_names", expression_attribute_names)
	#> {'#4085567360': 'music', '#2606051061': 'instructions', '#4253647420': 'updated'}
	
	# debug('update_expression', update_expression)
	# debug('expression_attribute_values', expression_attribute_values)
	# debug('expression_attribute_names', expression_attribute_names)
	# debug('key', key)
	# debug('attributes_to_update', d)
	debug("")
	return {
		"UpdateExpression": update_expression,
		"ExpressionAttributeValues": expression_attribute_values,
		"ExpressionAttributeNames": expression_attribute_names
	}



# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html

# v.expression_format.format( v.expression_operator)

# if_not_exists (path, value)

# import dynamo;db = dynamo.DB('USER')

# if isinstance(c, Increment)

## WORKING
# db.update('example.hello', {"count":0})
# data2 = {'count': Increment('count')}

## WORKING
# db.update('example.hello', {'count': dynamo.Increment('count')})
# db.update('example.hello', {'count': dynamo.Decrement('count')})

## WORKING
# db.get('example.hello')
# pprint(db.get('example.hello'))

## WORKING
# db.update('example.hello', {'a_list': [0,1]})
# db.update('example.hello', {'a_list': dynamo.ListAppend('a_list', [3,4])})

## WORKING
# db.update('example.hello', {'my_list': [1,2,3,4]})
# db.update('example.hello', {'my_list': dynamo.ListAppend('my_list', [5,6,7])})
# db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [5,6,7])})


## WORKING
# db.update('example.hello', {'my_list': dynamo.ListAppend('my_list', [0,0,0], start=True)})
# db.update('example.hello', {'my_list': dynamo.IfNotExists('my_list', [0,0,0])})

## WORKING
# db.update('example.hello', {'my_list': dynamo.IfNotExists('my_list', [9,9,9])})
# db.update('example.hello', {'my_list_new': dynamo.IfNotExists('my_list_new', [0,0,0])})
# db.get('example.hello')


## NOT WORKING
# >>> db.update('example.hello', {'my_list': dynamo.ListRemove('my_list', [5,6,7])})
# {'my_list': <dynamo.ListRemove object at 0x7f972cee5668>, 'updated': 1636290207, 'updated_iso': '2021-11-08T02:03:27.952948'}
# set #8064923367102735765=REMOVE :vals[#8064923367102735765], #739902644940642721=:739902644940642721, #6674966629363186716=:6674966629363186716
# additional_expression_attribute_values [(':vals', [5, 6, 7])]
# {':739902644940642721': 1636290207, ':6674966629363186716': '2021-11-08T02:03:27.952948'}
# {'#8064923367102735765': 'my_list', '#739902644940642721': 'updated', '#6674966629363186716': 'updated_iso'}
# Invalid UpdateExpression: Syntax error; token: "REMOVE", near: "=REMOVE :vals"



# def update(data):
# 	""" Function is not perfect but it tries to build the UpdateExpression for dynamo table.update_item

# 		MORE INFO:
# 		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
	
# 		It's not able to update nested attributes on dynamo. It can only replace them.
# 		WHY?
		
# 		TODO: add nested attr support, ie UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a"

# 		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html
# 		https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ReservedWords.html
		
# 		```
# 		update-expression ::=
# 		    [ SET action [, action] ... ]
# 		    [ REMOVE action [, action] ...]
# 		    [ ADD action [, action] ... ]
# 		    [ DELETE action [, action] ...]
# 		```
		
# 		# Appending Elements to a List
# 		SET #ri = list_append(#ri, :vals)

# 		Incrementing and Decrementing Numeric Attributes
# 		SET Price = Price - :p

# 		Adding Nested Map Attributes
# 		SET #pr.#5star[1] = :r5, #pr.#3star = :r3
		
# 		# Preventing Overwrites of an Existing Attribute
# 		SET Price = if_not_exists(Price, :p)

# 		# REMOVE—Deleting Attributes from an Item
# 		REMOVE Brand, InStock, QuantityOnHand

# 		# Removing Elements from a List
# 		REMOVE RelatedItems[1], RelatedItems[2]

# 		# Adding Elements to a Set
# 		ADD Color :c

# 		# DELETE—Removing Elements from a Set
# 		DELETE Color :p
	
# 		EXAMPLE:
# 			>>> data = {
# 				'music': 'Oneee', 
# 				'instructions': 'Hii', 
# 				'updated': 1599064200, 
# 				'updated_iso': '2020-09-03T04:30:00.743834'
# 			}
# 			>>> dynamo.update(data)
# 			(update_expression, expression_attribute_values, expression_attribute_names)
			
# 			IE
# 			  update_expression: 
# 			    'set #40855673607481416=:40855673607481416, #260605106150357403=:260605106150357403, #016731958467557352=:016731958467557352, #4253647420496117444=:4253647420496117444'
# 			  expression_attribute_values: 
# 			    {':40855673607481416': 'Oneee', ':260605106150357403': 'Hii', ':016731958467557352': 1599064200, ':4253647420496117444': '2020-09-03T04:30:00.743834'}
# 			  expression_attribute_names: 
# 			    {'#40855673607481416': 'music', '#260605106150357403': 'instructions', '#016731958467557352': 'updated', '#4253647420496117444': 'updated_iso'}
	
# 		# hash_func = lambda x, char=':': char + str(hash(x))[1:]  #> ':7585956570055401366'
# 		# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
# 	"""

# 	# ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES = []
# 	ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES = {}

# 	def hash_func(k, v=None, sep=':'):
# 		""" 
# 			k: str
# 			v: ExpressionBase | None
# 			sep: str

# 			EXAMPLE:
# 				>>> hash_func(k, char='#')
# 				'#7585956570055401366'
# 				>>> hash_func(k,v)
# 				':7585956570055401366'
			
# 			NOTE: function appends a list outside of its direct scope.
# 		"""
# 		# if issubclass(v, dynamo.ExpressionBase):
# 		# 	# created as a short hand to Increment & Decrement where
# 		# 	# db.update('count_students', Increment)
# 		# 	v = v(key)
# 		# 	# this fails on 'expression_attribute_values' TODO
		
# 		# debug('key', k, v, isinstance(v, ExpressionBase), type(v))
# 		if isinstance(v, ExpressionBase):
# 			# debug('hello')
# 			hashed = '#' + str(int(hash(k)))[1:] #> '#7585956570055401366'
# 			ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES.append(v.additional_expression_attribute_values)
# 			return v.create(hashed) #> ExpressionBase object
		
# 		hashed = sep + str(int(hash(k)))[1:] #> ':7585956570055401366'
# 		debug('', 'hashed', hashed, '')
# 		return hashed #> ':7585956570055401366'

# 	debug("data", data)
# 	# update_expression = "set " + ", ".join([f"{hash_func(k, '#')}={hash_func(k)}" for k in d])
# 	update_expression = "SET " + ", ".join([f"{hash_func(k, sep='#')}={hash_func(k,v)}" for k,v in data.items()])
# 	#> 'set #40855673607481416=:40855673607481416, #260605106150357403=:260605106150357403, #016731958467557352=:016731958467557352, #4253647420496117444=:4253647420496117444'
# 	debug("update_expression", update_expression)
# 	# update_expression += " REMOVE my_list[0]"
# 	# debug("update_expression", update_expression)
	
# 	# expression_attribute_values = {hash_func(k):v for k,v in d.items())}
# 	expression_attribute_values = {hash_func(k):v for k,v in data.items() if not isinstance(v, ExpressionBase)}
# 	#> {':40855673607481416': 'Oneee', ':260605106150357403': 'Hii', ':016731958467557352': 1599064200, ':4253647420496117444': '2020-09-03T04:30:00.743834'}
	
# 	"This is where you add the custom ExpressionBase names - untested."
# 	# ExpressionBase.additional_expression_attribute_values

# 	debug('additional_expression_attribute_values', ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES)
# 	# expression_attribute_values[':by_one'] = decimal.Decimal(1) 
# 	debug("expression_attribute_values", expression_attribute_values)

# 	for each in ADDITIONAL_EXPRESSION_ATTRIBUTE_VALUES:
# 		expression_attribute_values[each[0]] = each[1]


# 	expression_attribute_names = {hash_func(e, None, '#'):e for e in data}
# 	debug("expression_attribute_names", expression_attribute_names)
# 	#> {'#40855673607481416': 'music', '#260605106150357403': 'instructions', '#016731958467557352': 'updated', '#4253647420496117444': 'updated_iso'}
	
# 	# debug('update_expression', update_expression)
# 	# debug('expression_attribute_values', expression_attribute_values)
# 	# debug('expression_attribute_names', expression_attribute_names)
# 	# debug('key', key)
# 	# debug('attributes_to_update', d)

# 	return update_expression, expression_attribute_values, expression_attribute_names