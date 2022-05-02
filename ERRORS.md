// ERRORS.md


`DATE`: 17.04.22 - 19.04.22
`PROBLEM`: reserved keywords in .get_item ProjectionExpression need to be mapped
`STAUS`: DONE 
`DETAILS`: 

get_item also needs the auto encoding logic from update_item

```bash

>>> db.get("testing.example", filter_key="count")
Invalid ProjectionExpression: Attribute name is a reserved keyword; reserved keyword: count
WARNING: returning default response.
>>>

```

`CHANGE`: Used the expression.UpdateExpression class


------------
------------
------------
------------

`DATE`: 19.04.22 - 
`PROBLEM`: When Dot notation is actually just a string.
`STAUS`: In progress
`DETAILS`: 

The dot in 'Safety.Warning' should be ingored

```bash
aws dynamodb get-item \
    --table-name ProductCatalog \
    --key '{"Id":{"N":"123"}}' \
    --projection-expression "#sw" \
    --expression-attribute-names '{"#sw":"Safety.Warning"}'
```


`CHANGE`: replace_between() function has been written


------------
------------
------------
------------

`DATE`: 02.05.22 - 
`PROBLEM`: Missing _created key when using update and a record doesnt exist.
`STAUS`: In progress
`DETAILS`: 

Should add IfNotExists("_created")

and '_updated' should be blank

>>> db.get("USER.#ACTIVE#ACC_45438981")
{'_updated': '2022-05-01T23:01:52.470557', 'firstname': 'John', 'SK': '#ACTIVE#ACC_45438981', 'PK': 'USER', 'email': 'john@example.com', 'verified': True}



------------
------------
------------
------------


`DATE`: 02.05.22 
`PROBLEM`: expression SetRemove is not working
`STAUS`: In progress
`DETAILS`: 

Should be the following

>>> from pynamite import expression
>>> expression.update({"one": expression.SetRemove("key", "two")})
'DELETE #7513818127 = :SR_1707883424'

But is currently this 

'SET #7513818127 = :SR_1707883424 #7513818127'