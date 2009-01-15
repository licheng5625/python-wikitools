﻿# -*- coding: utf-8 -*-
from wikitools import *
import re
import codecs
import datetime
import time
import settings
site = wiki.Wiki()
userlist = {}
print "Logging in"
site.login(settings.bot, settings.botpass)
l = codecs.open('LogFile.txt', 'wb', 'utf-8')
l.close()
g = codecs.open('ErrorFile.txt','wb', 'utf-8')
g.close()
titlewhitelist = ["Category:Wikipedians who are indefinitely blocked for spamming"]

def main():
	if not site.isLoggedIn(settings.bot): # Make sure we're logged in before doing anything else
		e = open('CrashErrors.txt','w')
		e.write("\Not Logged in\n")
		e.close()
		quit()
	print "Starting..."
	params = {'action':'query',
		'generator':'categorymembers',
		'gcmtitle':'Category:Temporary Wikipedian userpages',
		'prop':'templates|revisions',
		'rvprop':'timestamp',
		'tlnamespace':'10',
		'tllimit':'5000',
		'gcmlimit':'1000',
		'indexpageids':'1',
	}
	req = api.APIRequest(site, params)
	global data
	data = req.query()
	userlist = {}
	print "Starting checks..."
	userlist = firstchecks()	
	blockcheck()
	deletePages()
	errorlog()

def deletePages():
	print "Deleting old pages..."
	log = []
	for pageid in data['query']['pages'].keys():
		if data['query']['pages'][pageid]['title'] in titlewhitelist:
			continue
		ts = data['query']['pages'][pageid]['revisions'][0]['timestamp']
		date = timestampToDate(ts)
		diff = date.today() - date
		if diff.days > 30:
			p = page.Page(site, title=data['query']['pages'][pageid]['title'], check=False, pageid=pageid)
			try:
				print("Deleting "+ p.title)
			except:
				print("Deleting" + p.pageid)
			log.append((p.title, ts))
			# LOG ONLY
			# res = p.delete(reason="Old [[CAT:TEMP|temporary userpage")
			# if not p.exists:
				# l = codecs.open('LogFile.txt', 'ab', 'utf-8')
				# l.write('\n# [[' + p.title + ']] - deleted')
				# l.close()
			# else:
				# reportError(p, "Deletion error"+res['error']['code'])		
	testlog = page.Page(site, settings.bot+"/testing")
	cont = unicode('', 'utf8')
	for entry in log:
		cont+='* [['+entry[0]+']] - '+entry[1]+'\n'
	testlog.edit(newtext=cont.encode('utf8'), summary="Testing", minor=True, bot=True)
		
def firstchecks():
	p = re.compile("(User|User talk):(.*?)\/.*")
	skip = False
	for pageid in data['query']['pages'].keys():
		userpage = data['query']['pages'][pageid]
		title = userpage['title'].encode('utf-8')
		if title in titlewhitelist:
			continue
		if userpage['ns'] != 2 and userpage['ns'] != 3: # Namespace check, only user [talk] should be in the cat
			removePage(title, "wrong namespace", "")
			skip = True
		if not skip and data['query']['pages'][pageid].has_key('templates'):
			for tem in data['query']['pages'][pageid]['templates']:
				if tem['title'] == "Template:Do not delete":
					removePage(title, "{{tl|do not delete}}", "")
					skip = True
					break
		if not skip:
			if title.find('/') != -1:
				username = p.sub(r'\2', title)
			else:
				username = title
				if userpage['ns'] == 2:
					username = username.replace( "User:", "", 1)
				if userpage['ns'] == 3:
					username = username.replace( "User talk:", "", 1)
			userlist[username] = title
		skip = False
	
def errorlog():
	print "Dumping error log"
	g = codecs.open('ErrorFile.txt','rb', 'utf-8')
	errordump = g.read()
	errorpage = page.Page(site, settings.bot+'/errors')
	errortext = "These are pages that the bot missed for whatever reason:\n"
	errorpage.edit(newtext = errortext + errordump, summary="Reporting errors", minor=True)
	g.close()

	print "Dumping edit log"
	l = codecs.open('LogFile.txt','rb', 'utf-8')
	logdump = l.read()
	logpage = page.Page(site, settings.bot+'/log')
	logtext = "These are pages the bot edited and why:\n"
	logpage.edit(logtext + logdump , summary="Edit log", minor=True)
	l.close()
	
def blockcheck():
	print "Starting block check"
	usercounter = 0
	userstring = ''
	users = []
	for user in userlist.keys():
		userstring += user+'|'
		users.append(user)
		usercounter+=1
		if usercounter == 350:
			getblocks(userstring, users)
			usercounter = 0
			userstring = ''
			users = []
	getblocks(userstring, users)
			
