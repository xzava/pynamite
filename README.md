> README.md


# Python Wrapper for the boto3 dynamoDB library

Library is built around single table design, and tries to keep the boto3 dynamodb interface, just without the bloat.


<p align="center">
  <img src="https://raw.githubusercontent.com/xzava/pynanite/master/docs/images/wile.jpg">
</p>



## Project status - Alpha

Used in production, with a very narrow scope. Things within the scope work very well things outside of the scope require your feedback.


### Installation

```bash
pip install git+https://github.com/xzava/pynamite.git --upgrade

# or for development
git clone https://github.com/xzava/pynamite.git
cd pynamite
python setup.py develop
```

### SETUP

Next, set up credentials (in e.g. ~/.aws_key_location):

```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
Then, set up a default region (in e.g. ~/.aws/config):

[default]
region=us-east-1

```

```sh
# ~/aws_key_location.sh

# Required Config..
export AWS_ACCESS_KEY_ID='YOUR_KEY'
export AWS_SECRET_ACCESS_KEY='YOUR_SECRET'
export DYNAMO_REGION='YOUR REGION'

# Optional Config..
export DYNAMO_TABLE_NAME='TABLE NAME' 
export DEBUG='DEBUG'
```

```bash
source ~/.aws_key_location.sh
```


### QUICK EXAMPLE

##### Bookmark Datamodel

<p align="center">
  <img src="https://raw.githubusercontent.com/xzava/pynanite/master/docs/images/bookmarks_data_model.png">
</p>

```python

# Using the bookmarks datamodel from nosql workbench examples

>>> from pynamite import dynamo
>>> db = dynamo.DB('bookmarks')
>>> db.get(["123", "CUST#123"])
{
  "email": "shirley@example.net",   
  "fullName": "Shirley Rodriguez",  
  "userPreferences": {"language": "en", "sort": "date", "sortDirection": "ascending"}
}
>>> db.get(["123", "https://aws.amazon.com"], "createDate, folder, url")
{
  "createDate": "2020-03-25T09:16:46-07:00",
  "folder": "Cloud",
  "url": "https://aws.amazon.com"
}
>>> db.update(["123", "https://aws.amazon.com"], {
  "updateDate": "2020-03-25T09:16:46-07:00",
  "folder": "Work"
})
>>> db.get_partition("123")
[
  {
    'PK': '123',
    'SK': 'CUST#123',
    'userPreferences': {
      'language': 'en',
      'sortDirection': 'ascending',
      'sort': 'date'
    },
    'email': 'shirley@example.net',
    'fullName': 'Shirley Rodriguez'
  },
  {
    'PK': '123',
    'SK': 'https://aws.amazon.com',
    'updateDate': '2020-03-25T09:16:46-07:00',
    'createDate': '2020-03-25T09:16:46-07:00',
    'description': 'Amazon Web Services',
    'folder': 'Cloud',
    'url': 'https://aws.amazon.com',
    'title': 'AWS'
  },
  {
    'PK': '123',
    'SK': 'https://console.aws.amazon.com',
    'updateDate': '2020-03-25T09:16:43-07:00',
    'createDate': '2020-03-25T09:16:43-07:00',
    'description': 'Web console',
    'folder': 'Cloud',
    'url': 'https://console.aws.amazon.com',
    'title': 'AWS Console'
  }
]


>>> db.get("321.CUST#321", "userPreferences.language")
{'userPreferences': {'language': 'zh'}}

>>> db.get("321.CUST#321", "userPreferences.gpsLocation")
{}
```


#### Note: 

The last example, you are requesting a filter from AWS, they process this after they have read the record. So you get charged the same amount compared to requesting the full record. The benefit is bandwidth/network traffic.

#### Pro tip: 

This datamodel the "SK" should ideally be "URL#https://aws.amazon.com"
So a user can query all records from user "123" that start with "URL#" 


### USAGE

##### Datamodel for a cloud video service

<p align="center">
  <img src="https://raw.githubusercontent.com/xzava/pynanite/master/docs/images/youtubeclone_data_model.png">
</p>

