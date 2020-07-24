import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QSystemTrayIcon, QFileDialog, QTextEdit, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QCursor, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer
import ctypes
import tweepy
from textblob import TextBlob
import re
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import pandas as pd
import random

stopwords=set(STOPWORDS)

auth=tweepy.AppAuthHandler('Qj6SB75GU9WMhfAQ7E0NDW0FL','172iv4lhR2WgbhwphJTDdgYigeicI3p7Czk2OZVsOR42wse7zg')
api=tweepy.API(auth)

class TSA:
   def __init__(self):
      self.w=QWidget()
      self.w.setFixedSize(640,480)
      self.w.setWindowTitle("Tweets Sentiment Analyzer")
      self.l=QLabel(self.w)
      self.l.setGeometry(0,462,640,18)
      self.l.setText('  Ready!')

   def splashScreen(self):
      img = QLabel(self.w)
      img.setGeometry(0,0,640,480)
      pixmap = QPixmap('SplashScreen.png')
      img.setPixmap(pixmap.scaled(640,480,Qt.KeepAspectRatio))
      QTimer.singleShot(4000, img.hide)

   def mainScreen(self):
      viaAPI=QPushButton(self.w)
      viaAPI.setText('Fetch Tweets via Twitter API')
      viaAPI.move(225,165)
      viaAPI.setCursor(QCursor(Qt.PointingHandCursor))
      viaAPI.clicked.connect(self.twitterAPI)

      viaDataset=QPushButton(self.w)
      viaDataset.setText('Fetch Tweets from Local Dataset')
      viaDataset.move(225,225)
      viaDataset.setCursor(QCursor(Qt.PointingHandCursor))
      viaDataset.clicked.connect(self.localDataset)

      tweetAnalyze=QPushButton(self.w)
      tweetAnalyze.setText('Analyze Handpicked Tweet')
      tweetAnalyze.move(225,285)
      tweetAnalyze.setCursor(QCursor(Qt.PointingHandCursor))
      tweetAnalyze.clicked.connect(self.analyzeText)

   def twitterAPI(self):
         self.tapi=QWidget()
         self.tapi.move(355,75)
         self.tapi.setFixedSize(640,480)
         self.tapi.setWindowTitle("Fetch Tweets via Twitter API")

         self.multitweet=QPushButton(self.tapi)
         self.multitweet.setText('Analyze Multiple Tweets')
         self.multitweet.move(225,195)
         self.multitweet.setCursor(QCursor(Qt.PointingHandCursor))
         self.multitweet.clicked.connect(self.fetchviaAPI)

         self.singletweet=QPushButton(self.tapi)
         self.singletweet.setText('Pick a Random Tweet')
         self.singletweet.move(225,255)
         self.singletweet.setCursor(QCursor(Qt.PointingHandCursor))
         self.singletweet.clicked.connect(self.fetchviaAPIsingle)

         self.tapi.show()

   def localDataset(self):
         self.locds=QWidget()
         self.locds.move(355,75)
         self.locds.setFixedSize(640,480)
         self.locds.setWindowTitle("Fetch Tweets from Local Dataset")

         self.multitweet=QPushButton(self.locds)
         self.multitweet.setText('Analyze Multiple Tweets')
         self.multitweet.move(225,195)
         self.multitweet.setCursor(QCursor(Qt.PointingHandCursor))
         self.multitweet.clicked.connect(self.fetchvialocal)

         self.singletweet=QPushButton(self.locds)
         self.singletweet.setText('Pick a Random Tweet')
         self.singletweet.move(225,255)
         self.singletweet.setCursor(QCursor(Qt.PointingHandCursor))
         self.singletweet.clicked.connect(self.viaDSetsingleProcess)

         self.locds.show()

   def showSingleAnalysis(self,tweet):
      cleaned_tweet=re.sub('[^a-zA-Z]',' ',tweet)
      self.tweetanalysis=QWidget()
      self.tweetanalysis.move(480,160)
      self.tweetanalysis.setFixedSize(400,300)
      self.tweetanalysis.setWindowTitle("Tweet Analysis")

      fileP=open('positive_words.txt','r')
      pos_words=fileP.readlines()
      pos_words=set([word[0:-1] for word in pos_words])

      fileP=open('negative_words.txt','r')
      neg_words=fileP.readlines()
      neg_words=set([word[0:-1] for word in neg_words])

      self.boxlabel=QLabel(self.tweetanalysis)
      self.boxlabel.move(20,20)
      self.boxlabel.setText('Tweet Text')

      self.boxlabel.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            }
        """)
      self.text=QTextEdit(self.tweetanalysis)
      self.text.setGeometry(20,50,360,120)

      self.words=tweet.split()
      for i in self.words:
         if i.lower() in pos_words:
            self.text.setTextColor(QColor(0,255,0))
            self.text.insertPlainText(i+' ')
         elif i in neg_words:
            self.text.setTextColor(QColor(255,0,0))
            self.text.insertPlainText(i+' ')
         else:
            self.text.setTextColor(QColor(0,0,0))
            self.text.insertPlainText(i+' ')

      self.singletest=TextBlob(cleaned_tweet)
      self.polarity=self.singletest.sentiment.polarity
      self.pos_prob=int(50+(self.polarity*100))
      self.neg_prob=100-self.pos_prob

      if self.pos_prob>100:
         self.pos_prob=100
         self.neg_prob=0
      elif self.pos_prob<0:
         self.pos_prob=0
         self.neg_prob=100

      self.postw=QLabel(self.tweetanalysis)
      self.postw.move(60,200)
      self.postw.setText('Positive Probability : '+str(self.pos_prob)+' %')
      self.postw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.negtw=QLabel(self.tweetanalysis)
      self.negtw.move(60,240)
      self.negtw.setText('Negative Probability : '+str(self.neg_prob)+' %')
      self.negtw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.tweetanalysis.show()

   def viaAPIsingleProcess(self):
      self.tweets=api.search(q=self.key.text() ,count=1,lang='en',tweet_mode='extended')
      self.tweet=self.tweets[0].full_text
      self.l.setText('  Random Tweet loaded via Twitter API!')
      self.showSingleAnalysis(self.tweet)

   def viaDSetsingleProcess(self):
      self.fileloc = QFileDialog.getOpenFileName(self.locds,"Select a compatible CSV file",filter="CSV File (*.csv)")
      if self.fileloc[0]=='':
         self.l.setText('  File not chosen!')
      else:
         self.tweetsdf=pd.read_csv(self.fileloc[0])
         self.tweetsdf=self.tweetsdf[self.tweetsdf['lang']=='en']
         self.tweet=random.sample(list(self.tweetsdf['text'].values),1)
         self.l.setText('  Random Tweet loaded from Dataset!')
         self.showSingleAnalysis(self.tweet[0])

   def fetchviaAPIsingle(self):
      self.fetchAPI=QWidget()
      self.fetchAPI.move(480 ,160)
      self.fetchAPI.setFixedSize(400,300)
      self.fetchAPI.setWindowTitle("Fetch via Twitter API")

      self.label1=QLabel(self.fetchAPI)
      self.label1.move(20,70)
      self.label1.setText('Keywords')
      self.label1.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            }
        """)

      self.key=QLineEdit(self.fetchAPI)
      self.key.setGeometry(20,100,360,20)
      self.key.setPlaceholderText('Keywords to be present in the tweet...')

      self.fetchbtn=QPushButton(self.fetchAPI)
      self.fetchbtn.setText('Fetch')
      self.fetchbtn.move(100,200)
      self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
      self.fetchbtn.clicked.connect(self.viaAPIsingleProcess)

      self.fetchAPI.show()

   def selectfromdataset(self):
      self.twcount=int(self.localcount.text())
      self.localtweetslist=random.sample(list(self.tweetsdf['text'].values),self.twcount)
      self.analysis_info=[]
      self.poscount=0
      self.negcount=0
      self.neutralcount=0
      for i in self.localtweetslist:
         self.analysis=TextBlob(re.sub('[^a-zA-Z]',' ',i))
         if self.analysis.sentiment.polarity>0:
            self.poscount+=1
            self.analysis_info.append(1)
         elif self.analysis.sentiment.polarity<0:
            self.negcount+=1
            self.analysis_info.append(-1)
         else:
            self.neutralcount+=1
            self.analysis_info.append(0)


      self.l.setText('  '+str(self.twcount)+' tweets fetched from Local Dataset!')

      self.twanalysis=QWidget()
      self.twanalysis.move(480,160)
      self.twanalysis.setFixedSize(400,300)
      self.twanalysis.setWindowTitle("Analysis")

      self.postw=QLabel(self.twanalysis)
      self.postw.move(40,20)
      self.postw.setText('Positive Tweets : '+str(self.poscount)+'  ( {:.2f}'.format((self.poscount/self.twcount)*100)+' % )')
      self.postw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.negtw=QLabel(self.twanalysis)
      self.negtw.move(40,55)
      self.negtw.setText('Negative Tweets : '+str(self.negcount)+'  ( {:.2f}'.format((self.negcount/self.twcount)*100)+' % )')
      self.negtw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.neutw=QLabel(self.twanalysis)
      self.neutw.move(40,90)
      self.neutw.setText('Neutral Tweets : '+str(self.neutralcount)+'  ( {:.2f}'.format((self.neutralcount/self.twcount)*100)+' % )')
      self.neutw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.fetchbtn=QPushButton(self.twanalysis)
      self.fetchbtn.setText('Word Cloud')
      self.fetchbtn.move(100,150)
      self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
      self.fetchbtn.clicked.connect(lambda:self.wrdcloud(self.localtweetslist,self.analysis_info))
      
      self.fetchbtn=QPushButton(self.twanalysis)
      self.fetchbtn.setText('Show Tweets')
      self.fetchbtn.move(100,220)
      self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
      self.fetchbtn.clicked.connect(lambda:self.showtweetlist(self.localtweetslist,self.analysis_info))

      self.twanalysis.show()


         
   def fetchvialocal(self):
      self.fileloc = QFileDialog.getOpenFileName(self.locds,"Select a compatible CSV file",filter="CSV File (*.csv)")
      if self.fileloc[0]=='':
         self.l.setText('  File not chosen!')
      else:
         self.tweetsdf=pd.read_csv(self.fileloc[0])
         self.tweetsdf=self.tweetsdf[self.tweetsdf['lang']=='en']
         self.l.setText('  Dataset loaded!')
         self.fetchviadataset=QWidget()
         self.fetchviadataset.move(480 ,160)
         self.fetchviadataset.setFixedSize(400,300)
         self.fetchviadataset.setWindowTitle("Fetch via Twitter API")

         self.label4=QLabel(self.fetchviadataset)
         self.label4.move(20,90)
         self.label4.setText('Count')
         self.label4.setStyleSheet("""
         QLabel {
               color: white;
               background-color: #27b0da;
               font-weight: bold;
               }
         """)

         self.localcount=QLineEdit(self.fetchviadataset)
         self.localcount.setGeometry(20,120,360,20)
         self.localcount.setPlaceholderText('Number of tweets to fetch - Max Limit : 10000')
         
         self.fetchbtn=QPushButton(self.fetchviadataset)
         self.fetchbtn.setText('Fetch')
         self.fetchbtn.move(100,200)
         self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
         self.fetchbtn.clicked.connect(self.selectfromdataset)

         self.fetchviadataset.show()




   def fetchviaAPI(self):
      self.fetchAPI=QWidget()
      self.fetchAPI.move(480 ,160)
      self.fetchAPI.setFixedSize(400,300)
      self.fetchAPI.setWindowTitle("Fetch via Twitter API")

      self.label1=QLabel(self.fetchAPI)
      self.label1.move(20,20)
      self.label1.setText('Keywords')
      self.label1.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            }
        """)

      self.key=QLineEdit(self.fetchAPI)
      self.key.setGeometry(20,50,360,20)
      self.key.setPlaceholderText('Keywords to be present in the tweet...')

      self.label2=QLabel(self.fetchAPI)
      self.label2.move(20,90)
      self.label2.setText('Count')
      self.label2.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            }
        """)

      self.count=QLineEdit(self.fetchAPI)
      self.count.setGeometry(20,120,360,20)
      self.count.setPlaceholderText('Number of tweets to fetch - Max Limit : 100')
      
      self.fetchbtn=QPushButton(self.fetchAPI)
      self.fetchbtn.setText('Fetch')
      self.fetchbtn.move(100,200)
      self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
      self.fetchbtn.clicked.connect(self.fetchtweets)

      self.fetchAPI.show()

   def ovcld(self,tweets):
      self.tw=[re.sub('[^a-zA-Z]', ' ', i).split() for i in tweets]
      for i in self.tw:
         while 'RT' in i:
            i.remove('RT')

      self.twrds=''
      for i in self.tw:
         for j in i:
            self.twrds+=j+' '

      self.ovwrdcld=WordCloud(stopwords=stopwords,background_color='white',width=800,height=800).generate(self.twrds)
      
      plt.figure(figsize=(8,6),num='Overall Words Cloud')
      plt.imshow(self.ovwrdcld)
      plt.axis('off')
      plt.show()

   def poscld(self,tweets,analysis):
      fileP=open('positive_words.txt','r')
      pos_words=fileP.readlines()
      pos_words=set([word[0:-1] for word in pos_words])

      self.poslist=[]
      self.tw=[re.sub('[^a-zA-Z]', ' ', i).split() for i in tweets]
      for i in self.tw:
         for j in i:
            if j in pos_words:
               self.poslist.append(j)

      self.poswrds=''
      for i in self.poslist:
         self.poswrds+=i+' '

      self.poswrdcld=WordCloud(stopwords=stopwords,background_color='white',width=800,height=800).generate(self.poswrds)
      
      plt.figure(figsize=(8,6),num='Positive Words Cloud')
      plt.imshow(self.poswrdcld)
      plt.axis('off')
      plt.show()

   def negcld(self,tweets,analysis):
      fileN=open('negative_words.txt','r')
      neg_words=fileN.readlines()
      neg_words=set([word[0:-1] for word in neg_words])

      self.neglist=[]
      self.tw=[re.sub('[^a-zA-Z]', ' ', i).split() for i in tweets]
      for i in self.tw:
         for j in i:
            if j in neg_words:
               self.neglist.append(j)

      self.negwrds=''
      for i in self.neglist:
         self.negwrds+=i+' '

      self.negwrdcld=WordCloud(stopwords=stopwords,background_color='white',width=800,height=800).generate(self.negwrds)
      
      plt.figure(figsize=(8,6),num='Negative Words Cloud')
      plt.imshow(self.negwrdcld)
      plt.axis('off')
      plt.show()

   def wrdcloud(self,tweets,analysis):
      self.wrdcldwin=QWidget()
      self.wrdcldwin.move(480,160)
      self.wrdcldwin.setFixedSize(400,300)
      self.wrdcldwin.setWindowTitle("Wordcloud")

      self.ovclick=QPushButton(self.wrdcldwin)
      self.ovclick.setText('All Words')
      self.ovclick.move(100,55)
      self.ovclick.setCursor(QCursor(Qt.PointingHandCursor))
      self.ovclick.clicked.connect(lambda:self.ovcld(tweets))

      self.posclick=QPushButton(self.wrdcldwin)
      self.posclick.setText('Positive Word')
      self.posclick.move(100,125)
      self.posclick.setCursor(QCursor(Qt.PointingHandCursor))
      self.posclick.clicked.connect(lambda:self.poscld(tweets,analysis))

      self.negclick=QPushButton(self.wrdcldwin)
      self.negclick.setText('Negative Words')
      self.negclick.move(100,195)
      self.negclick.setCursor(QCursor(Qt.PointingHandCursor))
      self.negclick.clicked.connect(lambda:self.negcld(tweets,analysis))

      self.wrdcldwin.show()

   def showtweetlist(self,tweets,analysis):
      self.tweetwin=QWidget()
      self.tweetwin.move(175,50)
      self.tweetwin.setFixedSize(1024,600)
      self.tweetwin.setWindowTitle("Tweets")

      self.tweetslist=QTableWidget(self.tweetwin)
      self.tweetslist.resize(1024,600)
      self.tweetslist.setRowCount(len(tweets))
      self.tweetslist.setColumnCount(2)

      self.tweetslist.setHorizontalHeaderLabels(['Tweet Text','Sentiment'])

      header = self.tweetslist.horizontalHeader()       
      header.setSectionResizeMode(0, QHeaderView.Stretch)
      header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

      for i in range(len(tweets)):
         self.tweetslist.setItem(i,0,QTableWidgetItem(tweets[i]))
         if analysis[i]==1:
            self.tweetslist.setItem(i,1,QTableWidgetItem('Positive'))
         elif analysis[i]==-1:
            self.tweetslist.setItem(i,1,QTableWidgetItem('Negative'))
         else:
            self.tweetslist.setItem(i,1,QTableWidgetItem('Neutral'))

      self.tweetwin.show()
      
   def fetchtweets(self):
      self.l.setText('Fetching Tweets...')
      self.keywrd=self.key.text()
      self.twcount=int(self.count.text())
      self.tweets=api.search(q=self.keywrd ,count=self.twcount,lang='en',tweet_mode='extended')
      self.tweets=[tweet.full_text for tweet in self.tweets]
      self.analysis_info=[]
      self.poscount=0
      self.negcount=0
      self.neutralcount=0
      for i in self.tweets:
         self.analysis=TextBlob(re.sub('[^a-zA-Z]',' ',i))
         if self.analysis.sentiment.polarity>0:
            self.poscount+=1
            self.analysis_info.append(1)
         elif self.analysis.sentiment.polarity<0:
            self.negcount+=1
            self.analysis_info.append(-1)
         else:
            self.neutralcount+=1
            self.analysis_info.append(0)


      self.l.setText('  '+str(self.twcount)+' tweets fetched from Twitter API!')

      self.twanalysis=QWidget()
      self.twanalysis.move(480,160)
      self.twanalysis.setFixedSize(400,300)
      self.twanalysis.setWindowTitle("Analysis")

      self.postw=QLabel(self.twanalysis)
      self.postw.move(40,20)
      self.postw.setText('Positive Tweets : '+str(self.poscount)+'  ( {:.2f}'.format((self.poscount/self.twcount)*100)+' % )')
      self.postw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.negtw=QLabel(self.twanalysis)
      self.negtw.move(40,55)
      self.negtw.setText('Negative Tweets : '+str(self.negcount)+'  ( {:.2f}'.format((self.negcount/self.twcount)*100)+' % )')
      self.negtw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.neutw=QLabel(self.twanalysis)
      self.neutw.move(40,90)
      self.neutw.setText('Neutral Tweets : '+str(self.neutralcount)+'  ( {:.2f}'.format((self.neutralcount/self.twcount)*100)+' % )')
      self.neutw.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            font-size: 20px;
            }
        """)

      self.fetchbtn=QPushButton(self.twanalysis)
      self.fetchbtn.setText('Word Cloud')
      self.fetchbtn.move(100,150)
      self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
      self.fetchbtn.clicked.connect(lambda:self.wrdcloud(self.tweets,self.analysis_info))
      
      self.fetchbtn=QPushButton(self.twanalysis)
      self.fetchbtn.setText('Show Tweets')
      self.fetchbtn.move(100,220)
      self.fetchbtn.setCursor(QCursor(Qt.PointingHandCursor))
      self.fetchbtn.clicked.connect(lambda:self.showtweetlist(self.tweets,self.analysis_info))

      self.twanalysis.show()

   def analyzeText(self):
      self.tweettext=QWidget()
      self.tweettext.move(480,160)
      self.tweettext.setFixedSize(400,300)
      self.tweettext.setWindowTitle("Analyze Handpicked Tweet")

      self.boxlabel=QLabel(self.tweettext)
      self.boxlabel.move(20,20)
      self.boxlabel.setText('Tweet Text')

      self.boxlabel.setStyleSheet("""
        QLabel {
            color: white;
            background-color: #27b0da;
            font-weight: bold;
            }
        """)

      self.twtext=QTextEdit(self.tweettext)
      self.twtext.setGeometry(20,50,360,100)
      self.twtext.setPlaceholderText('Put your chosen tweet here...')

      self.analyze=QPushButton(self.tweettext)
      self.analyze.setText('Analyze')
      self.analyze.move(100,200)
      self.analyze.setCursor(QCursor(Qt.PointingHandCursor))
      self.analyze.clicked.connect(lambda:self.showSingleAnalysis(self.twtext.toPlainText()))

      self.tweettext.show()

   def run(self):
      self.mainScreen()
      self.splashScreen()
      self.w.show()
      sys.exit(app.exec_())
	
if __name__ == '__main__':
   myappid = 'neeraj.tweets.sentimentanalyzer'
   ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
   app = QApplication([])
   app.setStyleSheet(open('StyleSheet.css').read())
   app.setWindowIcon(QIcon('icon.png'))
   instance=TSA()
   instance.run()