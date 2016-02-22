# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#container class
class RacedayItem(scrapy.Item):
    nomeets = scrapy.Field()
    todaysdate = scrapy.Field()
    meets = scrapy.Field()

class VenueItem(scrapy.Item):
    venueid= scrapy.Field()
    name= scrapy.Field()
    code= scrapy.Field()
    direction= scrapy.Field()
    shape= scrapy.Field()
    feature= scrapy.Field()
    speed= scrapy.Field()
    grade = scrapy.Field()

class HorseItem(scrapy.Item):
    horsename= scrapy.Field()
    horseid= scrapy.Field()
    horseurl= scrapy.Field()
    breeder = scrapy.Field()
    horseid = scrapy.Field()
    sex= scrapy.Field()
    sire= scrapy.Field()
    dam= scrapy.Field()
    dob= scrapy.Field()
    color= scrapy.Field()
    owners= scrapy.Field()
    previousraces = scrapy.Field()

class JockeyItem(scrapy.Item):
    jockeyname = scrapy.Field()
    jockeyid = scrapy.Field()

class OwnerItem(scrapy.Item):
    ownername = scrapy.Field()

class TrainerItem(scrapy.Item):
    trainername = scrapy.Field()
    trainerid = scrapy.Field()

class RaceItem(scrapy.Item):
    venue = scrapy.Field()
    venueid = scrapy.Field()

    raceid = scrapy.Field()
    raceurl = scrapy.Field()
    racedate= scrapy.Field()
    season= scrapy.Field()
    racename= scrapy.Field()
    isfemalerace= scrapy.Field()
    isclaiming= scrapy.Field()
    isselling= scrapy.Field()
    isclassified= scrapy.Field()
    specialrace = scrapy.Field()

    raceclass= scrapy.Field()
    racetime = scrapy.Field()
    racetype = scrapy.Field()

    prizemoneys= scrapy.Field()
    distance= scrapy.Field()
    going= scrapy.Field()
    raceratingspan= scrapy.Field()
    agerestriction= scrapy.Field()
    norunners= scrapy.Field()
    paceinfo= scrapy.Field()
    winninghorse = scrapy.Field()
    winningprize = scrapy.Field()

#which is a race
class LTOItem(scrapy.Item):
    raceid = scrapy.Field()
    racedate= scrapy.Field()
#which is a race
class NTOItem(scrapy.Item):

    raceid = scrapy.Field()
    racedate= scrapy.Field()


class ResultsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # raceid, horseid is index

    race = scrapy.Field()
    raceid= scrapy.Field()


    horse = scrapy.Field()

    horsename = scrapy.Field()
    horseid = scrapy.Field()

    jockey = scrapy.Field()
    jockeyid = scrapy.Field()

    trainer = scrapy.Field()
    trainerid = scrapy.Field()
    allowance = scrapy.Field()

    FINALPOS= scrapy.Field()
    horseprize = scrapy.Field()
    lbw= scrapy.Field()
    SP= scrapy.Field()
    draw = scrapy.Field()
    winodds = scrapy.Field()
    winoddsrank = scrapy.Field()
    raceComments= scrapy.Field()

    tippedby = scrapy.Field()
    isFROY= scrapy.Field()
    previousraces = scrapy.Field()
    prevrace = scrapy.Field()
    nextrace = scrapy.Field()
    l1pos = scrapy.Field()
    l1racecoursecode= scrapy.Field()
    trainerchangel1= scrapy.Field()

    isMaiden = scrapy.Field()
    previousstarts = scrapy.Field()

    currentowner= scrapy.Field()
    allowners = scrapy.Field()
    ownertrainer = scrapy.Field()
