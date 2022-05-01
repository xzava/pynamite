"""

Testing functions in `type_serializer` convert a python object into dynamodb type notation

ie

	DynamoDB                                Python
	--------                                ------
	{'NULL': True}                          None
	{'BOOL': True/False}                    True/False
	{'N': str(value)}                       Decimal(str(value))
	{'S': string}                           string
	{'B': bytes}                            Binary(bytes)
	{'NS': [str(value)]}                    set([Decimal(str(value))])
	{'SS': [string]}                        set([string])
	{'BS': [bytes]}                         set([bytes])
	{'L': list}                             list
	{'M': dict}                             dict



FUNCTIONS:

	serialize()
	deserialize()



pytest tests/test_type_serializer.py

pytest tests

"""


# test_serialize
# test_deserialize
# test_serialize_deserialize


def test_serialize():
	""" TEST: `serialize` from pynamite.type_serializer
	"""
	from pynamite.type_serializer import serialize, deserialize

	examples = [
		{"example": [1,2,3]}
	]

	results = [
		{'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}}
	]

	for example, result in zip(examples, results): 
		actual = serialize(example)
		expected = result
		assert actual == expected

	print("serialize passed all tests")
	
	

def test_deserialize():
	""" TEST: `deserialize` from pynamite.type_serializer
	"""
	from pynamite.type_serializer import serialize, deserialize

	examples = [
		{'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}}
	]

	results = [
		{"example": [1,2,3]}
	]

	for example, result in zip(examples, results): 
		actual = deserialize(example)
		expected = result
		assert actual == expected

	print("serialize passed all tests")
	


def test_serialize_deserialize():
	""" TEST: `serialize` from pynamite.type_serializer
	"""
	from pynamite.type_serializer import serialize, deserialize

	examples = [
		{"example": [1,2,3]}
	]

	results = [
		{'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}}
	]

	for example, result in zip(examples, results): 
		actual = serialize(deserialize(serialize(example)))
		expected = deserialize(serialize(result))
		assert actual == expected

	print("serialize deserialize - reversable passed all tests")