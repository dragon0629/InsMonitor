from urllib import request
from bs4 import BeautifulSoup
import time
import os
import re
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import datetime
import requests
import json
from cqsdk import CQBot, CQAt, CQImage, RcvdPrivateMessage, SendPrivateMessage, RcvdGroupMessage, SendGroupMessage, GetGroupMemberList, RcvGroupMemberList, SendPrivateMessage

urlINS = 'https://www.instagram.com/whitehairpin/'
qqgroup = 637995665
qqtest = 1691686998
def getIns(url):
	proxy = '127.0.0.1:8118'
	proxies = {
    	'http': 'http://' + proxy,
    	'https': 'https://' + proxy
	}
	try:
		r = requests.get(url,proxies=proxies)
		raw_text = r.text
		soup = BeautifulSoup(raw_text,"html.parser")
		dr = re.compile(r'<[^>]+>',re.S) 
		data = dr.sub('',soup.text) 
		data = data.split('window._sharedData = ',1)[1]
		data = data.split(';\n\n',1)[0]
		data = json.loads(data)
		data = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
		insTime = data[0]["node"]["taken_at_timestamp"]
		try:
			text = data[0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
		except Exception as e:
			text = ''
		pic = data[0]["node"]["thumbnail_src"]
		count = len(pic) -1
		pic = pic[count]["src"]
		comments = data[0]["node"]["edge_media_to_comment"]["count"]
		like = data[0]["node"]["edge_liked_by"]["count"]
		url = data[0]["node"]["shortcode"]
		url = 'https://www.instagram.com/p/' + url
	except Exception as e:
		insTime = 0
		text = ''
		like = 0
		comments =0
		pic = ''
		url = ''
	return int(insTime),str(text),int(like),int(comments),str(pic),str(url)

qqbot = CQBot(11235)
qqbot.start()
proxy = '127.0.0.1:8118'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}
print('开始获取INS')
dataIns = getIns(urlINS)
Instext = dataIns[0]
Inspicurl = dataIns[1]
print(Inspicurl)
Insweburl = dataIns[2]
insTime = dataIns[0]
print('最新INS时间：' + str(insTime))

while True:
#		if newNum > Num:
#			print('当前热搜条目数：' + str(newNum))
#			qqbot.send(SendGroupMessage(group1,'[热搜通知]李艺彤出现在微博热搜，当前热搜条目数: ' + str(newNum) + '当前最高排名：' + str(newresouRank)))
	try:
		time.sleep(60)
		dataInsNew = getIns(urlINS)
		insTimeNew = dataInsNew[0]
		print('新的INS时间：' + str(insTimeNew))
		if insTimeNew > insTime:
			time_local = time.localtime(insTimeNew)
			insTimeText = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
			text = dataInsNew[1]
			like = dataInsNew[2]
			comments = dataInsNew[3]
			picurl = dataInsNew[4]
			picname = picurl[-50:]
			picpath = 'E:/SNH/CoolQ_Pro/data/image/' + picname
			insUrl = dataInsNew[5]
			print(picname)
			print('最新INS地址：' + insUrl)
			print('最新INS内容：' + text)
			r = requests.get(picurl,proxies=proxies)
			with open(picpath,'wb') as f:
				f.write(r.content)
			print('INS更新！最新地址为: ' + insUrl)
			msgIns = '[李艺彤更新INS]！' +  '\r' + '发送时间：' + insTimeText + '\r'
			print(video)
#			if video == 'True':
#				msgIns += '本次INS内容为视频，请前往观看\r'
			msgIns += '\r' + text + '\r' + '[CQ:image,file='+ picname +']' + '\r' + '当前 ' + str(like) + ' 赞 ' + str(comments) + ' 评论！' + '\r' + insUrl
			qqbot.send(SendGroupMessage(group, msgIns))
			qqbot.send(SendPrivateMessage(qqtest, msgIns))
			insTime = insTimeNew
		else:
			print('INS no change')
	except Exception as e:
		print("error","10s to continue")
		time.sleep(10)