from PMS import Plugin, Log, XML, HTTP, JSON, RSS, Utils
from PMS.MediaXML import MediaContainer, DirectoryItem, PhotoItem

PLUGIN_PREFIX   = "/photos/RaeBarnes"
ROOT_URL        = "http://www.raebarnes.com"
RSS_FEED        = ROOT_URL + "/rss/"

####################################################################################################
def Start():
  Plugin.AddRequestHandler(PLUGIN_PREFIX, HandlePhotosRequest, "Rae Barnes", "icon-default.png", "art-default.png")
  Plugin.AddViewGroup("Pictures", viewMode="Pictures", contentType="photos")
  Plugin.AddViewGroup("Details", viewMode="InfoList", contentType="items")

####################################################################################################
def HandlePhotosRequest(pathNouns, count):
  if count == 0:
    dir = MediaContainer("art-default.png", "Details", "Rae Barnes")
    for item in RSS.Parse(RSS_FEED).entries:
      entry = XML.ElementFromString(item.description, True)
      imgs = entry.xpath('//img')
      if len(imgs) > 5:
        thumb = ''
        for img in imgs:
          if img.get('src').find('raebarnes.com/images/content') != -1:
            thumb = img.get('src')
            
        summary = entry.text_content()[:400] + '...'
        dir.AppendItem(DirectoryItem(Utils.EncodeStringToUrlPath(item.link)+'$'+Utils.EncodeStringToUrlPath(item.title), item.title, thumb, summary))
      
  elif count == 1:
    (url,title) = pathNouns[0].split('$')
    dir = MediaContainer("art-default.png", "Pictures", "Rae Barnes", Utils.DecodeUrlPathToString(title))
    count = 1
    for img in XML.ElementFromURL(Utils.DecodeUrlPathToString(url), True).xpath('//img'):
      if img.get('src').find('/images/content') != -1:
        url = ROOT_URL + img.get('src')
        dir.AppendItem(PhotoItem(url, 'Photo %d' % count, '', url))
        count += 1
    
  return dir.ToXML()