def getblocks(userstring, users):
	print "Getting blocks for " + str(len(users)) + " users"
	blockeduserlist = []
	userstring = re.sub('(.*)\|$', r'\1', userstring)
	predata = {'action': 'query',
		'list': 'blocks', 
		'bkusers': userstring, 
		'bklimit':'5000' } 
	req = api.APIRequest(site, predata)
	data = req.query()
	for entry in data['query']['blocks']:
		blockeduserlist.append(entry['user'])
		if not entry['expiry'] == "infinity":
				timestamp = entry['expiry']
				date = timestampToDate(timestamp)
				diff = date - date.today()
				if diff.days < 300:
					removePage(userlist[entry['user']], "not indef blocked", date)
	total = len(users) - len(blockeduserlist)
	counter = 0
	pagesToRemove = []
	for user in users:
		if blockeduserlist.count(user.decode('utf-8')) == 0:
			counter+=1
			pagesToRemove.append(userlist[user])
	if total == counter:
		for page in pagesToRemove:
			removePage(page, "not blocked", "")
	else:
		print "Block check error"
		for page in pagesToRemove:
			reportError(page, "Block check error")
			
def timestampToDate(timestamp):
	year = re.search("\d\d\d\d", timestamp).group(0)
	month = re.search("\d\d\d\d-(\d\d)-(\d\d)", timestamp).group(1)
	day = re.search("\d\d\d\d-(\d\d)-(\d\d)", timestamp).group(2)
	date = datetime.date(int(year), int(month), int(day))
	return date
	
