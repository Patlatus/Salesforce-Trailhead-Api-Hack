from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import http.client, urllib.request, urllib.parse, urllib.error, gzip, io,  json

def getTrailheadDataByUserIdAndURL(link, userId):
	conn = http.client.HTTPSConnection('trailblazer.me')
	conn.request("POST", "/aura?r=0&aura.ApexAction.execute=1", 'message=%7B%22actions%22%3A%5B%7B%22id%22%3A%2267%3Ba%22%2C%22descriptor%22%3A%22aura%3A%2F%2FApexActionController%2FACTION%24execute%22%2C%22callingDescriptor%22%3A%22UNKNOWN%22%2C%22params%22%3A%7B%22namespace%22%3A%22%22%2C%22classname%22%3A%22TrailheadProfileService%22%2C%22method%22%3A%22fetchTrailheadData%22%2C%22params%22%3A%7B%22userId%22%3A%22'
		+ userId + '%22%2C%22language%22%3A%22en-US%22%7D%2C%22cacheable%22%3Afalse%2C%22isContinuation%22%3Afalse%7D%7D%5D%7D&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%222a7dI3yJAq4Ks9x5yB5pfg%22%2C%22app%22%3A%22c%3AProfileApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fc%3AProfileApp%22%3A%22yjCZOuI7mJRgwyTzrSDOQw%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%22srcdoc%22%3Atrue%7D%2C%22uad%22%3Atrue%7D&aura.pageURI=' + 
		urllib.parse.quote_plus(link) + '&aura.token=undefined',
		{
	'Host': 'trailblazer.me',
	'Connection': 'keep-alive',
	'Content-Length': 840,
	'Origin': 'https://trailblazer.me',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Accept': '*/*',
	'Sec-Fetch-Site': 'same-origin',
	'Sec-Fetch-Mode': 'cors',
	'Referer': 'https://trailblazer.me' + link,
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9'
	    })
	response = conn.getresponse()
	print(response.status, response.reason)
	print(response.getheaders())
	 
	data = response.read()
	with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
	    data = gz.read()
	data = data.decode('utf-8');
	#print data.actions
	x = json.loads(data)
	#print x 
	result = None 
	if ( x["actions"][0]["state"] == "SUCCESS" ):
		y = json.loads(x["actions"][0]["returnValue"]["returnValue"]["body"])
		#print json.dumps(y["value"][0]["ProfileCounts"][0])
		result = y["value"][0]["ProfileCounts"][0]
	else:
		result = {}
	conn.close()
	return result
 
def getUserId(link):
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

		result = getTrailheadDataByUserIdAndURL(link, userId)
	else:
		result = {'error':'User link not found','link':link,'data':body}
	conn.close()
	return result

#getUserId("/id/yshyshkin")
getUserId("/id/vyaremenko") 

# Create your views here.
def index(request):
    qd = request.GET if request.method == 'GET' else request.POST
    # return HttpResponse('Hello from Python!')
    #return render(request, "index.html")
    l = qd['link'] if ('link' in qd) else ''
    return HttpResponse(json.dumps(getUserId(l)) if (l != '') else 'pass link to user profile in format ?link=/id/userAlias')
    #return render(request, getUserId("/id/yshyshkin"))


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
