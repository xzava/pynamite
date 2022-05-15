"""

Testing functions in `dynamo` ...


FUNCTIONS:


pytest tests/dynamo.py

pytest tests

"""

from pynamite import dynamo
db = dynamo.DB('TEST_TABLE')


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


def test_get():
	""" TEST:
	"""
	db.get()

def test_get():
	""" TEST:
	"""
	db.get_partition()


def test_update():
	""" TEST:
	"""
	db.update()


def test_scan():
	""" TEST:
	"""
	dynamo.scan()


def test_query():
	""" TEST:
	"""
	db.query()


def test_put():
	""" TEST:
	"""
	db.put()


def test_delete():
	""" TEST:
	"""
	db.delete()


def test_facet():
	""" TEST:
	"""
	db.facet()


def test_schema():
	""" TEST:
	"""
	db.schema()


def test_create_table():
	""" TEST:
	"""
	dynamo.create_table()


def test_create_gsi():
	""" TEST:
	"""
	dynamo.create_gsi()


def test_download():
	""" TEST:
	"""
	db.get()

