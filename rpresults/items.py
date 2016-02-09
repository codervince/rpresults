# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VenueItem(scrapy.Item):
    racecourseid= scrapy.Field()
    racecoursename= scrapy.Field()
    racecoursedir= scrapy.Field()
    racecourseshape= scrapy.Field()
    racecoursefeature= scrapy.Field()
    racecoursespeed= scrapy.Field()

class HorseItem(scrapy.Item):
    horsename= scrapy.Field()
    breeder = scrapy.Field()
    horseid = scrapy.Field()
    sex= scrapy.Field()
    sire= scrapy.Field()
    dam= scrapy.Field()
    dob= scrapy.Field()
    color= scrapy.Field()
    owners= scrapy.Field()

class JockeyItem(scrapy.Item):
    jockeyname = scrapy.Field()
    jockeyid = scrapy.Field()

class TrainerItem(scrapy.Item):
    trainername = scrapy.Field()
    trainerid = scrapy.Field()

class RaceItem(scrapy.Item):
    venue = scrapy.Field()
    raceid = scrapy.Field()
    raceurl = scrapy.Field()
    racedate= scrapy.Field()
    racename= scrapy.Field()
    racecourse= scrapy.Field()
    raceclass= scrapy.Field()
    racetime = scrapy.Field()
    racetype = scrapy.Field()
    raceclass = scrapy.Field()
    prizemoneys= scrapy.Field()
    distance= scrapy.Field()
    going= scrapy.Field()
    raceratingspan= scrapy.Field()
    agerestriction= scrapy.Field()
    norunners= scrapy.Field()
    paceinfo= scrapy.Field()

class LTOItem(scrapy.Item):
    raceid = scrapy.Field()
    racedate= scrapy.Field()

class NTOItem(scrapy.Item):

    raceid = scrapy.Field()
    racedate= scrapy.Field()


class ResultsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    race = scrapy.Field()
    raceid= scrapy.Field()

    horse = scrapy.Field()
    horsename = scrapy.Field()
    horseid = scrapy.Field()

    jockey = scrapy.Field()
    jockeyid = scrapy.Field()

    trainer = scrapy.Field()
    trainerid = scrapy.Field()


    pos= scrapy.Field()
    lbw= scrapy.Field()
    sp= scrapy.Field()
    draw = scrapy.Field()
    raceComments= scrapy.Field()

    tippedby = scrapy.Field()
    l1race = scrapy.Field()
    l1raceid = scrapy.Field()

    n1raceid = scrapy.Field()
    n1race = scrapy.Field()
