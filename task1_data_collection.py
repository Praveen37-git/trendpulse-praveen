import requests
import json
import time
import os
from datetime import datetime

#making tha API call
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
headers = {"User-Agent": "TrendPulse/1.0"}
response = requests.get(url,timeout=10,headers = headers)
#checking the response for the API call
print("Status code:",response.status_code)

#dictionory to get category wise stories based on the keywords
categories = {"technology":["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
              "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
              "sports" : ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
              "science" : ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
              "entertainment" : ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]}

#function to fetch the top stories details
def fetch_data(story_id):
    base_url = "https://hacker-news.firebaseio.com/v0/item/"
    #building URL string using the id value
    url1 = base_url + str(story_id) + ".json"
    response = requests.get(url1,timeout = 10,headers = headers)
    #check the request status, if it fails, print the response status code
    if(response.status_code == 200):
        return response.json()
    else:
        print(f"Unexpected Status code: {response.status_code}")
        return None

#function to group the news into the respective category
def get_category(title):
    if title == None:
        return None
    #convert the title to string and to lower case to check for matches with the keywords
    title = str(title)
    title_lower = title.lower()
    for category_name,keywords in categories.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title_lower:
                return category_name


#retrieve the data from API and slice it to fetch the first 500 stories
data = response.json()
all_stories = []
category_count = {k:0 for k in categories}
top_ids = data[:500]

#loop over top_ids with counter
for idx, story_id in enumerate(top_ids, 1):
    story = fetch_data(story_id)
    if not story:
        continue
    cat = get_category(story.get("title"))
    if not cat or category_count[cat] >= 25:
        continue
    #extract the fields and append it to all_stories list
    all_stories.append({
      "post_id": story.get("id"),
      "title": story.get("title"),
      "category": cat,
      "score": story.get("score",0),
      "num_comments": story.get("descendants",0),
      "author": story.get("by"),
      "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    category_count[cat] += 1
    #print the progress of retrieved stories with each category count
    if sum(category_count.values()) % 10 == 0:
        print(f"processed {idx}/{len(top_ids)} ids, counts={category_count}")
    #break the loop if all categories have atleast 25 stories
    if all(v >= 25 for v in category_count.values()):
        break
    #wait two seconds between each category
    time.sleep(2)

#create a data directory if it doesn't exist 
os.makedirs("data", exist_ok=True)
#save the collected data in a json file with the current date in the filename
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
num_of_stories = len(all_stories)
#write the collected stories to the json file
with open(filename, 'w') as f:
    json.dump(all_stories,f,indent=2)
print(f"Collected {num_of_stories} stories. Saved to {filename}")