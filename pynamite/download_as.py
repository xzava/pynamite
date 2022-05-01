from copy import deepcopy
from decimal import Decimal
from datetime import datetime

from type_serializer import serialize, deserialize
"""

Download a dynamodb Table

USAGE:
	from download_as import download_db_simple
	from download_as import download_db_dict
	from download_as import download_db_aws


	>>> download_db_simple(db)
	>>> download_db_dict(db)
	>>> download_db_aws(db)

"""

basemodel = {
  "ModelName": "Credit Card Offers Data Model",
  "ModelMetadata": {
    "Author": "Amazon Web Services, Inc.",
    "DateCreated": "May 1, 2020, 11:00 AM",
    "DateLastModified": "May 17, 2021, 03:17 PM",
    "Description": "This data model represents an Amazon DynamoDB model for credit card account offers that are part of a Credit Card Offers Application.\n\nA credit card provider designs offers over time, including balance transfers without fees, increased credit limits, lower interest rates, cash back, and airline miles. After a customer accepts or declines these offers, the respective offer status is updated accordingly.\n\nThe model’s data can be modeled in many ways. In this data model, we chose to use a single-table design and a prejoin access pattern for maintaining one-to-many relationships among entities such as Accounts, Offers, AccountOffers, and OfferItems. As a result, the retrieval of the data is near real time at scale. \n\nUnlike a relational database with a normalized schema with many entities and joins among them to fetch accounts and offers, this model’s key access patterns represent constant time data retrieval at scale.\n\nNote: for demonstration purpose, the attribute names have been kept descriptive and human readable. In real model, it is recommended to use shorter and less human readable attribute names to save space on disk and in every response that gets sent back.\n\nThe important access patterns facilitated by this data model are:\n\t* Retrieval of account records using AccountId, as facilitated by the main table\n        * Retrieval of all the accounts with few projected items, as facilitated by the secondary index AccountIndex\n\t* Retrieval of accounts and all the offer records associated with those accounts by using AccountId, as facilitated by the main table\n\t* Retrieval of accounts and specific offer records associated with those accounts by using AccountId and OfferId, as facilitated by the main table\n\t* Retrieval of all ACCEPTED/DECLINED offer records of specific OfferType associated with accounts using AccountId, OfferType, and Status, as facilitated by the secondary index GSI1\n\t* Retrieval of offers and associated offer item records using OfferId, as facilitated by the main table",
    "Version": "3.0",
    "AWSService": "Amazon DynamoDB"
  },
  "DataModel": [
    {
      "TableName": "CreditCardOffers",
      "KeyAttributes": {
        "PartitionKey": {
          "AttributeName": "PK",
          "AttributeType": "S"
        },
        "SortKey": {
          "AttributeName": "SK",
          "AttributeType": "S"
        }
      },
      "NonKeyAttributes": [
        {
          "AttributeName": "AccountId",
          "AttributeType": "N"
        },
        {
          "AttributeName": "PlasticCardNumber",
          "AttributeType": "S"
        },
        {
          "AttributeName": "FirstName",
          "AttributeType": "S"
        },
        {
          "AttributeName": "MiddleName",
          "AttributeType": "S"
        },
        {
          "AttributeName": "LastName",
          "AttributeType": "S"
        },
        {
          "AttributeName": "Emailid",
          "AttributeType": "S"
        },
        {
          "AttributeName": "Addresses",
          "AttributeType": "M"
        },
        {
          "AttributeName": "OfferId",
          "AttributeType": "N"
        },
        {
          "AttributeName": "OfferType",
          "AttributeType": "S"
        },
        {
          "AttributeName": "OfferDescription",
          "AttributeType": "S"
        },
        {
          "AttributeName": "OfferSubType",
          "AttributeType": "S"
        },
        {
          "AttributeName": "OfferEffectiveDate",
          "AttributeType": "S"
        },
        {
          "AttributeName": "OfferExpiryDate",
          "AttributeType": "S"
        },
        {
          "AttributeName": "CreatedDate",
          "AttributeType": "S"
        },
        {
          "AttributeName": "CreatedBy",
          "AttributeType": "S"
        },
        {
          "AttributeName": "LastModified",
          "AttributeType": "S"
        },
        {
          "AttributeName": "OfferUrl",
          "AttributeType": "S"
        },
        {
          "AttributeName": "AccountOfferStartDate",
          "AttributeType": "S"
        },
        {
          "AttributeName": "AccountOfferEndDate",
          "AttributeType": "S"
        },
        {
          "AttributeName": "Status",
          "AttributeType": "S"
        },
        {
          "AttributeName": "StatusChangeDate",
          "AttributeType": "S"
        },
        {
          "AttributeName": "AccountIndexId",
          "AttributeType": "S"
        },
        {
          "AttributeName": "GSI1SK",
          "AttributeType": "S"
        },
        {
          "AttributeName": "CreditLimit",
          "AttributeType": "N"
        },
        {
          "AttributeName": "BalanceTransferFeePct",
          "AttributeType": "N"
        },
        {
          "AttributeName": "BalanceTransferLimit",
          "AttributeType": "N"
        },
        {
          "AttributeName": "CashBackPct",
          "AttributeType": "N"
        },
        {
          "AttributeName": "Miles",
          "AttributeType": "N"
        },
        {
          "AttributeName": "OfferItemId",
          "AttributeType": "S"
        },
        {
          "AttributeName": "AprType",
          "AttributeType": "S"
        },
        {
          "AttributeName": "AprRate",
          "AttributeType": "N"
        },
        {
          "AttributeName": "APRDurationInMonths",
          "AttributeType": "S"
        },
        {
          "AttributeName": "AuthUsers",
          "AttributeType": "M"
        }
      ],
      "TableFacets": [
        {
          "FacetName": "Accounts",
          "KeyAttributeAlias": {
            "PartitionKeyAlias": "PK",
            "SortKeyAlias": "SK"
          },
          "TableData": [
            {
              "PK": {
                "S": "ACCT#76584123"
              },
              "SK": {
                "S": "ACCT#76584123"
              },
              "AccountId": {
                "N": "76584123"
              },
              "PlasticCardNumber": {
                "S": "4235400034568756"
              },
              "FirstName": {
                "S": "Zhang"
              },
              "LastName": {
                "S": "Wei"
              },
              "Emailid": {
                "S": "zhang.wei@example.com"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "135 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "100 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#76584123"
              },
              "AuthUsers": {
                "M": {
                  "AUTHUSER-1": {
                    "M": {
                      "Name": {
                        "S": "Paulo Santos"
                      },
                      "PlasticCardNumber": {
                        "S": "4036546984262340"
                      }
                    }
                  },
                  "AUTHUSER-2": {
                    "M": {
                      "Name": {
                        "S": "Mateo Jackson"
                      },
                      "PlasticCardNumber": {
                        "S": "4036516984267960"
                      }
                    }
                  }
                }
              }
            },
            {
              "PK": {
                "S": "ACCT#11584123"
              },
              "SK": {
                "S": "ACCT#11584123"
              },
              "AccountId": {
                "N": "11584123"
              },
              "PlasticCardNumber": {
                "S": "4235400134568790"
              },
              "FirstName": {
                "S": "Li"
              },
              "LastName": {
                "S": "Juan"
              },
              "Emailid": {
                "S": "li.juan12@example.com"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "125 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "101 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#11584123"
              }
            },
            {
              "PK": {
                "S": "ACCT#76584657"
              },
              "SK": {
                "S": "ACCT#76584657"
              },
              "AccountId": {
                "N": "76584657"
              },
              "PlasticCardNumber": {
                "S": "4235400034561244"
              },
              "FirstName": {
                "S": "Ana"
              },
              "MiddleName": {
                "S": "Carolina"
              },
              "LastName": {
                "S": "Silva"
              },
              "Emailid": {
                "S": "anacsilva@example.com"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "120 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "111 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#76584657"
              },
              "AuthUsers": {
                "M": {
                  "AUTHUSER-1": {
                    "M": {
                      "Name": {
                        "S": "Mary Major"
                      },
                      "PlasticCardNumber": {
                        "S": "4411785464105490"
                      }
                    }
                  },
                  "AUTHUSER-2": {
                    "M": {
                      "Name": {
                        "S": "Martha Rivera"
                      },
                      "PlasticCardNumber": {
                        "S": "4509056796535263"
                      }
                    }
                  }
                }
              }
            },
            {
              "PK": {
                "S": "ACCT#73572246"
              },
              "SK": {
                "S": "ACCT#73572246"
              },
              "AccountId": {
                "N": "73572246"
              },
              "PlasticCardNumber": {
                "S": "4079524883063080"
              },
              "FirstName": {
                "S": "Arnav"
              },
              "LastName": {
                "S": "Desai"
              },
              "Emailid": {
                "S": "arnav.desai@example.org"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "122 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "121 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#73572246"
              },
              "AuthUsers": {
                "M": {
                  "AUTHUSER-1": {
                    "M": {
                      "Name": {
                        "S": "Nikhil Jayashankar"
                      },
                      "PlasticCardNumber": {
                        "S": "4991947623580470"
                      }
                    }
                  },
                  "AUTHUSER-2": {
                    "M": {
                      "Name": {
                        "S": "Saanvi Sarkar"
                      },
                      "PlasticCardNumber": {
                        "S": "4321127171428841"
                      }
                    }
                  }
                }
              }
            },
            {
              "PK": {
                "S": "ACCT#82691500"
              },
              "SK": {
                "S": "ACCT#82691500"
              },
              "AccountId": {
                "N": "82691500"
              },
              "PlasticCardNumber": {
                "S": "9610432116466295"
              },
              "FirstName": {
                "S": "Alejandro"
              },
              "LastName": {
                "S": "Rosalez"
              },
              "Emailid": {
                "S": "alejandro.rosalez11@example.org"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "123 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "221 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#82691500"
              }
            },
            {
              "PK": {
                "S": "ACCT#53622839"
              },
              "SK": {
                "S": "ACCT#53622839"
              },
              "AccountId": {
                "N": "53622839"
              },
              "PlasticCardNumber": {
                "S": "4254427234262738"
              },
              "FirstName": {
                "S": "Jane"
              },
              "LastName": {
                "S": "Doe"
              },
              "Emailid": {
                "S": "jane2020@example.org"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "133 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "222 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#53622839"
              }
            },
            {
              "PK": {
                "S": "ACCT#49864709"
              },
              "SK": {
                "S": "ACCT#49864709"
              },
              "AccountId": {
                "N": "49864709"
              },
              "PlasticCardNumber": {
                "S": "7791356375391741"
              },
              "FirstName": {
                "S": "John"
              },
              "LastName": {
                "S": "Stiles"
              },
              "Emailid": {
                "S": "john.stiles@example.com"
              },
              "Addresses": {
                "M": {
                  "RESIDENCE": {
                    "M": {
                      "street": {
                        "S": "333 Any Street"
                      },
                      "city": {
                        "S": "Any Town"
                      },
                      "country": {
                        "S": "USA"
                      }
                    }
                  },
                  "BUSINESS": {
                    "M": {
                      "street": {
                        "S": "123 Main Street"
                      },
                      "city": {
                        "S": "Anytown"
                      },
                      "country": {
                        "S": "country"
                      }
                    }
                  }
                }
              },
              "AccountIndexId": {
                "S": "ACCT#49864709"
              }
            }
          ],
          "NonKeyAttributes": [
            "AccountId",
            "PlasticCardNumber",
            "FirstName",
            "MiddleName",
            "LastName",
            "Emailid",
            "Addresses",
            "AccountIndexId",
            "AuthUsers"
          ],
          "DataAccess": {
            "MySql": {}
          }
        },
        {
          "FacetName": "Offers",
          "KeyAttributeAlias": {
            "PartitionKeyAlias": "PK",
            "SortKeyAlias": "SK"
          },
          "TableData": [
            {
              "PK": {
                "S": "OFR#10001"
              },
              "SK": {
                "S": "OFR#10001"
              },
              "OfferId": {
                "N": "10001"
              },
              "OfferType": {
                "S": "BAX"
              },
              "OfferDescription": {
                "S": "Balance transfer with a 1% fee"
              },
              "OfferSubType": {
                "S": "BAL"
              },
              "OfferEffectiveDate": {
                "S": "2020-04-01"
              },
              "OfferExpiryDate": {
                "S": "2999-12-31"
              },
              "CreatedDate": {
                "S": "2020-03-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-03-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10001.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10002"
              },
              "SK": {
                "S": "OFR#10002"
              },
              "OfferId": {
                "N": "10002"
              },
              "OfferType": {
                "S": "BAX"
              },
              "OfferDescription": {
                "S": "Balance transfer with a 1.5% fee"
              },
              "OfferSubType": {
                "S": "BAL"
              },
              "OfferEffectiveDate": {
                "S": "2020-04-01"
              },
              "OfferExpiryDate": {
                "S": "2999-12-31"
              },
              "CreatedDate": {
                "S": "2020-03-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-03-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10002.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10010"
              },
              "SK": {
                "S": "OFR#10010"
              },
              "OfferId": {
                "N": "10010"
              },
              "OfferType": {
                "S": "CRL"
              },
              "OfferDescription": {
                "S": "Credit limit increase to 1500"
              },
              "OfferSubType": {
                "S": "CRL"
              },
              "OfferEffectiveDate": {
                "S": "2020-04-01"
              },
              "OfferExpiryDate": {
                "S": "2999-12-31"
              },
              "CreatedDate": {
                "S": "2020-03-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-03-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10010.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10011"
              },
              "SK": {
                "S": "OFR#10011"
              },
              "OfferId": {
                "N": "10011"
              },
              "OfferType": {
                "S": "CRL"
              },
              "OfferDescription": {
                "S": "Credit limit increase to 5000"
              },
              "OfferSubType": {
                "S": "CRL"
              },
              "OfferEffectiveDate": {
                "S": "2020-04-01"
              },
              "OfferExpiryDate": {
                "S": "2999-12-31"
              },
              "CreatedDate": {
                "S": "2020-03-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-03-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10011.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10012"
              },
              "SK": {
                "S": "OFR#10012"
              },
              "OfferId": {
                "N": "10012"
              },
              "OfferType": {
                "S": "CRL"
              },
              "OfferDescription": {
                "S": "Credit limit increase to 15000"
              },
              "OfferSubType": {
                "S": "CRL"
              },
              "OfferEffectiveDate": {
                "S": "2020-04-01"
              },
              "OfferExpiryDate": {
                "S": "2999-12-31"
              },
              "CreatedDate": {
                "S": "2020-03-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-03-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10015.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10020"
              },
              "SK": {
                "S": "OFR#10020"
              },
              "OfferId": {
                "N": "10020"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "OfferDescription": {
                "S": "Cash back 2% all categories"
              },
              "OfferSubType": {
                "S": "CASH"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Saanvi Sarkar"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10020.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10021"
              },
              "SK": {
                "S": "OFR#10021"
              },
              "OfferId": {
                "N": "10021"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "OfferDescription": {
                "S": "Cash back 3% all categories"
              },
              "OfferSubType": {
                "S": "CASH"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Saanvi Sarkar"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10021.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10022"
              },
              "SK": {
                "S": "OFR#10022"
              },
              "OfferId": {
                "N": "10022"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "OfferDescription": {
                "S": "Cash back 3.5% all categories"
              },
              "OfferSubType": {
                "S": "CASH"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Saanvi Sarkar"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10022.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10030"
              },
              "SK": {
                "S": "OFR#10030"
              },
              "OfferId": {
                "N": "10030"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "OfferDescription": {
                "S": "2 miles per dollar spent"
              },
              "OfferSubType": {
                "S": "MILES"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Saanvi Sarkar"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10030.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10031"
              },
              "SK": {
                "S": "OFR#10031"
              },
              "OfferId": {
                "N": "10031"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "OfferDescription": {
                "S": "5 miles per dollar spent"
              },
              "OfferSubType": {
                "S": "MILES"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Saanvi Sarkar"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10031.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10041"
              },
              "SK": {
                "S": "OFR#10041"
              },
              "OfferId": {
                "N": "10041"
              },
              "OfferType": {
                "S": "UPG"
              },
              "OfferDescription": {
                "S": "0% intro annual percent rate, 12.5% variable next year, 19.99% fixed thereafter"
              },
              "OfferSubType": {
                "S": "APR"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10041.jpeg"
              }
            },
            {
              "PK": {
                "S": "OFR#10003"
              },
              "SK": {
                "S": "OFR#10003"
              },
              "OfferId": {
                "N": "10003"
              },
              "OfferType": {
                "S": "BAX"
              },
              "OfferDescription": {
                "S": "Balance transfer with a 1% fee and 9.99% variable annual percent rate"
              },
              "OfferSubType": {
                "S": "BAR"
              },
              "OfferEffectiveDate": {
                "S": "2020-05-01"
              },
              "OfferExpiryDate": {
                "S": "2021-12-31"
              },
              "CreatedDate": {
                "S": "2020-04-01"
              },
              "CreatedBy": {
                "S": "Martha Rivera"
              },
              "LastModified": {
                "S": "2020-04-01"
              },
              "OfferUrl": {
                "S": "https://example.com/offers/10003.jpeg"
              }
            }
          ],
          "NonKeyAttributes": [
            "OfferId",
            "OfferType",
            "OfferDescription",
            "OfferSubType",
            "OfferEffectiveDate",
            "OfferExpiryDate",
            "CreatedDate",
            "CreatedBy",
            "LastModified",
            "OfferUrl"
          ],
          "DataAccess": {
            "MySql": {}
          }
        },
        {
          "FacetName": "AccountOffers",
          "KeyAttributeAlias": {
            "PartitionKeyAlias": "PK",
            "SortKeyAlias": "SK"
          },
          "TableData": [
            {
              "PK": {
                "S": "ACCT#76584123"
              },
              "SK": {
                "S": "OFR#10001"
              },
              "AccountId": {
                "N": "76584123"
              },
              "OfferId": {
                "N": "10001"
              },
              "OfferType": {
                "S": "BAX"
              },
              "AccountOfferStartDate": {
                "S": "2020-05-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-08-01"
              },
              "Status": {
                "S": "CREATED"
              },
              "StatusChangeDate": {
                "S": "2020-12-01"
              }
            },
            {
              "PK": {
                "S": "ACCT#76584123"
              },
              "SK": {
                "S": "OFR#10002"
              },
              "AccountId": {
                "N": "76584123"
              },
              "OfferId": {
                "N": "10002"
              },
              "OfferType": {
                "S": "BAX"
              },
              "AccountOfferStartDate": {
                "S": "2020-06-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-09-01"
              },
              "Status": {
                "S": "CREATED"
              },
              "StatusChangeDate": {
                "S": "2020-12-01"
              }
            },
            {
              "PK": {
                "S": "ACCT#11584123"
              },
              "SK": {
                "S": "OFR#10010"
              },
              "AccountId": {
                "N": "11584123"
              },
              "OfferId": {
                "N": "10010"
              },
              "OfferType": {
                "S": "CRL"
              },
              "AccountOfferStartDate": {
                "S": "2020-02-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-02-28"
              },
              "Status": {
                "S": "DECLINED"
              },
              "StatusChangeDate": {
                "S": "2020-04-20"
              },
              "GSI1SK": {
                "S": "DECLINED#CRL"
              }
            },
            {
              "PK": {
                "S": "ACCT#76584123"
              },
              "SK": {
                "S": "OFR#10010"
              },
              "AccountId": {
                "N": "76584123"
              },
              "OfferId": {
                "N": "10010"
              },
              "OfferType": {
                "S": "CRL"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "ACCEPTED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "ACCEPTED#CRL"
              }
            },
            {
              "PK": {
                "S": "ACCT#49864709"
              },
              "SK": {
                "S": "OFR#10003"
              },
              "AccountId": {
                "N": "49864709"
              },
              "OfferId": {
                "N": "10003"
              },
              "OfferType": {
                "S": "BAL"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "DECLINED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "DECLINED#BAL"
              }
            },
            {
              "PK": {
                "S": "ACCT#53622839"
              },
              "SK": {
                "S": "OFR#10011"
              },
              "AccountId": {
                "N": "53622839"
              },
              "OfferId": {
                "N": "10011"
              },
              "OfferType": {
                "S": "CRL"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "CREATED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              }
            },
            {
              "PK": {
                "S": "ACCT#53622839"
              },
              "SK": {
                "S": "OFR#10022"
              },
              "AccountId": {
                "N": "53622839"
              },
              "OfferId": {
                "N": "10022"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "CREATED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              }
            },
            {
              "PK": {
                "S": "ACCT#49864709"
              },
              "SK": {
                "S": "OFR#10021"
              },
              "AccountId": {
                "N": "49864709"
              },
              "OfferId": {
                "N": "10021"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "DECLINED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "DECLINED#PROMO"
              }
            },
            {
              "PK": {
                "S": "ACCT#82691500"
              },
              "SK": {
                "S": "OFR#10021"
              },
              "AccountId": {
                "N": "82691500"
              },
              "OfferId": {
                "N": "10021"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "ACCEPTED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "ACCEPTED#PROMO"
              }
            },
            {
              "PK": {
                "S": "ACCT#82691500"
              },
              "SK": {
                "S": "OFR#10030"
              },
              "AccountId": {
                "N": "82691500"
              },
              "OfferId": {
                "N": "10030"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "DECLINED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "DECLINED#PROMO"
              }
            },
            {
              "PK": {
                "S": "ACCT#73572246"
              },
              "SK": {
                "S": "OFR#10030"
              },
              "AccountId": {
                "N": "73572246"
              },
              "OfferId": {
                "N": "10030"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "ACCEPTED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "ACCEPTED#PROMO"
              }
            },
            {
              "PK": {
                "S": "ACCT#73572246"
              },
              "SK": {
                "S": "OFR#10041"
              },
              "AccountId": {
                "N": "73572246"
              },
              "OfferId": {
                "N": "10041"
              },
              "OfferType": {
                "S": "UPG"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "ACCEPTED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              },
              "GSI1SK": {
                "S": "ACCEPTED#UPG"
              }
            },
            {
              "PK": {
                "S": "ACCT#76584657"
              },
              "SK": {
                "S": "OFR#10022"
              },
              "AccountId": {
                "N": "76584657"
              },
              "OfferId": {
                "N": "10022"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "CREATED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              }
            },
            {
              "PK": {
                "S": "ACCT#82691500"
              },
              "SK": {
                "S": "OFR#10031"
              },
              "AccountId": {
                "N": "82691500"
              },
              "OfferId": {
                "N": "10031"
              },
              "OfferType": {
                "S": "PROMO"
              },
              "AccountOfferStartDate": {
                "S": "2020-03-01"
              },
              "AccountOfferEndDate": {
                "S": "2020-12-01"
              },
              "Status": {
                "S": "CREATED"
              },
              "StatusChangeDate": {
                "S": "2020-03-25"
              }
            }
          ],
          "NonKeyAttributes": [
            "AccountId",
            "OfferId",
            "OfferType",
            "AccountOfferStartDate",
            "AccountOfferEndDate",
            "Status",
            "StatusChangeDate",
            "GSI1SK"
          ],
          "DataAccess": {
            "MySql": {}
          }
        },
        {
          "FacetName": "OfferItems",
          "KeyAttributeAlias": {
            "PartitionKeyAlias": "PK",
            "SortKeyAlias": "SK"
          },
          "TableData": [
            {
              "PK": {
                "S": "OFR#10001"
              },
              "SK": {
                "S": "OFR#10001#ITEM#1"
              },
              "OfferId": {
                "N": "10001"
              },
              "BalanceTransferFeePct": {
                "N": "1"
              },
              "BalanceTransferLimit": {
                "N": "1000"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10002"
              },
              "SK": {
                "S": "OFR#10002#ITEM#1"
              },
              "OfferId": {
                "N": "10002"
              },
              "BalanceTransferFeePct": {
                "N": "1.5"
              },
              "BalanceTransferLimit": {
                "N": "2000"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10010"
              },
              "SK": {
                "S": "OFR#10010#ITEM#1"
              },
              "OfferId": {
                "N": "10010"
              },
              "CreditLimit": {
                "N": "1500"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10011"
              },
              "SK": {
                "S": "OFR#10011#ITEM#1"
              },
              "OfferId": {
                "N": "10011"
              },
              "CreditLimit": {
                "N": "5000"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10012"
              },
              "SK": {
                "S": "OFR#10012#ITEM#1"
              },
              "OfferId": {
                "N": "10012"
              },
              "CreditLimit": {
                "N": "15000"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10020"
              },
              "SK": {
                "S": "OFR#10020#ITEM#1"
              },
              "OfferId": {
                "N": "10020"
              },
              "CashBackPct": {
                "N": "2"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10021"
              },
              "SK": {
                "S": "OFR#10021#ITEM#1"
              },
              "OfferId": {
                "N": "10021"
              },
              "CashBackPct": {
                "N": "3"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10022"
              },
              "SK": {
                "S": "OFR#10022#ITEM#1"
              },
              "OfferId": {
                "N": "10022"
              },
              "CashBackPct": {
                "N": "3.5"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10030"
              },
              "SK": {
                "S": "OFR#10030#ITEM#1"
              },
              "OfferId": {
                "N": "10030"
              },
              "Miles": {
                "N": "2"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10031"
              },
              "SK": {
                "S": "OFR#10031#ITEM#1"
              },
              "OfferId": {
                "N": "10031"
              },
              "Miles": {
                "N": "5"
              },
              "OfferItemId": {
                "S": "2"
              }
            },
            {
              "PK": {
                "S": "OFR#10003"
              },
              "SK": {
                "S": "OFR#10003#ITEM#1"
              },
              "OfferId": {
                "N": "10003"
              },
              "BalanceTransferFeePct": {
                "N": "1"
              },
              "BalanceTransferLimit": {
                "N": "3000"
              },
              "OfferItemId": {
                "S": "1"
              }
            },
            {
              "PK": {
                "S": "OFR#10003"
              },
              "SK": {
                "S": "OFR#10003#ITEM#2"
              },
              "OfferId": {
                "N": "10003"
              },
              "OfferItemId": {
                "S": "2"
              },
              "AprType": {
                "S": "VAR"
              },
              "AprRate": {
                "N": "12.5"
              }
            },
            {
              "PK": {
                "S": "OFR#10041"
              },
              "SK": {
                "S": "OFR#10041#ITEM#1"
              },
              "OfferId": {
                "N": "10041"
              },
              "OfferItemId": {
                "S": "1"
              },
              "AprType": {
                "S": "INT"
              },
              "AprRate": {
                "N": "0"
              },
              "APRDurationInMonths": {
                "S": "12"
              }
            },
            {
              "PK": {
                "S": "OFR#10041"
              },
              "SK": {
                "S": "OFR#10041#ITEM#2"
              },
              "OfferId": {
                "N": "10041"
              },
              "OfferItemId": {
                "S": "2"
              },
              "AprType": {
                "S": "VAR"
              },
              "AprRate": {
                "N": "12.5"
              },
              "APRDurationInMonths": {
                "S": "12"
              }
            },
            {
              "PK": {
                "S": "OFR#10041"
              },
              "SK": {
                "S": "OFR#10041#ITEM#3"
              },
              "OfferId": {
                "N": "10041"
              },
              "OfferItemId": {
                "S": "3"
              },
              "AprType": {
                "S": "FIX"
              },
              "AprRate": {
                "N": "19.99"
              }
            }
          ],
          "NonKeyAttributes": [
            "OfferId",
            "CreditLimit",
            "BalanceTransferFeePct",
            "BalanceTransferLimit",
            "CashBackPct",
            "Miles",
            "OfferItemId",
            "AprType",
            "AprRate",
            "APRDurationInMonths"
          ],
          "DataAccess": {
            "MySql": {}
          }
        }
      ],
      "GlobalSecondaryIndexes": [
        {
          "IndexName": "AccountIndex",
          "KeyAttributes": {
            "PartitionKey": {
              "AttributeName": "AccountIndexId",
              "AttributeType": "S"
            }
          },
          "Projection": {
            "ProjectionType": "INCLUDE",
            "NonKeyAttributes": [
              "FirstName",
              "LastName",
              "MiddleName",
              "Emailid",
              "Addresses"
            ]
          }
        },
        {
          "IndexName": "GSI1",
          "KeyAttributes": {
            "PartitionKey": {
              "AttributeName": "PK",
              "AttributeType": "S"
            },
            "SortKey": {
              "AttributeName": "GSI1SK",
              "AttributeType": "S"
            }
          },
          "Projection": {
            "ProjectionType": "INCLUDE",
            "NonKeyAttributes": [
              "AccountId",
              "OfferId",
              "OfferType",
              "AccountOfferStartDate",
              "AccountOfferEndDate",
              "Status",
              "StatusChangeDate"
            ]
          }
        }
      ],
      "DataAccess": {
        "MySql": {}
      },
      "BillingMode": "PROVISIONED",
      "ProvisionedCapacitySettings": {
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        },
        "AutoScalingRead": {
          "ScalableTargetRequest": {
            "MinCapacity": 1,
            "MaxCapacity": 10,
            "ServiceRole": "AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
          },
          "ScalingPolicyConfiguration": {
            "TargetValue": 70
          }
        },
        "AutoScalingWrite": {
          "ScalableTargetRequest": {
            "MinCapacity": 1,
            "MaxCapacity": 10,
            "ServiceRole": "AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
          },
          "ScalingPolicyConfiguration": {
            "TargetValue": 70
          }
        }
      }
    }
  ]
}

base_model = 	{
	  "ModelName": "Credit Card Offers Data Model",
	  "ModelMetadata": {
	    "Author": "Amazon Web Services, Inc.",
	    "DateCreated": "May 1, 2020, 11:00 AM",
	    "DateLastModified": "May 17, 2021, 03:17 PM",
	    "Description": "This data model represents an Amazon DynamoDB model for credit card account offers that are part of a Credit Card Offers Application.\n\nA credit card provider designs offers over time, including balance transfers without fees, increased credit limits, lower interest rates, cash back, and airline miles. After a customer accepts or declines these offers, the respective offer status is updated accordingly.\n\nThe model’s data can be modeled in many ways. In this data model, we chose to use a single-table design and a prejoin access pattern for maintaining one-to-many relationships among entities such as Accounts, Offers, AccountOffers, and OfferItems. As a result, the retrieval of the data is near real time at scale. \n\nUnlike a relational database with a normalized schema with many entities and joins among them to fetch accounts and offers, this model’s key access patterns represent constant time data retrieval at scale.\n\nNote: for demonstration purpose, the attribute names have been kept descriptive and human readable. In real model, it is recommended to use shorter and less human readable attribute names to save space on disk and in every response that gets sent back.\n\nThe important access patterns facilitated by this data model are:\n\t* Retrieval of account records using AccountId, as facilitated by the main table\n        * Retrieval of all the accounts with few projected items, as facilitated by the secondary index AccountIndex\n\t* Retrieval of accounts and all the offer records associated with those accounts by using AccountId, as facilitated by the main table\n\t* Retrieval of accounts and specific offer records associated with those accounts by using AccountId and OfferId, as facilitated by the main table\n\t* Retrieval of all ACCEPTED/DECLINED offer records of specific OfferType associated with accounts using AccountId, OfferType, and Status, as facilitated by the secondary index GSI1\n\t* Retrieval of offers and associated offer item records using OfferId, as facilitated by the main table",
	    "Version": "3.0",
	    "AWSService": "Amazon DynamoDB"
	  },
	  "DataModel": [{
	    "TableName": "CreditCardOffers",
	    "KeyAttributes": {
	      "PartitionKey": {
	        "AttributeName": "PK",
	        "AttributeType": "S"
	      },
	      "SortKey": {
	        "AttributeName": "SK",
	        "AttributeType": "S"
	      }
	    },
	    "NonKeyAttributes": [
	      {
	        "AttributeName": "AccountId",
	        "AttributeType": "N"
	      }
	    ],
	    "TableFacets": [],
		"GlobalSecondaryIndexes": [],
		"DataAccess": {
	        "MySql": {}
	     },
      "BillingMode": "PROVISIONED",
      "ProvisionedCapacitySettings": {
        "ProvisionedThroughput": {
          "ReadCapacityUnits": 5,
          "WriteCapacityUnits": 5
        },
        "AutoScalingRead": {
          "ScalableTargetRequest": {
            "MinCapacity": 1,
            "MaxCapacity": 10,
            "ServiceRole": "AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
          },
          "ScalingPolicyConfiguration": {
            "TargetValue": 70
          }
        },
        "AutoScalingWrite": {
          "ScalableTargetRequest": {
            "MinCapacity": 1,
            "MaxCapacity": 10,
            "ServiceRole": "AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
          },
          "ScalingPolicyConfiguration": {
            "TargetValue": 70
          }
        }
      }
	 }]
	}

TableFacets = {
  "FacetName": "Accounts",
  "KeyAttributeAlias": {
    "PartitionKeyAlias": "PK",
    "SortKeyAlias": "SK"
  },
  "TableData": [
  ],
  "NonKeyAttributes": [
    "AccountId",
    "PlasticCardNumber",
    "FirstName",
    "MiddleName",
    "LastName",
    "Emailid",
    "Addresses",
    "AccountIndexId",
    "AuthUsers"
  ],
  "DataAccess": {
    "MySql": {}
  }
}

def download_db_csv(db):
	pass


def download_db_dict(db):
	""" Download the database in the format nested dict
		
		db

		REQUIRES:
			from copy import deepcopy
	"""
	scan = db.scan(confirm=True) #> List[Dict]
	output = {e[db.PK]: dict() for e in scan}
	for each in deepcopy(scan):
		PK = each.pop(db.PK, None)
		SK = each.pop(db.SK, None)
		output[PK][SK] = each
	return output #> Dict[Dict] -> {PK: {SK: {} }}

from pprint import pprint

def download_db_aws(db):
	""" Download the database in the format nested dict
		
		db

		EXAMPLE:
			>>> import dynamo;db = dynamo.DB('USER')
			>>> from download_as import download_db_aws
			>>> download_db_aws(db)

		REQUIRES:
			from copy import deepcopy
		

		Note: don't put SK and PK in 
	"""
  print("""AWS dynamodb and `nosql workbench` have compatibilty issues, 
    in dynamo db you can have a attr that is type string in one partition and type map in another partition.

    This is not allowed in `nosql workbench` and will lead to issues, where it can not load your model.

    The current work around it to code mappings to deserialized strings, for display purposes.

    Another issue is where No value is supplied for N (number) types aws codes with as "NULL": True, which creates two attr records leading to another error.
    """)
	model = deepcopy(base_model)
	table_facets = deepcopy(TableFacets)
	TableData = []
	TableDataAll = []
	AllNonKeyAttributes = []

	scan = db.scan(confirm=True) #> List[Dict]
	# output = {e[db.PK]: dict() for e in scan}
	for row in deepcopy(scan):
		NonKeyAttributes = []
		print(row)


		print("")
		# PK = each.pop(db.PK, None)
		# SK = each.pop(db.SK, None)

		for k,v in row.items():
			print(k)
			row[k] = serialize(v)

			data = {
			  "AttributeName": k,
			  "AttributeType": list(row[k].items())[0][0]
			}
			AllNonKeyAttributes.append(data)
			# NonKeyAttributes.append(data)


		# AllNonKeyAttributes = list(set(AllNonKeyAttributes + list(row.keys())))

		# print(type(row))
		# print(row)

		table_facets["FacetName"] = "One"
		# table_facets["NonKeyAttributes"] = NonKeyAttributes
		table_facets["NonKeyAttributes"] = list(set((row.keys())))
		table_facets["TableData"].append(row)
		TableData.append(table_facets)
		

		TableDataAll.append(row)

		
		# output[PK][SK] = row
	print("")
	print("..FINISHED..")
	print("")


	model["ModelName"] = "New Model"
	model["ModelMetadata"]["Author"] = "Mike"

	

	# model["DataModel"][0]["TableName"] = "Example111"
	# model["DataModel"][0]["NonKeyAttributes"] = list(set(AllNonKeyAttributes))
	# model["DataModel"][0]["TableFacets"] = TableData	





	# r_NonKeyAttributes = list(set(AllNonKeyAttributes))
	r_NonKeyAttributes = [dict(j) for j in {tuple(e.items()) for e in AllNonKeyAttributes}]
	print("", r_NonKeyAttributes)

	# [dict(j) for j in r_NonKeyAttributes]

	# r_NonKeyAttributes.remove("PK")
	# r_NonKeyAttributes.remove("SK")

	model["DataModel"][0]["TableName"] = "Example111"
	model["DataModel"][0]["NonKeyAttributes"] = r_NonKeyAttributes
	model["DataModel"][0]["TableFacets"] = []
	model["DataModel"][0]["TableData"] = TableDataAll
	

	import json
	return json.dumps(model)

	# NonKeyAttributes
      # {
      #   "AttributeName": "AccountId",
      #   "AttributeType": "N"
      # }
	# TableFacets

	# for k,v in row.items:
	# 	data = {
	# 	  "AttributeName": k,
	# 	  "AttributeType": v.items()[0]
	# 	}
	# 	AllNonKeyAttributes.append(data)
	# 	NonKeyAttributes.append(data)



	pprint({"TableData": TableData, "NonKeyAttributes": NonKeyAttributes})
	return {"TableData": TableData, "NonKeyAttributes": NonKeyAttributes}
	# return TableData #> Dict[Dict] -> {PK: {SK: {} }}



def download_db_simple(db):
	""" Download the database in the format dict

		db
		
		REQUIRES:
			from copy import deepcopy
	"""
	scan = db.scan(confirm=True) #> List[Dict]
	output = {}
	for each in deepcopy(scan):
		PK = each.pop(db.PK, None)
		SK = each.pop(db.SK, None)
		output[(PK,SK)] = each
	return output #> Dict -> {(PK, SK): {}}


# example scan
[{
		'updated_iso': '2021-09-27T22:56:27.347548',
		'userPreferences': {
			'language': 'zh',
			'sortDirection': 'descending',
			'sort': 'rating'
		},
		'updated': Decimal('1632736587'),
		'SK': 'CUST#321',
		'PK': '123',
		'email': 'zhang@example.net',
		'fullName': 'Zhang Wei'
	},
	{
		'updated_iso': '2021-09-27T22:56:27.531530',
		'updateDate': '2020-03-25T09:16:46-07:00',
		'createDate': '2020-03-25T09:16:46-07:00',
		'updated': Decimal('1632736587'),
		'SK': 'https://aws.amazon.com',
		'PK': '123',
		'description': 'Amazon Web Services',
		'folder': 'Tools',
		'url': 'https://aws.amazon.com',
		'title': 'AWS'
	},
	{
		'updated_iso': '2021-09-27T22:56:27.719783',
		'updateDate': '2020-03-25T09:16:43-07:00',
		'createDate': '2020-03-25T09:16:43-07:00',
		'updated': Decimal('1632736587'),
		'SK': 'https://docs.aws.amazon.com',
		'PK': '123',
		'description': 'Documentation',
		'folder': 'Docs',
		'url': 'https://docs.aws.amazon.com',
		'title': 'AWS Docs'
	},
	{
		'updated_iso': '2021-09-27T22:56:27.907174',
		'userPreferences': {
			'language': 'zh',
			'sortDirection': 'descending',
			'sort': 'rating'
		},
		'updated': Decimal('1632736587'),
		'SK': 'CUST#321',
		'PK': '321',
		'email': 'zhang@example.net',
		'fullName': 'Zhang Wei'
	},
	{
		'updated_iso': '2021-09-27T22:56:28.088424',
		'updateDate': '2020-03-25T09:16:46-07:00',
		'createDate': '2020-03-25T09:16:46-07:00',
		'updated': Decimal('1632736588'),
		'SK': 'https://aws.amazon.com',
		'PK': '321',
		'description': 'Amazon Web Services',
		'folder': 'Tools',
		'url': 'https://aws.amazon.com',
		'title': 'AWS'
	},
	{
		'updated_iso': '2021-09-27T22:56:28.272035',
		'updateDate': '2020-03-25T09:16:43-07:00',
		'createDate': '2020-03-25T09:16:43-07:00',
		'updated': Decimal('1632736588'),
		'SK': 'https://docs.aws.amazon.com',
		'PK': '321',
		'description': 'Documentation',
		'folder': 'Docs',
		'url': 'https://docs.aws.amazon.com',
		'title': 'AWS Docs'
	}
]



# download_db_dict()
{
	'123':
	{
		'CUST#123':
		{
			'updated_iso': '2021-09-27T23:20:47.901270',
			'userPreferences':
			{
				'language': 'en',
				'sortDirection': 'ascending',
				'sort': 'date'
			},
			'updated': Decimal('1632738047'),
			'email': 'shirley@example.net',
			'fullName': 'Shirley Rodriguez'
		},
		'https://aws.amazon.com':
		{
			'updated_iso': '2021-09-27T23:20:48.664226',
			'updateDate': '2020-03-25T09:16:46-07:00',
			'createDate': '2020-03-25T09:16:46-07:00',
			'updated': Decimal('1632738048'),
			'description': 'Amazon Web Services',
			'folder': 'Cloud',
			'url': 'https://aws.amazon.com',
			'title': 'AWS'
		},
		'https://console.aws.amazon.com':
		{
			'updated_iso': '2021-09-27T23:20:48.850602',
			'updateDate': '2020-03-25T09:16:43-07:00',
			'createDate': '2020-03-25T09:16:43-07:00',
			'updated': Decimal('1632738048'),
			'description': 'Web console',
			'folder': 'Cloud',
			'url': 'https://console.aws.amazon.com',
			'title': 'AWS Console'
		}
	},
	'321':
	{
		'CUST#321':
		{
			'updated_iso': '2021-09-27T23:20:49.040283',
			'userPreferences':
			{
				'language': 'zh',
				'sortDirection': 'descending',
				'sort': 'rating'
			},
			'updated': Decimal('1632738049'),
			'email': 'zhang@example.net',
			'fullName': 'Zhang Wei'
		},
		'https://aws.amazon.com':
		{
			'updated_iso': '2021-09-27T23:20:49.223435',
			'updateDate': '2020-03-25T09:16:46-07:00',
			'createDate': '2020-03-25T09:16:46-07:00',
			'updated': Decimal('1632738049'),
			'description': 'Amazon Web Services',
			'folder': 'Tools',
			'url': 'https://aws.amazon.com',
			'title': 'AWS'
		},
		'https://docs.aws.amazon.com':
		{
			'updated_iso': '2021-09-27T23:20:49.410889',
			'updateDate': '2020-03-25T09:16:43-07:00',
			'createDate': '2020-03-25T09:16:43-07:00',
			'updated': Decimal('1632738049'),
			'description': 'Documentation',
			'folder': 'Docs',
			'url': 'https://docs.aws.amazon.com',
			'title': 'AWS Docs'
		}
	}
}


"""
>>> download_db_simple()
Warning this function is returning a full database record.
"""
{
    ('123', 'CUST#123'): {
        'updated_iso': '2021-09-27T23:20:47.901270',
        'userPreferences':
        {
            'language': 'en',
            'sortDirection': 'ascending',
            'sort': 'date'
        },
        'updated': Decimal('1632738047'),
        'email': 'shirley@example.net',
        'fullName': 'Shirley Rodriguez'
    },
    ('123', 'https://aws.amazon.com'): {
        'updated_iso': '2021-09-27T23:20:48.664226',
        'updateDate': '2020-03-25T09:16:46-07:00',
        'createDate': '2020-03-25T09:16:46-07:00',
        'updated': Decimal('1632738048'),
        'description': 'Amazon Web Services',
        'folder': 'Cloud',
        'url': 'https://aws.amazon.com',
        'title': 'AWS'
    },
    ('123', 'https://console.aws.amazon.com'): {
        'updated_iso': '2021-09-27T23:20:48.850602',
        'updateDate': '2020-03-25T09:16:43-07:00',
        'createDate': '2020-03-25T09:16:43-07:00',
        'updated': Decimal('1632738048'),
        'description': 'Web console',
        'folder': 'Cloud',
        'url': 'https://console.aws.amazon.com',
        'title': 'AWS Console'
    }, 
    ('321', 'CUST#321'): {
        'updated_iso': '2021-09-27T23:20:49.040283',
        'userPreferences':
        {
            'language': 'zh',
            'sortDirection': 'descending',
            'sort': 'rating'
        },
        'updated': Decimal('1632738049'),
        'email': 'zhang@example.net',
        'fullName': 'Zhang Wei'
    }, 
    ('321', 'https://aws.amazon.com'): {
        'updated_iso': '2021-09-27T23:20:49.223435',
        'updateDate': '2020-03-25T09:16:46-07:00',
        'createDate': '2020-03-25T09:16:46-07:00',
        'updated': Decimal('1632738049'),
        'description': 'Amazon Web Services',
        'folder': 'Tools',
        'url': 'https://aws.amazon.com',
        'title': 'AWS'
    }, 
    ('321', 'https://docs.aws.amazon.com'): {
        'updated_iso': '2021-09-27T23:20:49.410889',
        'updateDate': '2020-03-25T09:16:43-07:00',
        'createDate': '2020-03-25T09:16:43-07:00',
        'updated': Decimal('1632738049'),
        'description': 'Documentation',
        'folder': 'Docs',
        'url': 'https://docs.aws.amazon.com',
        'title': 'AWS Docs'
    }
}
