import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import pytz
from pytz import timezone
import csv

#### Script for scaping local venue websites and finding concerts featuring local bands.
#### Stores shows in .csv readable by event_creator.
#### Author: Cameron Nielsen
#### Updated: 12/6/19
def main():
    bands = ["311","Deathwish","The Kings Company","Fat Nap","Reck Lèss",
             "4 Miles From Home","Smokin’ Shepherd","Courthouse Avenue",
             "Bearwithus","Lifeline","The Power Strangers","Stephen Bils",
             "Nick Rucker","IRRAFFARRI",'Thats Chance','Miss VA','Net.Avenue',
             'Eric King','DJ Shif-D','Kaylyn Sahs','King Xander','DJ Frost',
             'Ryan Nordstrom','Mary Ruth McLeay','Topher Booth','Abby Thurin',
             'Bill Riccetti','Justin Carlisle','Super Moon','Fish House Punch',
             'Marcy Yates','Op2mus','Timmy Gee','White Wolf T-Shirt','Mellie L.',
             'Rey Styles','Britta Tollefsrud','Battling Giants','Aj The Dread',
             'Artillery Funk','Lindsay Donovan','Lot Walks','Hiip','TKO',
             'Jamire Gray','HOSPICE','Jocelyn','Pancho and the Contraband',
             'Mike Bama','A Wasted Effort','Low Long Signal','Edem','Vashauna',
             'Emeka','Quit Being A Creeper','The Ragabonds','Omaha Street Percussion',
             'Morse Code','Brian Detweiler','The Sharp Young Men','Emily Ward',
             'Cannonista','Hope Dunbar','The 13th Letter','Reed Scott Nohrenberg',
             'Unscene Patrol','Arson City','Satchel Grande','Pony Creek',
             'Garst','Vago','Superman’s Hero','The George Heaston Experience',
             'Sebastian Lane']

    #### Creates .csv to store shows with their details. Calls functions to
    #### scrape each venue website.
    with open('shows.csv', mode='w') as csvFile:
        fieldnames = ['EventTitle', 'Location', 'StartDateTime', 'EndDateTime', 'Link']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()
        WaitingRoom(bands, writer)
        ReverbLounge(bands, writer)
        Slowdown(bands, writer)
##        SokolAuditorium(bands, writer)

    csvFile.close()

