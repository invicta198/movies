"""
A python script to add all movies name and its wikipedia url into the database
"""
import bs4
import requests
import pymongo


def mongo_connection():     # Function to esatblish the mongodb connection

    mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mongodb = mongoclient["my_data"]
    mongocol = mongodb["movies"]

    start_task(mongocol)


def start_task(mongocol):   # Function to complete the task

    wiki_url = "https://en.wikipedia.org/wiki/Lists_of_films"
    html = None
    links = []

    try:
        response = requests.get(wiki_url)
        if response.status_code == 200:
            html = response.content.decode()
        page = bs4.BeautifulSoup(html, "html.parser")

        table = page.find("table", {"class": "wikitable"})
        a = table.find_all("a", href=True)

        # links is the 'list', containing wiki pages, which have list of movies
        for i in range(0, 20):
            links.append(""+a[i]['href'])

    except Exception as e:
        print(e)

    try:
        # iteration over the wiki pages
        for link in links:
            per_link = ""+link
            new_url = "https://en.wikipedia.org" + per_link
            response = requests.get(new_url)

            if response.status_code == 200:
                html = response.content.decode()

            page = bs4.BeautifulSoup(html, "html.parser")
            content = page.find_all("div", {"class": "div-col columns column-width"})

            for all_names in content:

                try:
                    # extracting single movie name and link from page
                    names = all_names.find_all("li")
                except Exception as e:
                    continue

                for one_name in names:

                    try:
                        # name stores 'movie name'
                        name = "" + one_name.text
                    except Exception as e:
                        name = "Random_Data"

                    try:
                        # wiki_url stores url to movie
                        wiki_url = "" + "https://en.wikipedia.org" + one_name.a["href"]
                    except Exception as e:
                        wiki_url = "Random_Data"

                    # data to be indexed into the database
                    data = {
                        "name": name,
                        "wiki url": wiki_url
                    }
                    # insert query
                    mongocol.insert_one(data)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    mongo_connection()