import scrapy
import re
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Join, MapCompose, Identity
from scrapy.http import Request
from scrapy import log
import decimal
from .. import items
from rpresults.items import ResultsItem,HorseItem, JockeyItem, TrainerItem, LTOItem, NTOItem, VenueItem, RaceItem
from datetime import datetime
import pprint
import logging
from time import sleep
from fractions import Fraction
import unicodedata
from collections import defaultdict
# import numpy


dir_pat = re.compile("^.*(left|right)-handed.*")
rcspeed_pat = re.compile("^.*(galloping|stiff|tight).*")
rcfeature_pat = re.compile("^.*(undulating|uphill|flat).*")
rcshape_pat = re.compile("^.*(circle|horseshoe|oval|pear|triangle).*")
dgr_pat = re.compile(r'^([0-9.]{1,4})(\w+)')
gearl1_pat = re.compile("(\D*)\d{1,4}/\d{1,2}")
spl1_pat = re.compile("\D*(\d{1,4}/\d{1,2})")
sp_pat = re.compile("\D*(\d{1,4}/\d{1,2})[FCJ]{0,1}")
# (USA) 27/10F
raceidpat = re.compile(r'.*race_id=(\d+).*')

# patterns for horse, trainer, jockey,race, course id
raceid_pat = re.compile(r'.*race_id=(\d+).*')
horseid_pat = re.compile(r'.*horse_id=(\d+).*')
trainerid_pat= re.compile(r'.*trainer_id=(\d+).*')
jockeyid_pat= re.compile(r'.*jockey_id=(\d+).*')
racecourseid_pat = re.compile(r'.*crs_id=(\d+).*')
ownerid_pat = re.compile(r'.*owner_id=(\d+).*')

#u'Trentham (NZ) Result 17 Jan 2015'
nzaus_pat = re.compile("\D*\s\((NZ|AUS)\)\sResult.*")
badracecoursename_pat = re.compile(".*\((\D+)\)\sResult.*")
racecoursename_pat = re.compile("(\D*)\sResult.*")


def horselengthprocessor(value):
    #covers '' and '-'

    if '---' in value:
        return None
    elif value == '-':
        #winner
        return 0.0
    elif "-" in value and len(value) > 1:
        return float(Fraction(value.split('-')[0]) + Fraction(value.split('-')[1]))
    elif value == 'N':
        return 0.3
    elif value == 'SH':
        return 0.1
    elif value == 'HD':
        return 0.2
    elif value == 'SN':
        return 0.25
    #nose?
    elif value == 'NOSE':
        return 0.05
    elif '/' in value:
         return float(Fraction(value))
    elif value.isdigit():
        return try_float(value)
    else:
        return None


def parse_mixed_fraction(s):
    if s.isdigit():
        return float(s)
    elif len(s) == 1:
        return unicodedata.numeric(s[-1])
    else:
        return float(s[:-1]) + unicodedata.numeric(s[-1])

def sanitizelbw(lbw):
    if "L" not in lbw:
        '''suspect lbw'''
        return None
    lbw = lbw.replace("L", "")
    return parse_mixed_fraction(lbw)

#order is gear, SP
def parseL1gearSP(L1gearSP):
    if " " not in L1gearSP:
        return (None, None)
    elif len(L1gearSP.split(" ")) >1:
        return L1gearSP.split(" ")
    else:
        return (None, L1gearSP.split(" ")[0])

def distanetofurlongs(imperialdistance):
    pass

def isFavorite(winodds):
    if winodds is None:
        return None
    return "F" or "J" or "C" in winodds

def decimalizeodds(winodds):
    '''edge cases 9/4F EvensF '''
    if winodds is None:
        return None
    elif "Evens" in winodds:
        return 2.0
    else:
        #remove non digit chars not /
        winodds = winodds.replace("F", "").replace("J", "").replace("C", "")
        num, denom = winodds.split("/")
        dec = Fraction(int(num), int(denom)) + Fraction(1,1)
        return float(dec)

def try_float(value):
    try:
        return float(value)
    except:
        return 0

def isbeatenfavorite(winodds, place):
    return isFavorite(winodds) and place ==1

