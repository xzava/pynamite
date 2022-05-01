

def dynamo_schema_to_dict(data):
	""" Schema from nosql workbench to dict

	{
	    'OFR#10041': {
	        'OFR#10041#ITEM#1':
	        {
	            'PK': {'S': 'OFR#10041'},
	            'SK': {'S': 'OFR#10041#ITEM#1'},
	            'OfferId': {'N': '10041'},
	            'OfferItemId': {'S': '1'},
	            'AprType': {'S': 'INT'},
	            'AprRate': {'N': '0'},
	            'APRDurationInMonths': {'S': '12'}
	        },
	        'OFR#10041#ITEM#2': {
	            'PK': {'S': 'OFR#10041'},
	            'SK': {'S': 'OFR#10041#ITEM#2'},
	            'OfferId': {'N': '10041'},
	            'OfferItemId': {'S': '2'},
	            'AprType': {'S': 'VAR'},
	            'AprRate': {'N': '12.5'},
	            'APRDurationInMonths': {'S': '12'}
	        },
	        'OFR#10041#ITEM#3': {
	            'PK': {'S': 'OFR#10041'},
	            'SK': {'S': 'OFR#10041#ITEM#3'},
	            'OfferId': {'N': '10041'},
	            'OfferItemId': {'S': '3'},
	            'AprType': {'S': 'FIX'},
	            'AprRate': {'N': '19.99'}
	        }
	    }
	}

	"""
	from collections import defaultdict
	result = defaultdict(dict)
	# [result["TableData"] for e in data]

	for each in data2:
	    PK = list(each["PK"].items())[0][-1]
	    SK = list(each["SK"].items())[0][-1]
	    # result[PK] = dict()
	    result[PK][SK] = each
	    # result[each["FacetName"]] = each["TableData"]
	    
	dict(result)
