from updater import Updater

PREFIX = '/video/srfpodcast'
NAME = L('Title')
ART = 'art.png'
ICON = 'icon.png'

API_DIR = 'http://www.srf.ch/play/tv/episodesfromshow?layout=json&id='
API_ITEM = 'https://il.srgssr.ch/integrationlayer/1.0/ue/srf/video/play/%s.json'

API_BASE = 'http://www.srf.ch/podcasts#!program='
API_ALL = API_BASE + 'pt-tv'
API_SRF1 = API_BASE + 'pr-srf-1'
API_SRF2 = API_BASE + 'pr-srf-2'
API_SRFI = API_BASE + 'pr-srf-info'

# http://www.srf.ch/play/tv/sendung/einstein?id=f005a0da-25ea-43a5-b3f8-4c5c23b190b3
# http://www.srf.ch/feed/podcast/hd/f005a0da-25ea-43a5-b3f8-4c5c23b190b3.xml
# http://www.srf.ch/play/tv/episodesfromshow?id=f005a0da-25ea-43a5-b3f8-4c5c23b190b3&pageNumber=1&layout=json

###############################################################################
def Start():

    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR

    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


####################################################################################################
# Let's check the preferences
def ValidatePrefs():

    if int(Prefs['items_per_page']) < 10:
        Prefs['items_per_page'] = 25


####################################################################################################
# Main Menu is static
@handler(PREFIX, NAME, art=ART, thumb=ICON)
def VideoMainMenu():

    oc = ObjectContainer(title1=L('Title'))

    oc.add(DirectoryObject(key=Callback(SubMenu, title='Alle TV-Sendungen', url=API_ALL), title='Alle TV-Sendungen'))
    oc.add(DirectoryObject(key=Callback(SubMenu, title='SRF 1', url=API_SRF1), title='SRF 1'))
    oc.add(DirectoryObject(key=Callback(SubMenu, title='SRF zwei', url=API_SRF2), title='SRF zwei'))
    oc.add(DirectoryObject(key=Callback(SubMenu, title='SRF info', url=API_SRFI), title='SRF info'))

    return oc


####################################################################################################
# List shows of the selected channel
@route(PREFIX + '/submenu')
def SubMenu(title, url):

    oc = ObjectContainer(title1=L('Title'), title2=title)

    oc.add(DirectoryObject(
        key=Callback(GetDirectory, title='Einstein HD', id='f005a0da-25ea-43a5-b3f8-4c5c23b190b3'),
        title='Einstein HD',
        thumb=Resource.ContentsOfURLWithFallback('http://ws.srf.ch/asset/image/audio/10b9b28f-7667-4816-80ea-134442a38cf6/PODCAST/1448274538000.jpg')))

    return oc


####################################################################################################
# List episodes of the selected show
@route(PREFIX + '/directory')
def GetDirectory(title, id, page=1):

    oc = ObjectContainer(title1=L('Title'), title2=title)

    url = API_DIR + id + '&pageNumber=' + str(page)
    try:
        feed = JSON.ObjectFromURL(url, cacheTime=None)
    except:
        return ObjectContainer(header='Empty', message='There are no episodes available.')

    pages = int(feed['maxPageNumber'])
    nextpage = str(int(page) + 1)

    Log.Debug(url)

    for item in feed['episodes']:

        try:
            item_id = item['assets'][0]['url'][-36:]
            Log.Debug(item_id)
        except:
            pass

        url = API_ITEM %item_id
        Log.Debug(url)

        oc.add(VideoClipObject(
            url = url,
            title = item['title'],
            summary = item['description'],
            duration = 2169,
            thumb = Resource.ContentsOfURLWithFallback(item['imageUrl'])
        ))

    # Too much episodes in the current page? TODO: bad solution
    if len(oc) == 10 and page < pages:
        oc.add(NextPageObject(key=Callback(GetDirectory, title=title, id=id, page=nextpage), title='MoreItems'))

    return oc
