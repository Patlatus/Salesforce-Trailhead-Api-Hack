from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import http.client, urllib.request, urllib.parse, urllib.error, gzip, io,  json

def getTrailheadDataByUserIdAndURL(link, userId, isDebug):
    conn = http.client.HTTPSConnection('trailblazer.me')
    requestBody = 'message=%7B%22actions%22%3A%5B%7B%22id%22%3A%2267%3Ba%22%2C%22descriptor%22%3A%22aura%3A%2F%2FApexActionController%2FACTION%24execute%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22namespace%22%3A%22%22%2C%22classname%22%3A%22TrailheadProfileService%22%2C%22method%22%3A%22fetchTrailheadData%22%2C%22params%22%3A%7B%22userId%22%3A%22' + userId + '%22%2C%22language%22%3A%22en-US%22%7D%2C%22cacheable%22%3Afalse%2C%22isContinuation%22%3Afalse%7D%7D%5D%7D&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22kHqYrsGCjDhXliyGcYtIfA%22%2C%22app%22%3A%22c%3AProfileApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fc%3AProfileApp%22%3A%22ZoNFIdcxHaEP9RDPdsobUQ%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%22srcdoc%22%3Atrue%7D%2C%22uad%22%3Atrue%7D&aura.pageURI=' + urllib.parse.quote_plus(link) + '&aura.token=undefined'
    headers = {
    'Host': 'trailblazer.me',
    'Connection': 'keep-alive',
    'Content-Length': len(requestBody),
    'Origin': 'https://trailblazer.me',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://trailblazer.me' + link,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
    }
    conn.request(
        "POST",
        "/aura?r=0&aura.ApexAction.execute=1",
        requestBody,
        headers
    )
    if isDebug:
        print("requestBody: " + requestBody)
        print("headers: " + json.dumps(headers))
        print("Referer: " + 'https://trailblazer.me' + link)
    response = conn.getresponse()
    if isDebug:
        print(response.status, response.reason)
        print(response.getheaders())
     
    data = response.read()
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
        data = gz.read()
    if isDebug:
        print(data)
    data = data.decode('utf-8');
    if isDebug:
        print(data)

    pos = data.find('{')
    if pos < 0:
        result = {}
    data = data[pos:len(data)]
    data = data[::-1]
    pos = data.find('}')
    if pos < 0:
        result = {}
    data = data[pos:len(data)]
    data = data[::-1]


 

    #print data.actions
    x = json.loads(data)
    #print x 
    result = None 
    if (not('actions' in x) and ('event' in x) ):
        if isDebug:
            print(x['event']['descriptor'])
        result = {'error':'Need to update our code','descriptor':x['event']['descriptor']}
    elif ( x["actions"][0]["state"] == "SUCCESS" ):
        y = json.loads(x["actions"][0]["returnValue"]["returnValue"]["body"])
        #print json.dumps(y["value"][0]["ProfileCounts"][0])
        result = y["value"][0]["ProfileCounts"][0]
    else:
        result = {}
    conn.close()
    return result
 
def getUserId(link, isDebug):
    conn = http.client.HTTPSConnection('trailblazer.me')
    conn.request("GET", link, '' , {})
    response = conn.getresponse()
    #print(response.status, response.reason)
    #print(response.getheaders())
    data = response.read()
    body = "".join(map(chr, data))
    #print data
    pos = body.find('\\"Id\\":\\"')
    result = None
    if (pos >= 0):
        userId = body[pos+9:pos+27]
        if (isDebug):
            print("user id found: " + userId + " and current link = " + link)

        result = getTrailheadDataByUserIdAndURL(link, userId, isDebug)
    else:
        result = {'error':'User link not found','link':link,'data':body}
    conn.close()
    return result

def index(request):
    qd = request.GET if request.method == 'GET' else request.POST
    l = qd['link'] if ('link' in qd) else ''
    return HttpResponse(json.dumps(getUserId(l, False)) if (l != '') else 'pass link to user profile in format ?link=/id/userAlias')

def debug(request):
    qd = request.GET if request.method == 'GET' else request.POST
    l = qd['link'] if ('link' in qd) else ''
    return HttpResponse(json.dumps(getUserId(l, True)) if (l != '') else 'pass link to user profile in format ?link=/id/userAlias')