```python
>>> from pynamite import dynamo

# Connect to existing DynamoDB table named 'youtubeclone.com'
>>> db = dynamo.DB('youtubeclone.com')

# Create two users
>>> db.update(["USER", "#ACTIVE#ACC_45438981"], {"firstname": "John", "email": "john@example.com", "verified": True})
>>> db.update(["USER", "#ACTIVE#ACC_15464279"], {"firstname": "Penny", "email": "penny@example.com", "verified": False})

# Get a user
>>> db.get("USER.#ACTIVE#ACC_45438981")
{
	"PK": "USER",
	"SK": "#ACTIVE#ACC_45438981",
	"firstname": "John",
	"verified": True,
	"email": "john@example.com",
	"_created": "2022-04-02T10:52:04.976474",
	"_updated": ""
}

# User creates a channel
>>> db.update(["CHANNEL", "#penny_makes_things"], {"author": "ACC_15464279", "videos": 0, "subscribers": 0, "channel": "penny_makes_things"})

# Update a user record, they have verified their email & return full item
>>> db.update(["USER", "#ACTIVE#ACC_15464279"], {"verified": True}, ReturnValues="ALL_NEW")
{
	"PK": "USER",
	"SK": "#ACTIVE#ACC_15464279",
	"firstname":"Penny",
	"author": "ACC_15464279"
	"channel": "penny_makes_things",
	"verified": True,
	"email": "penny@example.com",
	"_created": "2022-04-02T10:52:04.976474",
	"_updated": "2022-04-02T10:58:03.172424"
}

# User adds a video to their channel
>>> db.update(["VIDEO", "#VID_15464279"], {"Title": "How to make soup", "views": 0, "author": "ACC_15464279", "channel": "penny_makes_things"})

# Increment channel attr videos plus 1
>>> db.update(["CHANNEL", "#ACTIVE#ACC_15464279"], {"videos": Increment("videos")})

# User video gets 3 views
>>> db.update(["VIDEO", "#VID_15464279"], {"views": Increment("views")})
>>> db.update(["VIDEO", "#VID_15464279"], {"views": Increment("views")})
>>> db.update(["VIDEO", "#VID_15464279"], {"views": Increment("views")})

# User gets two subscribers, update their channel model
>>> db.update(["CHANNEL", "#ACTIVE#ACC_15464279"], {"subscribers": Increment("subscribers")})
>>> db.update(["CHANNEL", "#ACTIVE#ACC_15464279"], {"subscribers": Increment("subscribers")})

# Get video information
>>> db.get(["VIDEO", "#VID_15464279"])
{
	"PK": "VIDEO",
	"SK": "#VID_15464279",
	"firstname":"Penny",
	"channel": "penny_makes_things",
	"author": "VID_15464279"
	"email": "penny@example.com",
	"_created": "2022-04-02T10:52:04.976474",
	"_updated": "2022-04-02T10:58:03.172424"
}

# Get channel information
>>> db.get("CHANNEL.#penny_makes_things")
{
	"author": "ACC_15464279", 
	"videos": 1, 
	"subscribers": 2,
	"channel": "penny_makes_things",
	"_created": "2022-04-02T10:52:04.976474",
	"_updated": "2022-04-02T10:58:03.172424"
}

# User is naughty..
>>> db.update("VIDEO.#VID_15464279", {
	"__shadow_ban_level": {"MODERATE"}
})

# Elon Musk buys company
>>> db.update("VIDEO.#VID_15464279", {"__shadow_ban_level": SetRemove("MODERATE")}, ReturnValues="ALL_NEW")
{
	"__shadow_ban_level": {}
}
```


```python

from pynanite import dynamo
from pprint import pprint

db = dynamo.DB('USER')

db.put('example.hello', {'count': 0})
# {'PK': 'example', 'SK': 'hello', 'size': 132}

example = db.get('example.hello')
pprint(example)
# {
#     'SK': 'hello',
#     'PK': 'example',
#     'count': Decimal('0'),
#     '_created': '2022-04-14T00:52:29.862785',
#     '_updated': '2022-04-14T00:52:29.862785'
# }

pprint(db.update('example.hello', {'count': dynamo.Increment('count')}))
# {'_updated': '2022-04-14T00:55:21.683986', 'count': Decimal('1')}
pprint(db.update('example.hello', {'count': dynamo.Increment('count')}))
# {'_updated': '2022-04-14T01:05:23.290422', 'count': Decimal('2')}

```


## Modelling with AWS nosql work bench

<p align="center">
  <img src="https://raw.githubusercontent.com/xzava/pynanite/master/docs/images/tabledesign_style.png">
</p>


```python


create_nosql_workbench(filename="table.json")


```



## Advcanced Examples:

```python

>>> db.query("123")
>>> db.scan("123")

```


## Why use dynamo from pynamite

boto3 is heavy and hard to learn, this library acts as a wrapper keeping the same interface but keeping it simple.

You can interact with the DynamoDB like python dict, meaning you can get things up and running quicker.

Other libraies focus on adhock .query and .scan, DynamoDB is not SQL using these transactions should be the exception.
IE access patterns should be built into the datamodel, and GSI (Global Secondary index) should be used for common read heavy access patterns.

This library supports single table design, and nosql style data modelling.


## Future changes

- Connect pynamite to pandas

- Add datamodel support, likly using attrs

- Add callback transactions, ie if a video record is added automaticlly update the channel record to increment "videos" dynamoDB supports this use case using lambda functions

- Add a video showing examples, one thing I had trouble was finding dynamoDB example functions.


