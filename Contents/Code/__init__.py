from updater import Updater

VIDEO_PREFIX = '/video/srfpodcast'
NAME = L('Title')
ART = 'art.png'
ICON = 'icon.png'

Shows = None
Episodes = None

#API_URL_SHOW = ''
#API_URL_EPISODES = API_URL_SHOW + '/'

###############################################################################
def Start():

    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)

    HTTP.CacheTime = CACHE_1HOUR

    VideoClipObject.thumb = R(ICON)
    VideoClipObject.art = R(ART)


# Let's check the preferences
def ValidatePrefs():

    if int(Prefs['items_per_page']) < 10:
        Prefs['items_per_page'] = 25


# Main Menu
@handler(VIDEO_PREFIX, NAME, art=ART, thumb=ICON)
def VideoMainMenu():

    # Dummy Only
    oc = ObjectContainer(header='Empty', message='There are no shows available.')
    return oc
