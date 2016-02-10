# d = response.url.split("_")
# l.add_value('racedate', ''.join([ i for i in d[-2] if i.isdigit()]))
# l.add_value('rpraceid', ''.join([ i for i in d[-1] if i.isdigit()]))
# racecourse = response.xpath('//title').extract()[0].split('|')[0].strip().split("At ")[-1]
# l.add_value('racecourse', racecourse)
# if u'(AW)' in racecourse:
#     l.add_value('surface', 'AWT')
# else:
#     l.add_value('surface', 'Turf')
# l.add_value('racetime', response.xpath('//title/text()').extract()[0].split('|')[0].strip().split(" Race")[0].replace("Results From The ", ""))
# # l.add_value('racename', response.xpath("//h3[@class='clearfix']/text()").extract()[0].strip())
# #race number?
# #race name, racetype
#
# racedetails = response.xpath("//div[@class='leftColBig']/ul/li/text()")
# l.add_value("raceclass", racedetails.extract()[0].split('\n')[1].replace("(", '').replace(")", "").strip())
# l.add_value("raceratingspan", racedetails.extract()[0].split('\n')[2].split(",")[0].replace("(", "").replace(")", "").strip())
# l.add_value("agerestriction", racedetails.extract()[0].split('\n')[2].split(")")[0].split(",")[-1].replace("(", "").strip())
# l.add_value("imperialdistance", racedetails.extract()[0].split('\n')[2].split(" ")[-1].replace("(", "").replace(")", ""))
# item['racedate'] = ''.join([ i for i in d[-2] if i.isdigit()]) #yyyymmdd
# item['rpraceid'] = ''.join([ i for i in d[-1] if i.isdigit()])

# # response.xpath('//title').extract()[0].split('|')[0].strip()
# item['racecourse'] = response.xpath('//title').extract()[0].split('|')[0].strip().split("At ")[-1]
# item['racetime'] = response.xpath('//title/text()').extract()[0].split('|')[0].strip().split(" Race")[0].replace("Results From The ", "")

# #raceinfo
# race = response.xpath("//div[@class='leftColBig']").extract()
# # racename = response.xpath("//div[@class='leftColBig']/h3/text()").extract()[0].strip()

# # [u'', u' (Class 4) ', u' (0-105, 4yo+) (2m110y)', u' ', u' 2m\xbdf Good 8 hdles ']
# response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[0].split('\n')
# item['raceclass'] = response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[0].split('\n')[1].replace("(", '').replace(")", "").strip()

# # u' (0-105, 4yo+) (2m110y)' ratingband agerestrictin (imperialdistance mfy)
# racedata = response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[0].split('\n')[2]
# item['ratingband'] = response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[0].split('\n')[2].split(",")[0].replace("(", "").replace(")", "").strip()
# item['agerestriction'] = response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[0].split('\n')[2].split(")")[0].split(",")[-1].replace("(", "").strip()
# item['imperialdistance'] = response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[0].split('\n')[2].split(" ")[-1].replace("(", "").replace(")", "")
# pprint.pprint(l.load_item())
# # #prizemoney
# # prized = {}
# pm = response.xpath("//div[@class='leftColBig']/ul/li/text()").extract()[1].split('\n')
# pms = [i.encode('ascii', 'ignore') for i in pm]
# pms2 = pms[0].split(', ')
# pms = [ decimal.Decimal(i.replace(',','')) for i in pms2]
# pms.sort() #inline
# # for k, prize in enumerate(sorted(pms, reverse=True)):
# #     l.add_value('pm'+ str(k+1), prize)
#     # prized[str(i+1)] = prize
# l.add_value('prizemoney', sum(pms))

# #raceinfo
        # yield item
            #the horses

            # for i, r in enumerate(response.xpath("//table/tbody")):
            #     #tds - blank horsenumber, lbw, horsename country sp (td span a), age, carrierWt, OR, TS , OPR,  RATED
            #     #if * then not logged in!
            #     position
            #     lbw
            #     horse_id
            #     horsename
            #     horsecountry
            #     sp = winodds
            #     age
            #     weight
            #     trainername
            #     OR
            #     TS
            #     RPR
            #     jockeyname
            #     commentText


    ##NATCH HORSE WITH CORRECT ENTRY IN TABLE DATA
    ##NOT MATCHING UP!

    
