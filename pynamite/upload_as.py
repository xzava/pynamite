"""

Upload Json to DYNAMODB

"""

# NOTE: This is the format of a offical dynamodb backup 
"""
{"Item":{"PK":{"S":"one"},"SK":{"S":"example"},"updated_iso":{"S":"2021-05-29T05:17:14.682836"},"created":{"N":"1622222234"},"updated":{"N":"1622222234"},"data2":{"N":"2"},"created_iso":{"S":"2021-05-29T05:17:14.682836"}}}
{"Item":{"PK":{"S":"hello"},"SK":{"S":"earth"},"two":{"S":"two"},"tid":{"S":"magic"},"three":{"S":"three"},"one":{"S":"one"}}}
{"Item":{"PK":{"S":"one"},"SK":{"S":"example2"},"data":{"S":"7"}}}
{"Item":{"PK":{"S":"hello"},"SK":{"S":"land"},"two":{"S":"two2"},"three":{"S":"three"},"one":{"S":"one"}}}
{"Item":{"PK":{"S":"hello"},"SK":{"S":"one"},"created":{"N":"1617313924"},"created_iso":{"S":"2021-04-02T10:52:04.976474"},"one":{"S":"two"},"sort":{"S":"okay"},"updated":{"N":"1617313924"},"updated_iso":{"S":"2021-04-02T10:52:04.976474"}}}
{"Item":{"PK":{"S":"example"},"SK":{"S":"name"},"created":{"N":"1610534514"},"created_iso":{"S":"2021-01-13T23:41:54.917338"},"oneone":{"S":"threethree"},"updated":{"NULL":true},"updated_iso":{"NULL":true}}}
{"Item":{"PK":{"S":"example"},"SK":{"S":"name2"},"data":{"M":{"PK":{"S":"example"},"SK":{"S":"name"}}},"dataa":{"M":{"PK":{"S":"example"},"SK":{"S":"name"}}},"hello":{"S":"there"},"updated":{"N":"1610536476"},"updated_iso":{"S":"2021-01-14T00:14:36.939146"}}}
{"Item":{"PK":{"S":"hello"},"SK":{"S":"world"},"two":{"S":"two"},"three":{"S":"three"},"one":{"S":"one"}}}
"""




all_data = {
	"123": {
		"CUST#123": {
			"email": "shirley@example.net",
			"fullName": "Shirley Rodriguez",
			"userPreferences": {"language": "en", "sort": "date", "sortDirection": "ascending"},
		},
		"https://aws.amazon.com": {
			"createDate": "2020-03-25T09:16:46-07:00",
			"updateDate": "2020-03-25T09:16:46-07:00",
			"folder": "Cloud",
			"title": "AWS",
			"description": "Amazon Web Services",
			"url": "https://aws.amazon.com",
			},
		"https://console.aws.amazon.com": {
			"createDate": "2020-03-25T09:16:43-07:00",
			"updateDate": "2020-03-25T09:16:43-07:00",
			"folder": "Cloud",
			"title": "AWS Console",
			"description": "Web console",
			"url": "https://console.aws.amazon.com",
		}
	},
	"321": {
		"CUST#321": {
			"email": "zhang@example.net",
			"fullName": "Zhang Wei",
			"userPreferences": {"language": "zh", "sort": "rating", "sortDirection": "descending"},
		},
		"https://aws.amazon.com": {
			"createDate": "2020-03-25T09:16:46-07:00",
			"updateDate": "2020-03-25T09:16:46-07:00",
			"folder": "Tools",
			"title": "AWS",
			"description": "Amazon Web Services",
			"url": "https://aws.amazon.com",
			},
		"https://docs.aws.amazon.com": {
			"createDate": "2020-03-25T09:16:43-07:00",
			"updateDate": "2020-03-25T09:16:43-07:00",
			"folder": "Docs",
			"title": "AWS Docs",
			"description": "Documentation",
			"url": "https://docs.aws.amazon.com",
		}
	}
}



def push_local_db(db, data):
	""" Push json structure to dynamodb

		Data has to be structured {PK: {SK: {...}, SK: {...}}}

	"""
	push_db = lambda PK, value: [db.update([PK, k], v) for k,v in value.items()]
	# [push_db(PK, value) for PK, value in all_data.items()]
	for PK, value in all_data.items():
		push_db(PK, value)


def push_backup(db, filename):
	""" Upload offical dynamodb backup, line by line
		
		// awsbackup.json
		'''
		{"Item":{"PK":{"S":"one"},"SK":{"S":"example1"},"data":{"S":"7"}}}
		{"Item":{"PK":{"S":"one"},"SK":{"S":"example2"},"data":{"S":"7"}}}
		'''
		
		from type_serializer import serialize, deserialize
	"""

	with open(filename, "r") as lines:

		print(f"DynamoDB backup has records: {f.fileno()}")
		for i, eline in enumerate(lines):
			record = json.loads(line.strip())["Items"]
			PK = record.pop("PK", None)
			SK = record.pop("SK", None)
			db.update([PK, SK], record, ReturnValues="NONE")

	print("SUCCESS: Backup uploaded to dynamodb")


	




	# push_db = lambda PK, value: [db.update([PK, k], v, ReturnValues="NONE") for k,v in value.items()]
	# [push_db(PK, value) for PK, value in all_data.items()]