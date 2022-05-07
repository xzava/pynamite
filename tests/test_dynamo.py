"""

Testing functions in `dynamo` ...


FUNCTIONS:


pytest tests/dynamo.py

pytest tests

"""

from pynamite import dynamo
db = dynamo.DB('TEST_TABLE')


def test_get():
	""" TEST:
	"""
	db.get()


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

