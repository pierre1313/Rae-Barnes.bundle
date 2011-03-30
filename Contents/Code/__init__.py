PLUGIN_PREFIX   = "/photos/RaeBarnes"
ROOT_URL        = "http://www.raebarnes.com"
RSS_FEED        = ROOT_URL + "/rss/"

####################################################################################################
def Start():

  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "Rae Barnes", "icon-default.png", "art-default.png")
  Plugin.AddViewGroup("Pictures", viewMode="Pictures", mediaType="photos")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.art = "art-default.png"
  DirectoryItem.thumb = "icon-default.png"

####################################################################################################
def MainMenu():
    dir = MediaContainer(title2="Details", title1="Rae Barnes")
    for item in XML.ElementFromURL(RSS_FEED).xpath("//item"):
      #Log(HTML.StringFromElement(item))
      
      title = item.xpath('.//title')[0].text
      url = item.xpath('.//guid')[0].text
      raw_summary = HTML.StringFromElement(item.xpath('.//description')[0]).replace(']]','').replace('<![CDATA[','').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','')#.text
      summary = HTML.ElementFromString(raw_summary).text_content()[:400]+"..."
      try:
        thumb = HTML.ElementFromString(raw_summary).xpath('.//img')[0].get('src')
      except:
        thumb = None
        
      dir.Append(Function(DirectoryItem(PictureMenu, title=title, thumb=thumb, summary=summary), url=url))
     
     #  entry = HTML.ElementFromString(item.description)
#       imgs = entry.xpath('//img')
#       if len(imgs) > 5:
#         thumb = ''
#         for img in imgs:
#           if img.get('src').find('raebarnes.com/images/content') != -1:
#             thumb = img.get('src')
#             
#         summary = entry.text_content()[:400] + '...'
#         dir.Append(Function(DirectoryItem(PictureMenu, item.title, thumb, summary),url=item.link,title=item.title))
    return dir

def PictureMenu(sender, url,title = ''):
  dir = MediaContainer(viewGroup="Pictures", title1="Rae Barnes", title2=title)
  count = 1
  for img in HTML.ElementFromURL(url).xpath('//img'):
    if img.get('src').find('/images/content') != -1:
      url = ROOT_URL + img.get('src')
      dir.Append(PhotoItem(url, 'Photo %d' % count, '', url))
      count += 1
    
  return dir
