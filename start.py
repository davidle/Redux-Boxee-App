#imports boxee, urllibs
import mc
import urllib
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import simplejson as json



#Requests login details from users
#Returns [username, password]
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
		
#Get a redux cookie (log in)
#Returns the result of the post
def getNewCookie(loginDetails):
	#Set up params
	params = urllib.urlencode([('username', loginDetails[0]), ('password', loginDetails[1]), ('dologin', "1"), ('submit', "log in")])
	print "posting:"
	print params
	mc.Http().Post('http://www.bbcredux.com/', params)
	


#Displays the first screen after checking redux login details
def continueLoading():
	print 'Continuing to load app'
	mc.ActivateWindow(14000)
	replaceList('rss://devapi.bbcredux.com/latest.rss/2m-mp4+mp3?channel=bbcone')
	mc.HideDialogWait()
	loadTopShows()
	
#Replaces the list in the main part of the screen with an Rss feed from rssUrl 	
def replaceList(rssUrl):
	items = mc.GetDirectory(rssUrl)
	mc.GetActiveWindow().GetList(120).SetItems(items)
	
#Search for text put into text box, this pulls the rss feed as each letter is typed
#Might cause a bit of load...	
def search(terms):
	print 'search terms:'
	print terms

	itemList = mc.ListItems()
	item = mc.ListItem( mc.ListItem.MEDIA_UNKNOWN)
	item.SetLabel("Searching...")
	itemList.append(item)

	if len(terms) > 1:
		encodedTerms = urllib.urlencode([('q', terms)])
		queryUrl = 'rss://devapi.bbcredux.com/search.rss/2m-mp4+mp3?&q='+ encodedTerms
		replaceList(queryUrl) 

#Check if we're authenticated on Redux
def loginCheck():
	data = mc.Http().Get('http://devapi.bbcredux.com/user/')

	try:
		jsonData = json.loads(data)
		if jsonData['activated'] == 1:
			print 'Auth check success:'
			return True
		else:
			return False
	except AttributeError, e:
		print 'Auth check error:'
		print e
		return False

	
#Clear login details from Boxee store
def clearLogin():
	config = mc.GetApp().GetLocalConfig()
	config.Reset('ReduxName')
	config.Reset('ReduxPass')
	mc.ShowDialogNotification("Cleared login details")



#Start here:
mc.ShowDialogWait()

#Check redux login status
authResult = loginCheck()

if authResult:
	#True/logged in - continue
	continueLoading()
else:
	#Not logged in - check store for login details
	config = mc.GetApp().GetLocalConfig()
	loginDetails= []
	reduxName = config.GetValue('ReduxName')
	reduxPass = config.GetValue('ReduxPass')
	print 'login:'
	print reduxName

	#Check details are available
	if reduxName and reduxPass:
		#Yes, use them
		print 'Got details from config store'
		loginDetails = [reduxName, reduxPass]
	else:
		#No ask for them
		print 'Requesting login details'
		loginDetails = getLoginDetails()

	#Login/get a cookie
	getNewCookie(loginDetails)
	
	#Check if the login worked
	authResult2 = loginCheck()

	if authResult2:
		continueLoading()
	else:
		mc.ShowDialogNotification("Unable to login to Redux")
		config = mc.GetApp().GetLocalConfig()
		config.Reset('ReduxName')
		config.Reset('ReduxPass')
		mc.HideDialogWait()
		mc.GetApp().Close()

	
	
	