#imperialtofurlongs
def imperialtofurlongs(idist):
    '''ex 2m2f50y'''
    miles = 0
    furlongs = 0
    yards = 0
    if "f" in idist and "m" in idist:
        miles, furlongs = try_int(idist.split("m")[0]), try_int(idist.split("f")[0].split("m")[1])
    if "f" in idist and "m" not in idist:
        furlongs = try_int(idist.split("f")[0])
    return miles*8 + furlongs

def imperialweighttokg(imperialweight):
    '''stone ounces '''
    if "-" not in imperialweight or imperialweight is None:
        return None
    else:
        stones, pounds = imperialweight.split("-")
        return round( ((int(stones)*14)+int(pounds))/2.20462262, 0)



'''2m2f50y'''
def getdistance(distancegoing):
    '''2 cases: case1: has dot then decimal'''
    res = ""
    if '.' in distancegoing:
        d1 = ''.join( ''.join([ i for i in distancegoing.split(".")[0]if i.isdigit() ])   )
        d2 = ''.join( ''.join([ i for i in distancegoing.split(".")[1]if i.isdigit() ])   )
        res = d1 + '.' + d2
    else:
        res =''.join( ''.join([ i for i in distancegoing if i.isdigit() ])   )
    return res


def tidytomoney(moneyvalue):
    from decimal import Decimal
    #replace non money chars
    if " " in moneyvalue:
        moneyvalue = moneyvalue.split(" ")[0]
    # ''.join( ''.join([ i for i in L1distgoing if not i.isdigit() ]))
    newmoney = float(moneyvalue.replace(",", ""))
    return decimal.Decimal(newmoney)


def tf(values, encoding="utf-8"):
    value = ""
    for v in values:
        if v is not None and v != "":
            value = v
            break
    return value.encode(encoding).strip()



def clean_lbwresult(s):
    if s is None:
        return None
    if s == u' ':
        return '0'
    s= s.strip()
    s= s.replace(u'\xbe', u'.75').replace(u'\xbd', u'.5').replace(u'\xbc', u'.25')
    s = s.replace(u'1\xbd', u'1.5')
    s = s.replace('nse', '0.01').replace('shd', '0.3').replace('nk', '0.25').replace('hd', '0.6').replace('snk', '0.05')
    return s

def removeunichars(value):
    return value.encode('ascii', 'ignore')

def cleandamsire(damsire):
    #count number of ( if 2 remove outer
    return damsire[1:-1]

def try_int(value):
    try:
        return int(value)
    except:
        return 0

def today():
    return datetime.today()

todaysdate = datetime.today()
todaysdatestr = datetime.today().strftime("%Y-%m-%d")

class LTOItemLoader(ItemLoader):
    default_item_class = HorseItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class NTOItemLoader(ItemLoader):
    default_item_class = HorseItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class VenueItemLoader(ItemLoader):
    default_item_class = HorseItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class JockeyItemLoader(ItemLoader):
    default_item_class = JockeyItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class TrainerItemLoader(ItemLoader):
    default_item_class = TrainerItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class HorseItemLoader(ItemLoader):
    default_item_class = HorseItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)

class RaceItemLoader(ItemLoader):
    default_item_class = RaceItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)