def removePage(pagename, reason, other):
	userpage = page.Page(site, pagename)
	del data['query']['pages'][userpage.pageid]
	try:
		print(userpage.title + " - " + reason)
	except:
		print(userpage.pageid + " - " + reason)
	if other:
		print(other)
	text = userpage.getWikiText()
	newtext = re.sub(r'\[\[Category:Temporary Wikipedian userpages.*?\]\]', '', text)
	newtext = newtext.replace('{{legalthreatblock}}', '{{tl|Legalthreatblock}}')
	newtext = newtext.replace('{{Legalthreatblock}}', '{{tl|Legalthreatblock}}')
	# TODO: these can be cut way down with regexes, but I was feeling lazy
	if reason == "{{tl|do not delete}}":
		newtext = newtext.replace('{{Temporary userpage}}', '')
		newtext = newtext.replace('{{Blockedimpersonator}}', '{{Indefblockeduser|historical}}')
		newtext = newtext.replace('{{Blockedtroll}}', '{{Blockedtroll|historical}}')
		newtext = newtext.replace('{{Indefblockeduser-big}}', '{{Indefblockeduser-big|historical}}')
		newtext = newtext.replace('{{Indefblockeduser}}', '{{Indefblockeduser|historical}}')
		newtext = newtext.replace('{{Indefblockuser}}', '{{Indefblockuser|historical}}')
		newtext = newtext.replace('{{Indefblock}}', '{{Indefblock|historical}}')
		newtext = newtext.replace('{{Indefblocked}}', '{{Indefblocked|historical}}')
		newtext = newtext.replace('{{Indef}}', '{{Indef|historical}}')
		newtext = newtext.replace('{{IndefBlocked}}', '{{IndefBlocked|historical}}')
		newtext = newtext.replace('{{Vpblock}}', '{{Vpblock|historical}}')
		newtext = newtext.replace('{{Pagemovevandal}}', '{{Pagemovevandal|historical}}')
		newtext = newtext.replace('{{Pageblankvandal}}', '{{Pageblankvandal|historical}}')
		newtext = newtext.replace('{{Blockedindef}}', '{{Blockedindef|historical}}')
		newtext = newtext.replace('{{Idb}}', '{{Idb|historical}}')
		newtext = newtext.replace('{{Userindef}}', '{{userindef|historical}}')
		newtext = newtext.replace('{{VOAblock}}', '{{VOAblock|historical}}')
	
		newtext = newtext.replace('{{temporary userpage}}', '')
		newtext = newtext.replace('{{blockedimpersonator}}', '{{Indefblockeduser|historical}}')
		newtext = newtext.replace('{{blockedtroll}}', '{{Blockedtroll|historical}}')
		newtext = newtext.replace('{{indefblockeduser-big}}', '{{Indefblockeduser-big|historical}}')
		newtext = newtext.replace('{{indefblockeduser}}', '{{Indefblockeduser|historical}}')
		newtext = newtext.replace('{{indefblockuser}}', '{{Indefblockuser|historical}}')
		newtext = newtext.replace('{{indefblock}}', '{{Indefblock|historical}}')
		newtext = newtext.replace('{{indefblocked}}', '{{Indefblocked|historical}}')
		newtext = newtext.replace('{{indef}}', '{{Indef|historical}}')
		newtext = newtext.replace('{{indefBlocked}}', '{{IndefBlocked|historical}}')
		newtext = newtext.replace('{{vpblock}}', '{{Vpblock|historical}}')
		newtext = newtext.replace('{{pagemovevandal}}', '{{Pagemovevandal|historical}}')
		newtext = newtext.replace('{{pageblankvandal}}', '{{Pageblankvandal|historical}}')
		newtext = newtext.replace('{{blockedindef}}', '{{Blockedindef|historical}}')
		newtext = newtext.replace('{{idb}}', '{{Idb|historical}}')
		newtext = newtext.replace('{{userindef}}', '{{userindef|historical}}')
		newtext = newtext.replace('{{vOAblock}}', '{{VOAblock|historical}}')
	else:
		newtext = newtext.replace('{{Temporary userpage}}', '')
		newtext = newtext.replace('{{Blockedimpersonator}}', '{{tl|Indefblockeduser}}')
		newtext = newtext.replace('{{Blockedtroll}}', '{{tl|Blockedtroll}}')
		newtext = newtext.replace('{{Indefblockeduser-big}}', '{{tl|Indefblockeduser-big}}')
		newtext = newtext.replace('{{Indefblockeduser}}', '{{tl|Indefblockeduser}}')
		newtext = newtext.replace('{{Indefblockuser}}', '{{tl|Indefblockuser}}')
		newtext = newtext.replace('{{Indefblock}}', '{{tl|Indefblock}}')
		newtext = newtext.replace('{{Indefblocked}}', '{{tl|Indefblocked}}')
		newtext = newtext.replace('{{Indef}}', '{{tl|Indef}}')
		newtext = newtext.replace('{{IndefBlocked}}', '{{tl|IndefBlocked}}')
		newtext = newtext.replace('{{Vpblock}}', '{{tl|Vpblock}}')
		newtext = newtext.replace('{{Pagemovevandal}}', '{{tl|Pagemovevandal}}')
		newtext = newtext.replace('{{Pageblankvandal}}', '{{tl|Pageblankvandal}}')
		newtext = newtext.replace('{{Blockedindef}}', '{{tl|Blockedindef}}')
		newtext = newtext.replace('{{Idb}}', '{{tl|Idb}}')
		newtext = newtext.replace('{{Userindef}}', '{{tl|userindef}}')
		newtext = newtext.replace('{{VOAblock}}', '{{tl|VOAblock}}')
		
		newtext = newtext.replace('{{temporary userpage}}', '')
		newtext = newtext.replace('{{blockedimpersonator}}', '{{tl|Indefblockeduser}}')
		newtext = newtext.replace('{{blockedtroll}}', '{{tl|Blockedtroll}}')
		newtext = newtext.replace('{{indefblockeduser-big}}', '{{tl|Indefblockeduser-big}}')
		newtext = newtext.replace('{{indefblockeduser}}', '{{tl|Indefblockeduser}}')
		newtext = newtext.replace('{{indefblockuser}}', '{{tl|Indefblockuser}}')
		newtext = newtext.replace('{{indefblock}}', '{{tl|Indefblock}}')
		newtext = newtext.replace('{{indefblocked}}', '{{tl|Indefblocked}}')
		newtext = newtext.replace('{{indef}}', '{{tl|Indef}}')
		newtext = newtext.replace('{{indefBlocked}}', '{{tl|IndefBlocked}}')
		newtext = newtext.replace('{{vpblock}}', '{{tl|Vpblock}}')
		newtext = newtext.replace('{{pagemovevandal}}', '{{tl|Pagemovevandal}}')
		newtext = newtext.replace('{{pageblankvandal}}', '{{tl|Pageblankvandal}}')
		newtext = newtext.replace('{{blockedindef}}', '{{tl|Blockedindef}}')
		newtext = newtext.replace('{{idb}}', '{{tl|Idb}}')
		newtext = newtext.replace('{{userindef}}', '{tl|{userindef}}')
		newtext = newtext.replace('{{vOAblock}}', '{{tl|VOAblock}}')
	
	if not(newtext == text):
		try:
			userpage.edit(newtext=newtext, summary="Removing Temporary userpage category", minor=True, bot=True, basetime=userpage.lastedittime)
			l = codecs.open('LogFile.txt', 'ab', 'utf-8')
			l.write('\n# [[' + userpage.title + ']] - ' + reason)
			l.close()
		except api.APIError, (code, errortext):
			if code == 'protectedpage':
				reportError(userpage, "Page protected")
			else:
				reportError(userpage, errortext)
	else:
		reportError(userpage, "No change detected")

def reportError(userpage, error):
	g = codecs.open('ErrorFile.txt','ab', 'utf-8')
	g.write('\n# [['+userpage.title+']] ' + error)
	print( "ERROR on: " + userpage.pageid)
	g.close() 
		
if __name__ == '__main__':
	main()