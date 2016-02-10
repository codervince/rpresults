# import to mongo raceceoursestats
import pymongo
from pymongo import MongoClient

def dovenues(db):
    #read from CSV
    venues = db.venues
    #create unique index
    result1 = venues.create_index([('venueid', pymongo.ASCENDING)],unique=True)
    print(result1)
    #EXAMPLE 2
    new_venues = [{
    'venueid': 3,
    'name': 'AYR',
    'code': 'Ayr',
    'direction': 'left',
    'shape': 'oval',
    'feature': None,
    'speed': 'galloping',
    'straight': 6.0,
    'grade': 1,
    'location': 'Scotland',
    'postcode': 'KA8 OJE'
    },
    {
    'venueid': 37,
    'name': 'NEWCASTLE',
    'code': 'Ncs',
    'direction': 'left',
    'shape': 'triangle',
    'feature': 'flat',
    'speed': 'galloping',
    'straight': 8.0,
    'grade': 4,
    'location': 'North',
    'postcode': 'NE3 5HP'
    },
    {
    'venueid': 16,
    'name': 'MUSSELBURGH',
    'code': 'Mus',
    'direction': 'right',
    'shape': 'oval',
    'feature': 'flat',
    'speed': 'stiff',
    'straight': 5.0,
    'grade': 3,
    'location': 'Scotland',
    'postcode': 'EH21 7RG'
    }]
    result = venues.insert_many(new_venues)
    return result.inserted_ids

client = MongoClient()
client = MongoClient('mongodb://localhost:27017/')
db = client.rp_database
venues = db.venues
result1 = venues.create_index([('venueid', pymongo.ASCENDING)],unique=True)
print(result1)
print(dovenues(db))
for v in db.venues.find():
    v
