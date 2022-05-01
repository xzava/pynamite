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