#fix up fields

TODOs  

######### MONGO DB TASK

1.  Filter out AUS NZ SIN? meetings !!
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

#####################


dir:
cd /Users/vmac/SCRAPY16/rpresults/rpresults
scrapy crawl rpresults -a filename=inputdates_test.txt


FIELDS NEEDED

classchangel1
appallowance
