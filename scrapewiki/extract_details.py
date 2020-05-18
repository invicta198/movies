"""
Script to extract movies details from wiki pages and store them into 'data.json' file
"""

import bs4
import requests
import json


# Function to extract and dump the data
def start_task():
    # open 'data.json' for reading and writing
    with open(".././data.json", "r+") as f:
        file_data = json.load(f)
        count = 0
        for name in file_data:
            final_data = {}
            print(count)
            # reading 'name' as 'key' and its 'url' as 'value'
            wiki_url = file_data[name]["url"]
            html = None
            movie_detail = {}
            try:
                response = requests.get(wiki_url)
                if response.status_code == 200:
                    html = response.content.decode()
                page = bs4.BeautifulSoup(html, "html.parser")
                try:
                    table = page.find(
                        "table", {"class": "infobox vevent"})
                    details = table.find_all("tr")
                except Exception as e:
                    print("table missing: " + name +
                          "    error: "+str(e))
                    continue
                for data in details:
                    try:
                        data_key = data.find("th").text.replace("\n", "")
                        data_value = data.find("td").text.replace("\n", "")
                        movie_detail[data_key] = data_value
                    except Exception as e:
                        '''print("missing: "+name+
                              "    error: "+str(e))'''
                        continue
                # appending the data
                final_data[name] = movie_detail
                file_data.update(final_data)
                f.seek(0)
                json.dump(file_data, f)
                count += 1
            except Exception as e:
                print("error: ", e)
                continue


if __name__ == '__main__':
    start_task()
