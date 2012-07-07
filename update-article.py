#!/usr/bin/python
# -*- coding: utf-8 -*-

import mwclient
import re, os
import ConfigParser


class wikiConnector:

    def __init__(self):
        self.defaultEditMessage = 'updating article from API'
        config = self.readConfig()
        self.mwhost = config.get('main', 'mwhost')
        self.mwpath = config.get('main', 'mwpath')
        self.mwuser = config.get('main', 'mwuser')
        self.mwpass = config.get('main', 'mwpass')
        
        self.articlesPrefix = 'sandbox/'
        self.login(self.mwhost,self.mwpath,self.mwuser,self.mwpass)
        
    def readConfig(self, configFilename = 'config.ini'):
        config = ConfigParser.RawConfigParser()
        config.read(configFilename)
        return config
        

    def login(self, host = 'en.wikipedia.org', path = '/w/', username ='username', password='password'):
        self.site = mwclient.Site(host, path)
        self.site.login(username, password)
        print ('Logged in to '+ host + path +' as '+ username +'...')

    def read_article(self, articleName):
        page = self.site.Pages[articleName]
        print ('Fetching article '+ articleName +'...')
        return page.edit().encode('utf-8')
                

    def update_article(self, articleName = 'Sandbox', articleText = '', editMessage = 'Updating from API'):
        page = self.site.Pages[articleName]
        print ('Fetching article '+ articleName +'...')
        text = page.edit().encode('utf-8')
        if (text == articleText): print ('Article '+ articleName +' already up-to-date.')
        else: 
            print ('Updating article '+ articleName +'...')
            page.save(articleText, summary = editMessage)
            
    def file_get(self, filename): 
        print ('Fetching local file '+ filename +'...')       
        f = open(filename, 'r')
        fileContent = f.read()
        f.close()
        return fileContent
        
    def sync_file_to_wiki(self, filename, articleName, editMessage = 'Updating from API'):
        fileContent = self.file_get(filename)       
        #self.update_article(articleName, fileContent, editMessage)
    
    def sync_files_to_wiki(self, path = os.getcwd(), matchPattern = r'.*\.wiki', articlePattern = r'^([^\.]*)\..*$', editMessage = 'Updating from API'):
        folderContent = os.listdir(path)
        matchFiles = re.compile (matchPattern)
        articleNaming = re.compile (articlePattern)
        for filename in folderContent:
            if (matchFiles.match(filename)):
                #print ("Match! "+ filename)
                articleName = articleNaming.match(filename+'.').groups()[0]
                self.sync_file_to_wiki(filename, self.articlesPrefix + articleName, editMessage)
            #else: print ("unmatch - "+ filename)
            
            

w = wikiConnector()
w.sync_files_to_wiki('.', r'^.*\.wiki(\..*)?$')
