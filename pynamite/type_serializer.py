""" 

Type serializer/deserializer for converting between python & AWS dynamo db type notation.


EXAMPLE:

>>> from pynamite.type_serializer import serialize, deserialize
>>> serialize({"example": [1,2,3]})
{'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}}
>>> deserialize({'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}})
{"example": [1,2,3]}


RESOURCES:
 - https://github.com/boto/boto3/blob/develop/boto3/dynamodb/types.py


STATUS - COMPLETE

"""


from boto3.dynamodb.types import TypeSerializer
from boto3.dynamodb.types import TypeDeserializer


TYPE_SERIALIZE = TypeSerializer()
TYPE_DESERIALIZE = TypeDeserializer()


def serialize(value):
	""" serialize a python onject to aws specification

		 Python                                  DynamoDB
		------                                  --------
		None                                    {'NULL': True}
		True/False                              {'BOOL': True/False}
		int/Decimal                             {'N': str(value)}
		string                                  {'S': string}
		Binary/bytearray/bytes (py3 only)       {'B': bytes}
		set([int/Decimal])                      {'NS': [str(value)]}
		set([string])                           {'SS': [string])
		set([Binary/bytearray/bytes])           {'BS': [bytes]}
		list                                    {'L': list}
		dict                                    {'M': dict}

		EXAMPLES:
			>>> serialize({"example": [1,2,3]})
			{'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}}
			>>> serialize({"example": ["1","2","3"]})
			{'M': {'example': {'L': [{'S': '1'}, {'S': '2'}, {'S': '3'}]}}}
			>>> serialize([1,2,3,4])
			{'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}, {'N': '4'}]}
			>>> serialize(1)
			{'N': '1'}
			>>> serialize(True)
			{'BOOL': True}
			>>> serialize(None)
			{'NULL': True}
			>>> serialize(bytes("magic".encode()))
			{'B': b'magic'}
	"""
	return TYPE_SERIALIZE.serialize(value)


def deserialize(value):
	""" deserialize a aws specification to a python onject

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

		EXAMPLES:
			>>> deserialize({'M': {'example': {'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}]}}})
			{"example": [1,2,3]}
			>>> deserialize({'M': {'example': {'L': [{'S': '1'}, {'S': '2'}, {'S': '3'}]}}})
			{"example": ["1","2","3"]}
			>>> deserialize({'L': [{'N': '1'}, {'N': '2'}, {'N': '3'}, {'N': '4'}]})
			[1,2,3,4]
			>>> deserialize({'N': '1'})
			1
			>>> deserialize({'BOOL': True})
			True
			>>> deserialize({'NULL': True})
			None
			>>> deserialize({'B': b'magic'})
			Binary(b'magic')
		
	"""
	return TYPE_DESERIALIZE.deserialize(value)






