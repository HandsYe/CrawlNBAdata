#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#==================================
#   user:huiye                    #
#   email:yehuitree@gmail.com     #
#   version:v0.1.0                #
#   time:2019-12-25               #
#==================================

import sys
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

team1 = sys.argv[1] #球队1
team2 = sys.argv[2] #球队2

# 球队字典
teamlist ={'老鹰':'ATL','黄蜂':'CHA','热火':'MIA','魔术':'ORL','奇才':'WAS','公牛':'CHI','骑士':'CLE','活塞':'DET','步行者':'IND','雄鹿':'MIL','篮网':'BKN','凯尔特人':'BOS','尼克斯':'NYK','76人':'PHI','猛龙':'TOR','勇士':'GSW','快船':'LAC','湖人':'LAL','太阳':'PHO','国王':'SAC','掘金':'DEN','森林狼':'MIN','雷霆':'OKC','开拓者':'POR','爵士':'UTA','独行侠':'DAL','火箭':'HOU','灰熊':'MEM','鹈鹕':'NOH','马刺':'SAS'}

#print(teamlist[team1])
#print(teamlist[team2])

response = requests.get("http://www.stat-nba.com/query_team.php?crtcol=date_out&order=1&QueryType=game&Team_id="+teamlist[team1]+"&TOpponent_id="+teamlist[team2]+"&PageNum=10000") #主URL
#print(response.status_code)
#响应状态
if response:
	print('Success!')
else:
	print('An error has occurred.')

soup = BeautifulSoup(response.content,'html.parser') #解析主URL,当前只爬取第一页的内容
urls = [] #待爬取URL集合
for i in soup.find_all(href = re.compile("game/\w+.html"),target="_blank"): #匹配符合条件的标签
	#print(i.string)
	href = re.sub(r'^\.',"",i['href']) #提取标签中href数据并去掉URL开始的点（.）
	urls.append("http://www.stat-nba.com" + href) #每个URL添加到集合

f = open(team1+'_'+team2+'.csv',"w",encoding='utf_8_sig')
f.write("时间,客队,主队,客队得分,主队得分,总分,总分单双,第一节单双,第二节单双,上半场单双,第三节单双,第四节单双\n")
num = 0
for url in urls:
	num += 1
	print(num)
	print(url)
	response = requests.get(url)
	if response:
		print('Success!')
	else:
		print('An error has occurred.')
	
	soup = BeautifulSoup(response.content,'html.parser')
	time = soup.find(text = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})')) #比赛时间
	time = re.sub(r'\s+',"",time) #去掉时间上的空字符
	team = soup.find_all(href = re.compile('/team/'),target="_blank")
	kedui = team[1].string #客队名称
	#print(kedui)
	zhudui = team[3].string #主队名称
	#print(zhudui)
	kedui_score = soup.find_all(class_ ="score")[0].string #客队得分
	zhudui_score = soup.find_all(class_ ="score")[1].string #主队得分
	zongfen = int(kedui_score) + int(zhudui_score) #总分
	#print(zongfen)
	if(zongfen % 2 == 0): #判断总分单双
		zongfendanshuang = "双"
	else:
		zongfendanshuang = "单"
	#print(zongfendanshuang)
	danjiescore = soup.find_all(class_ ="number")
	onescore = int(danjiescore[0].string) + int(danjiescore[4].string) #第一节总得分
	twoscore = int(danjiescore[1].string) + int(danjiescore[5].string) #第二节总得分
	thrscore = int(danjiescore[2].string) + int(danjiescore[6].string) #第三节总得分
	fouscore = int(danjiescore[3].string) + int(danjiescore[7].string) #第四节总得分
	shangbanjiescore = onescore + twoscore
	if(onescore % 2 == 0):
		danshuang1 = "双"
	else:
		danshuang1 = "单"
	if(twoscore % 2 == 0):
		danshuang2 = "双"
	else:
		danshuang2 = "单"
	if(thrscore % 2 == 0):
		danshuang3 = "双"
	else:
		danshuang3 = "单"
	if(fouscore % 2 == 0):
		danshuang4 = "双"
	else:
		danshuang4 = "单"
	if(shangbanjiescore % 2 == 0): #判断上半场单双
		bandanshuang = "双"
	else:
		bandanshuang = "单"
	# 写数据	
	f.write(time+','+kedui+','+zhudui+','+str(kedui_score)+','+str(zhudui_score)+','+str(zongfen)+','+zongfendanshuang+','+danshuang1+','+danshuang2+','+bandanshuang+','+danshuang3+','+danshuang4 + "\n")
f.close()
