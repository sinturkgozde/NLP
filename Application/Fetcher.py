
import urllib2


wiki_link_first_part = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles="
wiki_link_end_part = "&rvprop=content&redirects=true&format=json"

def fetchDataForProcessing(NAME):
    
    data = urllib2.urlopen(wiki_link_first_part+NAME+wiki_link_end_part).read().decode('utf8')
    return data
