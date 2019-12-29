########################################################################################################
###    This script scrapes Investopedia pages using beautiful soup library and lists out the         ###
###       top 10 investment banks in the world (as selected by Investopedia website).                ###
########################################################################################################

from bs4 import BeautifulSoup
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context #to bypass ssl related authentication

#url = input("Enter URL: ")
url='https://www.investopedia.com/articles/investing/111114/worlds-top-10-investment-banks.asp'
html=urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup('strong')
Top_Bank_List = [tag.text.split('(')[0].strip() for tag in tags]
del Top_Bank_List[-1] ## To delte the last bank name as it was repetitive
