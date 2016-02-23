import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from collections import defaultdict
#assume mongod running

#correct?
client = MongoClient('mongodb://localhost')
db = client['rpresults']


##basic no Nesting
# why raceid is string?

#collections horses, jockeys, races, results, trainers, venues

def get_race_with_results(raceid):
    race = db.races.find_one({'raceid': raceid})
    results = db.results.find({'raceid': raceid}).sort("-SP")
    # print race['venue']
    for ru in results:
    #from results get horse, trainer, jockey
        h = db.horse.find_one({'horseid': ru['horseid']})
    #nextrace, #previousraces
        print "-----------------"
        print h, ru



def get_all_previous_comments_horse(horseid):
    #get all results with this horse id
    results = db.results.find({'horseid': horseid})
    # comments = results['raceComments']
    # currentowner
    s = defaultdict(dict)
    for ru in results:
        ts = db.trainers.find({'trainerid': ru['trainerid']})
        for t in ts:
            print t['trainername']
        # print ru['trainer']
        # print s.keys()
    # print(dumps(results))
    # for ru in results:
    #     print tojson(ru)
        # print ru['previousraces']
        # print ru['previousraces'].values()[i]['racecomment']

        # print prev_races['racecomment']

get_all_previous_comments_horse("876846")
# print(get_race_with_results("615704"))
