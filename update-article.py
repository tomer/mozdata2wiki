#!/usr/bin/python
# -*- coding: utf-8 -*-
	
from mwbot import wikiConnector

w = wikiConnector()
w.sync_files_to_wiki('out/', r'^.*\.wiki(\..*)?$')