# from rpost.items import RpostResultsItem
class ResultsItemLoader(ItemLoader):
    default_item_class = ResultsItem
    default_output_processor = Compose(TakeFirst(), unicode, unicode.strip)
    pm1_out = Compose(default_output_processor, removeunichars, tidytomoney)
    pm2_out = Compose(default_output_processor, removeunichars, tidytomoney)
    pm3_out = Compose(default_output_processor, removeunichars, tidytomoney)
    pm4_out = Compose(default_output_processor, removeunichars, tidytomoney)
    pm5_out = Compose(default_output_processor, removeunichars, tidytomoney)
    prizemoney_out = Compose(default_output_processor, removeunichars, tidytomoney)
    racename_out = Compose(default_output_processor, removeunichars)
    gear_out = Compose(default_output_processor, removeunichars)
    OR_out = Compose(default_output_processor, removeunichars)
    TS_out = Compose(default_output_processor, removeunichars)
    RPR_out = Compose(default_output_processor, removeunichars)
    damsire_out = Compose(default_output_processor, removeunichars, cleandamsire)
    jockeyname_out = Compose(default_output_processor, removeunichars)
    trainername_out = Compose(default_output_processor, removeunichars)
    sire_out = Compose(default_output_processor, removeunichars)
    dam_out = Compose(default_output_processor, removeunichars)
    horsename_out = Compose(default_output_processor, removeunichars)
    prizemoney_in = Compose(default_output_processor, removeunichars,tidytomoney)
    L1racedate = Compose(default_output_processor, removeunichars)
    L2racedate = Compose(default_output_processor, removeunichars)
    L3racedate = Compose(default_output_processor, removeunichars)
    L4racedate = Compose(default_output_processor, removeunichars)
    L5racedate = Compose(default_output_processor, removeunichars)
    L6racedate = Compose(default_output_processor, removeunichars)
    L1comment_out = Compose(default_output_processor, removeunichars)
    L2comment_out = Compose(default_output_processor, removeunichars)
    L3comment_out = Compose(default_output_processor, removeunichars)
    L4comment_out = Compose(default_output_processor, removeunichars)
    L5comment_out = Compose(default_output_processor, removeunichars)
    L6comment_out = Compose(default_output_processor, removeunichars)
    currentodds_out = Compose(default_output_processor, decimalizeodds)
    horse_out = Identity()
    horse_in = Identity()


