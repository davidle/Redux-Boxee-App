import mc
import urllib
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError

def getLoginDetails():
	mc.HideDialogWait()
	#Pop up dialogs
	username = mc.ShowDialogKeyboard("Enter Redux Username", "", False)
	password = mc.ShowDialogKeyboard("Enter Redux Password", "", True)
	
	if username == "" or password == "":
		mc.ShowDialogNotification("You failed to enter anything, playing stuff won't work.")
	
	loginDetails = [username, password]
	#Save details
	config = mc.GetApp().GetLocalConfig()
	config.SetValue('ReduxName', username)
	config.SetValue('ReduxPass', password)
	mc.ShowDialogWait()
	return loginDetails
		
def getNewCookie(loginDetails):
	#loginDetails = getLoginDetails()
	#Set up params
	params = urllib.urlencode([('username', loginDetails[0]), ('password', loginDetails[1]), ('dologin', "1"), ('submit', "log in")])
	print "posting:"
	print params
	#Return pos result
	return mc.Http().Post('http://www.bbcredux.com/', params)

def continueLoading():
	print 'Continuing to load app'
	mc.ActivateWindow(14000)
	replaceList('rss://devapi.bbcredux.com/latest.rss/2m-mp4+mp3')
	mc.HideDialogWait()
	
	
def replaceList(rssUrl):
	items = mc.GetDirectory(rssUrl)
	mc.GetActiveWindow().GetList(120).SetItems(items)
	
	
def search(terms):
	print 'search terms:'
	print terms
	if len(terms) > 3:
		encodedTerms = urllib.urlencode([('sort', 'date'), ('q', terms)])
		queryUrl = 'rss://devapi.bbcredux.com/search.rss/2m-mp4+mp3?sort=date&q='+ encodedTerms
		replaceList(queryUrl) 

mc.ShowDialogWait()
#Check redux status
req = urllib2.Request('http://devapi.bbcredux.com/programme/5668414944669113368/media/m2ts/20111028_064500_bbctwo_pet_squad.ts')
req.get_method = lambda : 'HEAD'
try:
	response = urllib2.urlopen(req)
	print response.read()
	print response.code
except HTTPError, e:
	print 'Initial check error:'
	print e.code
	print e.read()
	
	#Load login details from config store
	config = mc.GetApp().GetLocalConfig()
	loginDetails= []
	reduxName = config.GetValue('ReduxName')
	reduxPass = config.GetValue('ReduxPass')
	print 'login:'
	print reduxName
	print reduxPass
	
	if reduxName and reduxPass:
		print 'Got details from config store'
		loginDetails = [reduxName, reduxPass]
	else:
		print 'Requesting login details'
		loginDetails = getLoginDetails()
	#Login/get a cookie
	result = getNewCookie(loginDetails)	
	if result:
		continueLoading()
	else:
		mc.ShowDialogNotification("Unable to login to Redux")
		mc.GetApp().Close()
		
		
#http = mc.Http()
#http.Get('http://devapi.bbcredux.com/programme/5668456176355154977/')

#resultCode = mc.Http().GetHttpResponseCode()
else:
	continueLoading()
	
	
	