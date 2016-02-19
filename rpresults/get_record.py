# -*- coding: utf-8 -*-
import pymongo
from settings import MONGO_DBNAME

raceid = "616064"
horseid = "838250"

mongo = pymongo.MongoClient()
db = mongo[MONGO_DBNAME]

result = db.results.find_one({'raceid': raceid, 'horseid': horseid})

if result is None:
    print 'record not found'
else:
    trainer = db.trainers.find_one({'trainerid': result['trainerid']})
    jockey = db.jockeys.find_one({'jockeyid': result['jockeyid']})

    race = db.races.find_one({'raceid': result['raceid']})
    venue = db.venues.find_one({'venueid': race['venueid']})

    horse = db.horses.find_one({'horseid': result['horseid']})

    print 'result', result, '\n'
    print 'trainer', trainer, '\n'
    print 'jockey', jockey, '\n'
    print 'race', race, '\n'
    print 'venue', venue, '\n'
    print 'horse', horse