class RpostSpider(scrapy.Spider):
    name = "rpresults"
    allowed_domains = ["www.racingpost.com"]
    start_url = "http://www.racingpost.com/horses2/results/home.sd?r_date=%s" #2015-03-01 %y-%m-%d
    start_urls = []

        # "http://www.racingpost.com/horses/result_home.sd?race_id=618500&r_date=2015-02-27&popup=yes#results_top_tabs=re_&results_bottom_tabs=ANALYSIS"


    #rules horses http://www.racingpost.com/horses/horse_home.sd?horse_id=871316
    def __init__(self, date=None, filename=None):
        self.forbiddencountries = ['NZ', 'AUS']
        self.AUScourseids = [980,1022,629,311,821,517,480,471]
        self.todaysvenues = {}
        self.racedate = datetime.utcnow().date()
        if filename:
            with open(filename, 'r') as f:
                self.start_urls = [ self.start_url % (x.strip()) for x in f.readlines()]
        if filename is None:
            raise ValueError("Invalid spider parameters")
        # self.racedate = date
        # http://www.racingpost.com/horses2/cards/home.sd?r_date=2015-03-03

    # def start_requests(self):
    #     return [Request(self.start_url % (self.racedate))]


    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        if "No race meeting" in response.body:
            log.msg("Results page not ready, waiting 2 secs...", logLevel=log.INFO)
            sleep(2)
            yield Request(response.url, dont_filter=True)
        else:
            #raceday item? u'Trentham (NZ) Result 17 Jan 2015'
            title = response.xpath('//title').extract()[0]
            todayscourses = response.xpath("//h3//a[contains(@title, 'Course')]//@href").extract()
            # l.add_value('rpraceid',  re.match(r'.*race_id=(\d+).*', response.url).group(1))
            todaysnames = response.xpath("//h3//a[contains(@title, 'Course')]//text()").extract()
            todaysdate = response.url.split("=")[1]
            print todaysdate
            self.racedate = datetime.strptime(todaysdate, '%Y-%m-%d').date() #2016-02-06
            crsid = None
            for n,l in zip(todaysnames, todayscourses):
                print("n,l:\t", n, l)
                if re.match(racecourseid_pat, l):
                    crsid = re.match(racecourseid_pat, l).group(1)
                    # print("crsid:\t", crsid)
                    if n == 'SANDOWN (AUS) (AUS)':
                        n = 'SANDOWN (AUS)'
                    rc = n.upper().strip()
                self.todaysvenues[rc] = crsid
                # SANDOWN (AUS)
            if crsid in self.AUScourseids:
                yield Request(response.url, dont_filter=True)
            else:
                for link in LinkExtractor(restrict_xpaths="//a[contains(@title,'View full result')]",).extract_links(response)[:-1]:
                    # yield Request(link.url)
                    yield Request(link.url, callback=self.parse_race)


    def parse_race(self, response):

            # http://www.racingpost.com/horses/result_home.sd?race_id=642432&amp;r_date=2016-02-07#results_top_tabs=re_&results_bottom_tabs=ANALYSIS
            table_data = list()

            #FULL RESULTS PAGES
            # Results From The 2.10 Race At Doncaster | 27 February 2015 | Racing Post</title>'
            raceid = re.match(raceid_pat, response.url).group(1)
            racetitle = " ".join(response.xpath("//div[@class='leftColBig']/h1/text()").extract()).strip()
            racecoursename = None
            racecourseid = None
            if re.match(racecoursename_pat, racetitle):
                racecoursename = re.match(racecoursename_pat, racetitle).group(1)
                racecourseid = self.todaysvenues[racecoursename.upper().strip()]

            racetime = " ".join(response.xpath("//span[@class='timeNavigation']/text()").extract()).strip()
            racename = " ".join(response.xpath("//h3[@class='clearfix']/text()").extract()).strip()
            racedetails_ = " ".join(response.xpath("//div[@class='leftColBig']/ul/li[1]/text()").extract())
            #class rating agegroup distance going
            prizemoneys_ = " ".join(response.xpath("//div[@class='leftColBig']/ul/li[2]/text()").extract())
            prizemoneys = removeunichars(prizemoneys_)

            #tipster success?
            tippedby = None
            if response.xpath("//img[contains(@title,'Tipped by')]"):
                tippedby_ = response.xpath("//img[contains(@title,'Tipped by')]/@title").extract()[0]
                tippedby = tippedby_.replace("tipped by", "")
            print("racetitle, racetime, racename, prizemoneys, tippedby\n")
            print(racetitle, racetime, racename, prizemoneys, tippedby)
            print("\n")
            ##RESULTS GRID
            norunners = float(response.xpath("count(//table[contains(@class,'resultRaceGrid')]//tbody//tr[@data-hid])").extract()[0])
            # print("norunners", norunners)
            runnerslist = response.xpath("//table[contains(@class,'resultRaceGrid')]//tbody//tr[@data-hid]//td[4]/span/b/a/@href").extract()
            alllbws = response.xpath("//table[contains(@class,'resultRaceGrid')]//tbody//tr[@data-hid]//td[4]/span/b/a/@href/../../../../../td[3]/text()").extract()
            runnerlbws = defaultdict(list)
            for i, (ru,l) in enumerate(zip(runnerslist, alllbws)):
                vallist = []
                if re.match(horseid_pat, ru):
                    horseid = re.match(horseid_pat, ru).group(1)
                    vallist.append(horseid)
                    vallist.append( clean_lbwresult(l) )
                    runnerlbws[str(i)] = vallist

            if len(runnerlbws) >1:
                print("runnerlbws---------->")
                print(runnerlbws)
                winninghorse = runnerlbws['0'][0]
                winninglbw = -1* float(runnerlbws['1'][1])
                print "winninghorse and lbw: \n"
                print (winninghorse, winninglbw)
            # alllbws_ = response.xpath("//table[contains(@class, 'resultRaceGrid')]/tbody/tr[@data-hid]//td[3]//text()").extract()
            # alllbws = [clean_lbwresult(x) for x in alllbws_]
            # if alllbws:
            #     winninglbw = round(-1*float(alllbws[1]),2)
            # else:
            #     winninglbw = None
            for tr in response.xpath("//table[contains(@class, 'resultRaceGrid')]/tbody/tr[@data-hid]"):
                l = ResultsItemLoader(item=ResultsItem(), response=response)
                r = RaceItemLoader(item=RaceItem(), response=response)
                lto = LTOItemLoader(item=LTOItem(), response=response)
                nto = NTOItemLoader(item=NTOItem(), response=response)
                v = VenueItemLoader(item=VenueItem(), response=response)
                j = JockeyItemLoader(item=JockeyItem(), response=response)
                t = TrainerItemLoader(item=TrainerItem(), response=response)

                v.add_value('venueid', racecourseid)
                v.add_value('name', racecoursename)
                # l.add_value('racetitle', racetitle)

                ### RACEITEM

                r.add_value('raceid', raceid)
                r.add_value('raceurl', response.url)
                r.add_value('racedate', self.racedate)
                r.add_value('racename', racename)
                r.add_value('raceid', raceid)
                r.add_value('prizemoneys', prizemoneys)
                r.add_value('racetime', racetime)
                r.add_value('norunners', norunners)



                #redundancy x1
                l.add_value('raceid', raceid)
                ###
                l.add_value('tippedby', tippedby)
                l1raceid = None
                if tr.xpath("td[1]/a/@href").extract():
                    l1raceurl = tr.xpath("td[1]/a/@href").extract()[0]
                    if re.match(raceid_pat, l1raceurl):
                        l1raceid = re.match(raceid_pat, l1raceurl).group(1)
                l.add_value('l1raceid', l1raceid)
                lto.add_value('raceid', l1raceid)
                ##n1
                n1raceid = None
                if tr.xpath("td[@class='last'][2]/a/@href").extract():
                    n1raceurl = tr.xpath("td[@class='last'][2]/a/@href").extract()[0]
                    if re.match(raceid_pat, n1raceurl):
                        n1raceid = re.match(raceid_pat, n1raceurl).group(1)
                l.add_value('n1raceid', n1raceid)
                nto.add_value('raceid', n1raceid)

                pos = tr.xpath("td[2]/h3/text()").extract()[0]
                draw_ = tr.xpath("td[2]/span/text()").extract()
                draw = None
                if draw_:
                    draw = draw_[0]
                lbw_ = tr.xpath("td[3]/text()").extract()[0].strip()
                lbw =clean_lbwresult(lbw_)
                # if pos == u'1':
                #     lbw = winninglbw
                horseurl = tr.xpath("td[4]/span/b/a/@href").extract()[0]
                horsename =  tr.xpath("td[4]/span/b/a/text()").extract()[0].upper()

                if re.match(horseid_pat, horseurl):
                    horseid = re.match(horseid_pat, horseurl).group(1)
                sp_ =  " ".join(tr.xpath("td[4]/span/text()").extract() ) #do pattern match to get
                sp = None
                if re.match(sp_pat, sp_):
                    sp = re.match(sp_pat, sp_).group(1)
                    sp = decimalizeodds(sp)
                # print("raceid, pos, draw, lbw\n")
                # print(l1raceid, pos, draw, lbw)
                # print("-----------------------")
                # print(horseurl, sp, horsename)
                #td5 is weight
                trainerurl = tr.xpath("td[7]/a[contains(@href, 'trainer_id')]/@href").extract()[0]
                trainername = tr.xpath("td[7]/a[contains(@href, 'trainer_id')]/text()").extract()[0]
                jockeyurl = tr.xpath("../tr/td[2]/a[contains(@href, 'jockey_id')]/@href").extract()[0]
                jockeyname = tr.xpath("../tr/td[2]/a[contains(@href, 'jockey_id')]/text()").extract()[0]
                # print("TRAINERURL : ", trainerurl)
                # print("JOCKEYURL : ", jockeyurl)
                trainerid = None
                jockeyid = None
                if re.match(trainerid_pat, trainerurl):
                    trainerid = re.match(trainerid_pat, trainerurl).group(1)
                if re.match(jockeyid_pat, jockeyurl):
                    jockeyid = re.match(jockeyid_pat, jockeyurl).group(1)

                raceComments = " ".join(tr.xpath("../tr[@class='rowComment']//td//text()").extract()).strip()
                l.add_value('raceComments', raceComments)
                l.add_value('pos', pos)
                l.add_value('draw', draw)
                l.add_value('lbw', lbw)
                l.add_value('sp', sp)
                l.add_value('horseid', horseid)
                l.add_value('horsename', horsename)
                l.add_value('trainerid', trainerid)
                l.add_value('jockeyid', jockeyid)

                t.add_value('trainername', trainername)
                t.add_value('trainerid', trainerid)
                j.add_value('jockeyname', jockeyname)
                j.add_value('jockeyid', jockeyid)

                # ri = response.xpath("//div[@class='raceInfo']")
            # l.add_value("runners", ri.xpath("b[text()[contains(.,'ran')]]/text()").extract()[0].strip().replace("ran", "").strip())
            # l.add_value("paceinfo", ri.xpath("b[text()[contains(.,'TIME')]]/following-sibling::text()").extract()[0].strip() )
            #format 3m 58.40s (slow by 7.40s) '

            # #race analysis ALL text to racereport
            # l.add_value("racereport", " ".join(response.xpath("//div[@id='ANALYSIS']").extract()) )

            ###NESTED
                ra_item = r.load_item()
                ra_item['venue'] = v.load_item()
                l_item = l.load_item()
                l_item['race'] = ra_item
                l_item['jockey'] = j.load_item()
                l_item['trainer'] = t.load_item()
                l_item['n1race'] = nto.load_item()
                l_item['l1race'] = lto.load_item()
                # table_data.append(i)
                # yield i
                # for link in LinkExtractor(restrict_xpaths="//a[contains(@href,'horse_id')]/..", deny=( [r'.*/stallion/.*', r'.*/dam/.*' ]) ).extract_links(response):
                #     yield Request(link.url, callback=self.parse_horse, meta=dict(table_data=table_data))
                #do per horse
                if horseurl:
                    yield Request(
                    horseurl,
                    callback=self.parse_horse,
                    meta={
                        'item': l_item
                    }
                    )

    def parse_horse(self, response):

        l = ResultsItemLoader(item=ResultsItem(response.meta['item']), response=response)

        # table_data = response.meta["table_data"]
        # pprint.pprint("tabledata:\n")
        # print(table_data[0])
        # item = items.RpostResultsItem()
        # l = ResultsItemLoader()
        # l.add_value(None,table_data[0])

        #now HorseItem
        hl = HorseItemLoader(item=HorseItem(), response=response)
        owners_ = ";".join( response.xpath("//ul[@id='detailedInfo']/li[contains(text(), 'Owner')]/b//text()").extract())
        owners = tf(owners_.strip().split(";"))
        hl.add_value("owners", owners)
        horseurl = response.url
        hl.add_value("horseurl", horseurl)
        if re.match(horseid_pat, horseurl):
            horseid = re.match(horseid_pat, horseurl).group(1)
            hl.add_value("horseid", horseid)
        details = response.xpath("//ul[@id='detailedInfo']")
        hdetails= details.xpath("//li/b/text()").extract()[0].strip() #format u'4-y-o (19Apr11 b f)'
        # age = re.split('-y-o', details)
        date_string = re.split('-y-o', hdetails)[1].replace('(', "").replace(')', "").strip().split(' ')[0]

        hdob = datetime.strptime(date_string, '%d%b%y').date()
        hcolor = re.split('-y-o', hdetails)[1].replace('(', "").replace(')', "").strip().split(' ')[1]
        hsex = re.split('-y-o', hdetails)[1].replace('(', "").replace(')', "").strip().split(' ')[2]

        #convert to useful format from http://strftime.org/ 19Apr11 strftime %d%b%y datetime.strptime(date_string, '%d%b%y')

        # hl.add_value('horsename',table_data[0]['horsename'])
        hl.add_value("dob", hdob)
        hl.add_value("color", hcolor)
        hl.add_value("sex", hsex)
        # l.add_value("hdetails", details.xpath("//li/b/text()").extract()[0].strip())
        hl.add_value("sire", details.xpath("//a[contains(@href,'stallionbook')]/text()").extract()[0].strip())
        hl.add_value("dam", details.xpath("//a[contains(@href,'dam_home')]/text()").extract()[0].strip())
        # l.add_value("damsire", details.xpath("//a[contains(@href,'stallionbook')]/text()").extract()[0].strip())
        # l.add_value("trainername", details.xpath("//a[contains(@href,'trainer_id')]/text()").extract()[0].strip())

        # l.add_value("owner", details.xpath("//a[contains(@href,'owner_id')]/text()").extract()[0].strip())
        hl.add_value("breeder",details.xpath("//li[text()[contains(.,'Breeder')]]/b/text()").extract()[0].strip())


        # l['horse'] = hl.load_item()
        l.add_value('horse', hl.load_item() )
        # yield hl.load_item()
        yield l.load_item()