#########################################################################
def WaitingRoom(bands, writer):
    result = requests.get("https://waitingroomlounge.com/events/", headers={'User-Agent': 'Mozilla/5.0'})
    print(result.status_code)
    src = result.content
    soup = BeautifulSoup(src, features="html.parser")

    eventList = soup.find_all("div", {"class": "rhino-event-section rhino-list-view"})
    for event in eventList:
        links = event.find_all("a")
        opener = event.find('h3')
        for link in links:
            for band in bands:
                if link(text=re.compile(band)) != []:
                    eventTitle = link.get("title").strip()
                    eventMonth = event.find("div", {"class": "rhino-event-datebox-month"}).getText().strip()
                    eventDate = event.find("div", {"class": "rhino-event-datebox-date"}).getText().strip()
                    eventTime = event.find("div", {"class": "rhino-event-time-box"}).getText().strip()
                    eventLink = link.attrs['href'].strip()
                    if datetime.now().month > datetime.strptime(eventMonth, '%b').month:
                        eventYear = datetime.now().year + 1
                    else:
                        eventYear = datetime.now().year
                    dateTime_str = eventMonth+" "+eventDate+" "+eventTime+" "+str(eventYear)
                    dateTime_obj = datetime.strptime(dateTime_str, '%b %d %I:%M %p %Y')
                    central = timezone('America/Chicago')
                    dateTime_objEnd = dateTime_obj + timedelta(hours=3)

                    print(eventTitle)
                    print(dateTime_obj)
                    print(dateTime_objEnd)
                    print(eventLink)

                    writer.writerow({'EventTitle': eventTitle, 'Location': 'The Waiting Room', 'StartDateTime': dateTime_obj,
                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
                    
                ### Checks if a local band is an opener
                if event.find('h3') and link.parent.name == 'h2':
                    if opener(text=re.compile(band)) != []:
                        eventTitle = band+' -SUPPORTING- '+link.get("title").strip()
                        eventMonth = event.find("div", {"class": "rhino-event-datebox-month"}).getText().strip()
                        eventDate = event.find("div", {"class": "rhino-event-datebox-date"}).getText().strip()
                        eventTime = event.find("div", {"class": "rhino-event-time-box"}).getText().strip()
                        eventLink = link.attrs['href'].strip()
                        if datetime.now().month > datetime.strptime(eventMonth, '%b').month:
                            eventYear = datetime.now().year + 1
                        else:
                            eventYear = datetime.now().year
                        dateTime_str = eventMonth+" "+eventDate+" "+eventTime+" "+str(eventYear)
                        dateTime_obj = datetime.strptime(dateTime_str, '%b %d %I:%M %p %Y')
                        central = timezone('America/Chicago')
                        dateTime_objEnd = dateTime_obj + timedelta(hours=3)

                        print(eventTitle)
                        print(dateTime_obj)
                        print(dateTime_objEnd)
                        print(eventLink)

                        writer.writerow({'EventTitle': eventTitle, 'Location': 'The Waiting Room', 'StartDateTime': dateTime_obj,
                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
        
######################################################################

def ReverbLounge(bands, writer):
    result = requests.get("https://reverblounge.com/events/", headers={'User-Agent': 'Mozilla/5.0'})
    print(result.status_code)
    src = result.content
    soup = BeautifulSoup(src, features="html.parser")

    eventList = soup.find_all("div", {"class": "rhino-event-section rhino-list-view"})
    for event in eventList:
        links = event.find_all("a")
        opener = event.find('h3')
        for link in links:
            for band in bands:
                if link(text=re.compile(band)) != []:
                    eventTitle = link.get("title").strip()
                    eventMonth = event.find("div", {"class": "rhino-event-datebox-month"}).getText().strip()
                    eventDate = event.find("div", {"class": "rhino-event-datebox-date"}).getText().strip()
                    eventTime = event.find("div", {"class": "rhino-event-time-box"}).getText().strip()
                    eventLink = link.attrs['href'].strip()
                    if datetime.now().month > datetime.strptime(eventMonth, '%b').month:
                        eventYear = datetime.now().year + 1
                    else:
                        eventYear = datetime.now().year
                    dateTime_str = eventMonth+" "+eventDate+" "+eventTime+" "+str(eventYear)
                    dateTime_obj = datetime.strptime(dateTime_str, '%b %d %I:%M %p %Y')
                    central = timezone('America/Chicago')
                    dateTime_objEnd = dateTime_obj + timedelta(hours=3)

                    print(eventTitle)
                    print(dateTime_obj)
                    print(dateTime_objEnd)
                    print(eventLink)

                    writer.writerow({'EventTitle': eventTitle, 'Location': 'Reverb Lounge', 'StartDateTime': dateTime_obj,
                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
                    
                ### Checks if a local band is an opener
                if event.find('h3') and link.parent.name == 'h2':
                    if opener(text=re.compile(band)) != []:
                        eventTitle = band+' -SUPPORTING- '+link.get("title").strip()
                        eventMonth = event.find("div", {"class": "rhino-event-datebox-month"}).getText().strip()
                        eventDate = event.find("div", {"class": "rhino-event-datebox-date"}).getText().strip()
                        eventTime = event.find("div", {"class": "rhino-event-time-box"}).getText().strip()
                        eventLink = link.attrs['href'].strip()
                        if datetime.now().month > datetime.strptime(eventMonth, '%b').month:
                            eventYear = datetime.now().year + 1
                        else:
                            eventYear = datetime.now().year
                        dateTime_str = eventMonth+" "+eventDate+" "+eventTime+" "+str(eventYear)
                        dateTime_obj = datetime.strptime(dateTime_str, '%b %d %I:%M %p %Y')
                        central = timezone('America/Chicago')
                        dateTime_objEnd = dateTime_obj + timedelta(hours=3)

                        print(eventTitle)
                        print(dateTime_obj)
                        print(dateTime_objEnd)
                        print(eventLink)

                        writer.writerow({'EventTitle': eventTitle, 'Location': 'Reverb Lounge', 'StartDateTime': dateTime_obj,
                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
        
#########################################################################
def Slowdown(bands, writer):
    result = requests.get("https://www.theslowdown.com/listing/", headers={'User-Agent': 'Mozilla/5.0'})
    print(result.status_code)
    src = result.content
    soup = BeautifulSoup(src, features="html.parser")

    mainList = soup.find("article", {"class": "list-view"})
    eventList = soup.find_all("article", {'class': re.compile('card')})
    for event in eventList:
        headliner = event.find('h1', {'class': 'event-name headliners'})
        opener = event.find('h2', {'class': 'supports'})
        headlinerLink = headliner.find('a')
        if opener: openerLink = opener.find('a')
        for band in bands:
            if headlinerLink(text=re.compile(band)) != []:
                eventTitle = headlinerLink.text.strip()
                eventDate = event.find("span", {"class": "dates"}).getText().strip()[4:]
                eventTime = event.find("span", {"class": "start"}).getText().strip()[6:]
                if len(eventTime) == 4:
                    eventTime = eventTime[:1]+':00'+eventTime[1:]
                eventLink = 'https://www.theslowdown.com'+headlinerLink.attrs['href'].strip()
                dateTime_str = eventDate+" "+eventTime
                dateTime_obj = datetime.strptime(dateTime_str, '%m/%d/%y %I:%M %p')
                central = timezone('America/Chicago')
                dateTime_objEnd = dateTime_obj + timedelta(hours=3)

                print(eventTitle)
                print(dateTime_obj)
                print(dateTime_objEnd)
                print(eventLink)

                writer.writerow({'EventTitle': eventTitle, 'Location': 'The Slowdown', 'StartDateTime': dateTime_obj,
                                 'EndDateTime': dateTime_objEnd, 'Link': eventLink})
                    
                ### Checks if a local band is an opener
            if opener:
                if opener(text=re.compile(band)) != []:
                    eventTitle = band+' -SUPPORTING- '+headlinerLink.text.strip()
                    eventDate = event.find("span", {"class": "dates"}).getText().strip()[4:]
                    eventTime = event.find("span", {"class": "start"}).getText().strip()[6:]
                    if len(eventTime) == 4:
                        eventTime = eventTime[:1]+':00'+eventTime[1:]
                    eventLink = 'https://www.theslowdown.com'+headlinerLink.attrs['href'].strip()
                    dateTime_str = eventDate+" "+eventTime
                    dateTime_obj = datetime.strptime(dateTime_str, '%m/%d/%y %I:%M %p')
                    central = timezone('America/Chicago')
                    dateTime_objEnd = dateTime_obj + timedelta(hours=3)

                    print(eventTitle)
                    print(dateTime_obj)
                    print(dateTime_objEnd)
                    print(eventLink)

                    writer.writerow({'EventTitle': eventTitle, 'Location': 'The Slowdown', 'StartDateTime': dateTime_obj,
                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
        
#########################################################################
def SokolAuditorium(bands, writer):
    result = requests.get("http://sokolauditorium.com/events/", headers={'User-Agent': 'Mozilla/5.0'})
    print(result.status_code)
    src = result.content
    soup = BeautifulSoup(src, features="html.parser")

##    upcoming = soup.find("div", {"class": "_p6e _4-u3"})
    eventList = soup.find_all("div", {"class": "_4-u3"})
    print(eventList)
    for event in eventList:
        print(event)
##    for event in eventList:
##        links = event.find_all("a")
##        opener = event.find('h3')
##        for link in links:
##            for band in bands:
##                if link(text=re.compile(band)) != []:
##                    eventTitle = link.get("title").strip()
##                    eventMonth = event.find("div", {"class": "rhino-event-datebox-month"}).getText().strip()
##                    eventDate = event.find("div", {"class": "rhino-event-datebox-date"}).getText().strip()
##                    eventTime = event.find("div", {"class": "rhino-event-time-box"}).getText().strip()
##                    eventLink = link.attrs['href'].strip()
##                    if datetime.now().month > datetime.strptime(eventMonth, '%b').month:
##                        eventYear = datetime.now().year + 1
##                    else:
##                        eventYear = datetime.now().year
##                    dateTime_str = eventMonth+" "+eventDate+" "+eventTime+" "+str(eventYear)
##                    dateTime_obj = datetime.strptime(dateTime_str, '%b %d %I:%M %p %Y')
##                    central = timezone('America/Chicago')
##                    dateTime_objEnd = dateTime_obj + timedelta(hours=3)
##
##                    print(eventTitle)
##                    print(dateTime_obj)
##                    print(dateTime_objEnd)
##                    print(eventLink)
##
##                    writer.writerow({'EventTitle': eventTitle, 'Location': 'The Waiting Room', 'StartDateTime': dateTime_obj,
##                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
##                    
##                ### Checks if a local band is an opener
##                if event.find('h3') and link.parent.name == 'h2':
##                    if opener(text=re.compile(band)) != []:
####                        eventTitle = band+' - OPENING FOR - '+link.get("title").strip()
##                        eventTitle = band+" - "+link.get("title").strip()
##                        eventMonth = event.find("div", {"class": "rhino-event-datebox-month"}).getText().strip()
##                        eventDate = event.find("div", {"class": "rhino-event-datebox-date"}).getText().strip()
##                        eventTime = event.find("div", {"class": "rhino-event-time-box"}).getText().strip()
##                        eventLink = link.attrs['href'].strip()
##                        if datetime.now().month > datetime.strptime(eventMonth, '%b').month:
##                            eventYear = datetime.now().year + 1
##                        else:
##                            eventYear = datetime.now().year
##                        dateTime_str = eventMonth+" "+eventDate+" "+eventTime+" "+str(eventYear)
##                        dateTime_obj = datetime.strptime(dateTime_str, '%b %d %I:%M %p %Y')
##                        central = timezone('America/Chicago')
##                        dateTime_objEnd = dateTime_obj + timedelta(hours=3)
##
##                        print(eventTitle)
##                        print(dateTime_obj)
##                        print(eventLink)
##                        print(dateTime_objEnd)
##
##                        writer.writerow({'EventTitle': eventTitle, 'Location': 'The Waiting Room', 'StartDateTime': dateTime_obj,
##                                     'EndDateTime': dateTime_objEnd, 'Link': eventLink})
        
    

if __name__ == '__main__':
    main()
