#This script recommends a number of similar movies and books for a given title.
#It also shows IMDB and Rotten tomatoes rating for the movies and the Good read rating for the books.

import requests
import sqlite3
import json
import xml.etree.ElementTree as ET
import ssl
import Credentials as ct # stored the API keys in a separate file and imported it

#Assigning the variable keys to short variables
tk = ct.tastedive_key
ok = ct.omdb_key
gk = ct.good_read_key

########## To avoid the SSL errors during script execution  ##########
ssl._create_default_https_context = ssl._create_unverified_context

# The function below takes a given name and returns the JSON file of all the
# related movies by using TasteDive API
def get_movie_from_tastedive(st):
    baseurl = "https://tastedive.com/api/similar"
    dict = {}
    dict["q"] = st
    dict["type"] = "movies"
    dict["limit"] = input_limit
    dict["k"] = "341908-Movieand-1GNY8H3A"
    #dict["info"] = "1"
    test_dive_res=requests.get(baseurl, params=dict)
    # j=test_dive_res.json()
    # print (json.dumps(j, indent=2))
    return test_dive_res.json()

# The function below takes a given name and returns the JSON file of all the
# related books by using TasteDive API
def get_book_from_tastedive(st):
    baseurl = "https://tastedive.com/api/similar"
    dict = {}
    dict["q"] = st
    dict["type"] = "books"
    dict["limit"] = input_limit
    dict["k"] = tk
    #dict["info"] = "1"
    test_dive_res=requests.get(baseurl, params=dict)
    return test_dive_res.json()

# The function below takes a given name as input and calls  get_movie_from_tastedive function.
# Then it parses the JSON dictionary returned to convert it into a list.
def extract_movie_titles(tl):
    titl_dict = get_movie_from_tastedive(tl)
    title_movie_lst = [nm["Name"] for nm in titl_dict["Similar"]["Results"] if nm["Type"] == "movie"]
    return title_movie_lst

# The function below takes a given name as input and calls  get_book_from_tastedive function.
# Then it parses the JSON dictionary returned to convert it into a list
def extract_book_titles(tl):
    titl_dict = get_book_from_tastedive(tl)
    title_book_lst = [nm["Name"] for nm in titl_dict["Similar"]["Results"] if nm["Type"] == "book"]
    return title_book_lst

# The function below retrieves the JSON dictionary for any movie passed into it using OMDB API
def get_movie_data(title):
    baseurl = f"http://www.omdbapi.com/{ok}"
    dict_input={}
    dict_input["t"] = title
    dict_input["r"] = "json"
    movie_info = requests.get(baseurl, params=dict_input)
    return(movie_info.json())

# The function below parses the JSON dictionary returned by get_movie_data
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
    dict["key"] = gk
    dict["title"] = bn
    goodread_dtl = requests.get(baseurl, params=dict)
    root = ET.fromstring(goodread_dtl.text)
    #print (root[1][18].text) ## An alternative way to access the contents of root
    rating = root.find(".//average_rating").text
    return rating



#Combine everything to give recommendations and ratings of the related movies and books
def get_sorted_recommendations(mv_bk):
    sorted_list=[]
    book_list=[]
    for movie_name in extract_movie_titles(mv_bk):
        m = list(get_movie_rating(movie_name))
        m.append(movie_name)
        sorted_list.append(m)
    mfinal=sorted(sorted_list,key= lambda x:[x[0],x[2],x[1]], reverse=True)

    for book_name in extract_book_titles(mv_bk):
        b = extract_goodread_rating(book_name)
        book_list.append([book_name,b])
    bfinal=sorted(book_list, key = lambda x:[x[1],x[0]], reverse=True)
    return (mfinal, bfinal)


#Make connection and create a Database if it does not exist. Create two tables:
#One to store the Book details and Ratings and the other for Movie details and ratings

def write_to_db(final_movie_list, final_book_list):
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

## The main block of code where all the functions are called from directly / indirectly

if __name__ == '__main__':
    input_name = input("\nEnter the title (Movie or Book Name: Eg: 'Never Let Me Go'): \n")
    input_limit = input("\nEnter the number of books / movies you want to be recomended: \n")
    final_list = get_sorted_recommendations([input_name])
    final_movie_list = final_list[0]
    final_book_list = final_list[1]

    # Call the DB function
    write_to_db(final_movie_list,final_book_list)

    print (f"\n Given Title : {input_name}\n")
    print ("\n***********  Related Books: BOOK NAME, GOOD READ RATING ***************\n")
    print (*final_book_list, sep="\n")
    print ("\n***********  Related Movies: IMDB RATING, ROTTEN TOMATOES RATING, MOVIE NAME ***************\n")
    k = [list(reversed(x)) for x in final_list[0]]
    print (*k,"\n", sep="\n")
