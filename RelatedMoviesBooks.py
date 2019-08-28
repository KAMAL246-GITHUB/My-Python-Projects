#This script recommends a number of similar movies and books for a given name.
#It also shows IMDB and Rotten tomatoes rating for the movies and the Good read rating for the books.
import requests
import sqlite3
import json
import xml.etree.ElementTree as ET
import urllib.request, urllib.parse, urllib.error
import ssl

# To avoid the SSL errors during script execution
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Make connection and create a Database if it does not exist already. Create two tables:
#One to store the Book details and Ratings and the other for Movie details and ratings
conn = sqlite3.connect('movierating.sql')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS RELATED_MOVIES
(GIVEN_NAME CHAR(100), RELATED_MOVIES CHAR(100), IMDB_RATING REAL, ROTTEN_TOMATOES_RATING REAL)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS RELATED_BOOKS
(GIVEN_NAME CHAR(100),RELATED_BOOKS CHAR(100), GOOD_READ_RATING REAL)
''')

# The function below takes a given name and returns the JSON file of all the
# related movies by using TasteDive API
def get_movie_from_tastedive(st):
    baseurl = "https://tastedive.com/api/similar"
    dict = {}
    dict["q"] = st
    dict["type"] = "movies"
    dict["limit"] = "5"
    dict["k"] = "<Your API KEY Goes here>"
    #dict["info"] = "1"
    test_dive_res=requests.get(baseurl, params=dict)
    # j=test_dive_res.json()
    # print (json.dumps(j, indent=2))
    return test_dive_res.json()
#print (get_data_from_tastedive("The Giver"))

# The function below takes a given name and returns the JSON file of all the
# related books by using TasteDive API
def get_book_from_tastedive(st):
    baseurl = "https://tastedive.com/api/similar"
    dict = {}
    dict["q"] = st
    dict["type"] = "books"
    dict["limit"] = "5"
    dict["k"] = "<Your API KEY Goes here>"
    #dict["info"] = "1"
    test_dive_res=requests.get(baseurl, params=dict)
    #j=test_dive_res.json()
    #print (json.dumps(j, indent=2))
    return test_dive_res.json()
#get_book_from_tastedive("Never Let Me Go")

# The function below takes a given name as input and calls  get_movie_from_tastedive function.
# Then it parses the JSON dictionary returned to convert it into a list.
def extract_movie_titles(tl):
    titl_dict = get_movie_from_tastedive(tl)
    title_movie_lst = [nm["Name"] for nm in titl_dict["Similar"]["Results"] if nm["Type"] == "movie"]
    return title_movie_lst
#print (extract_movie_titles("The Giver"))

# The function below takes a given name as input and calls  get_book_from_tastedive function.
# Then it parses the JSON dictionary returned to convert it into a list
def extract_book_titles(tl):
    titl_dict = get_book_from_tastedive(tl)
    title_book_lst = [nm["Name"] for nm in titl_dict["Similar"]["Results"] if nm["Type"] == "book"]
    return title_book_lst
#print (extract_book_titles("Never Let Me Go"))

# The function below retrieves the JSON dictionary for any movie passed into it using OMDB API
def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/?i=tt3896198&apikey=4f0791ba"
    dict_input={}
    dict_input["t"] = title
    dict_input["r"] = "json"
    movie_info = requests.get(baseurl, params=dict_input)
    return(movie_info.json())
#get_movie_data("Venom")

# The function below parses the JSON dictionary retirned by get_movie_data
# and returns a tuple containing IMDB and Rotten tomatoes ratings.

def get_movie_rating(m_name):
    movie_info = get_movie_data(m_name)
    val1 = 0
    val2 = 0
    for info in movie_info['Ratings']:
        if info['Source']=='Internet Movie Database':
            val1 =  info['Value'].split('/')[0]
        if info['Source']=='Rotten Tomatoes':
            val2 =  info['Value']
    val = (val1,val2)
    return val

#The below function returns the good read rating for a given book using Good read API
def extract_goodread_rating(bn):
    baseurl = "https://www.goodreads.com/book/title.xml"
    dict = {}
    #dict["format"] = "xml"
    dict["key"] = "<Your API KEY Goes here>"
    dict["title"] = bn
    goodread_dtl = requests.get(baseurl, params=dict)
    goodread_url = goodread_dtl.url
    req = urllib.request.urlopen(goodread_url, context=ctx).read()
    root = ET.fromstring(req)
    #print (root[1][18].text)
    rating = root.find(".//average_rating").text
    return rating

#print (extract_goodread_rating("One Hundred Years of Solitude"))


#Combine everything to give recommendations and ratings of the related movies and books
def get_sorted_recommendations(mv_bk):
    sorted_list=[]
    book_list=[]
    for movie_name in extract_movie_titles(mv_bk):
        m = list(get_movie_rating(movie_name))
        m.append(movie_name)
        sorted_list.append(m)
    mfinal=sorted(sorted_list,key= lambda x:[x[0],x[2],x[1]], reverse=True)
    #final_sorted_list = [l[0] for l in n]
    for book_name in extract_book_titles(mv_bk):
        b = extract_goodread_rating(book_name)
        book_list.append([book_name,b])
    bfinal=sorted(book_list, key = lambda x:[x[1],x[0]], reverse=True)
    return (mfinal, bfinal)

#print (get_sorted_recommendations("Never Let Me Go"))
#name = input("Enter the name you want to search: ")

final_list = get_sorted_recommendations(["Never Let Me Go"])
final_movie_list = final_list[0]
final_book_list = final_list[1]
# print (*final_book_list, sep="\n")

# Store the data in Data Base table created earlier
for item in final_movie_list:
    cur.execute('''
    insert into RELATED_MOVIES
    (GIVEN_NAME, RELATED_MOVIES, IMDB_RATING, ROTTEN_TOMATOES_RATING)
    VALUES (?,?,?,?)''',
    ("Never Let Me Go", item[2], item[0],item[1]))

for item in final_book_list:
    cur.execute('''
    insert into RELATED_BOOKS
    (GIVEN_NAME, RELATED_BOOKS, GOOD_READ_RATING)
    VALUES (?,?,?)''',
    ("Never Let Me Go",item[0], item[1])
    )
conn.commit()
cur.close()
