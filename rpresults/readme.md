#fix up fields

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
