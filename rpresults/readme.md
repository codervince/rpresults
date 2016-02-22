#fix up fields

errors

venueid
dates to date objects

#TODOs
racetime to time timezone

add dates to previous racedates do race like objects in dictionary




'raceurl': u'http://www.racingpost.com/horses/result_home.sd?popup=yes&r_date=2015-01-01&race_id=617100',
'season': u'Winter',
'specialrace': u'False',
'winninghorse': u'833851',
'winningprize': u'50732.98'},
'raceid': u'617100',
'sp': u'14.0',
'trainer': {'trainerid': u'23854', 'trainername': u'Grant Williams'},
'trainerid': u'23854',
'winoddsrank': u'4'}
Traceback (most recent call last):
 File "/Users/vmac/anaconda3/envs/pyscrapy/lib/python2.7/site-packages/twisted/internet/defer.py", line 588, in _runCallbacks
   current.result = callback(current.result, *args, **kw)
 File "/Users/vmac/SCRAPY16/rpresults/rpresults/pipelines.py", line 81, in process_item
   {'venueid': race_venue['venueid']},
 File "/Users/vmac/anaconda3/envs/pyscrapy/lib/python2.7/site-packages/scrapy/item.py", line 56, in __getitem__
   return self._values[key]
KeyError: 'venueid'



TODOs  



######### MONGO DB TASK

1.  Filter out AUS NZ SIN? meetings !!!

2.  Upsert to Mongodb
    database rpost
    collections:  (id unique key)
    - races
    - results
    - venues
    - horses
    - trainers
    - jockeys
    - LTOS (race)
    - NTOS (race)

Check for duplicates/upsert
Nesting in MongoDB as per item (or using internal object id)

{
  "_id" : ObjectId("5126bbf64aed4daf9e2ab771"),
  // .. application fields
  "creator" : {
                  "$ref" : "creators",
                  "$id" : ObjectId("5126bc054aed4daf9e2ab772"),
                  "$db" : "users"
               }
}

#####################


dir:
cd /Users/vmac/SCRAPY16/rpresults/rpresults
scrapy crawl rpresults -a filename=inputdates_test.txt


FIELDS NEEDED

classchangel1
appallowance
