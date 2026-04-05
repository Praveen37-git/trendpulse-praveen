import requests
import json
import time
import os
from datetime import datetime

#making the API call
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
headers = {"User-Agent": "TrendPulse/1.0"}
response = requests.get(url,timeout=10,headers = headers)
#checking the response for the API call
print("Status code:",response.status_code)

#dictionary to get category wise stories based on the keywords
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
    #Using try-except blocks to handle timeouts
    try:
        response = requests.get(url1, timeout=10, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Unexpected status code {response.status_code} for id {story_id}")
            return None
    except requests.RequestException as e:
        print(f"Request failed for id {story_id}: {e}")
        return None


#function to group the news into the respective category
def get_category(title):
    if title is None:
        return None
    #convert the title to string and to lower case to check for matches with the keywords
    title_lower = str(title).lower()
    #Loop through the categories dictionary and the keywords to find the matching words
    for category_name,keywords in categories.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            #condition to check whether the word is present in the title sequence using "in" keyword and return the category name
            if keyword_lower in title_lower:
                return category_name


#retrieve the data from API and slice it to fetch the first 500 stories
data = response.json()
top_ids = data[:500]
all_stories = []
#create a dictionary for counting the stories for each category 
category_count = {"technology": 0,"worldnews": 0,"sports" : 0,"science" : 0,"entertainment" : 0}

#Loop through the top_ids list and fetch the stories for each ids
for i in range(len(top_ids)):
    story = fetch_data(top_ids[i])
    if story is None:
        continue
    #extracting the fields from each story
    post_id = story.get("id")
    title = story.get("title")
    category = get_category(title)
    score = story.get("score",0)
    num_comments = story.get("descendants",0)
    author = story.get("by")
    now = datetime.now()
    collected_at = now.strftime("%Y-%m-%d %H:%M:%S")

    #if there is category skip the current iteration
    if category is None:
        continue
    #condition to check the count of category is 25 and sleep for 2 seconds if it matches
    if category_count[category] == 25:
        print(f"Finished category {category}, sleeping 2 seconds...")
        time.sleep(2)
    #create a dictionary for each story and append it to the all_stories list, also update the category count
    my_dict = {"post_id": post_id,"title" : title,"category": category,"score": score,
                "num_comments": num_comments,"author": author,"collected_at": collected_at}
    all_stories.append(my_dict)
    category_count[category] += 1
    #print the progress of retrieved stories with each category count 
    if sum(category_count.values()) % 10 == 0:
        print(f"processed {i+1}/{len(top_ids)} ids, counts={category_count}")
    #break the loop if all categories have atleast 25 stories
    if all(c >= 25 for c in category_count.values()):
            break


#create a data directory if it doesn't exist 
os.makedirs("data", exist_ok=True)
#save the collected data in a json file with the current date in the filename
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
num_of_stories = len(all_stories)
#write the collected stories to the json file
with open(filename, 'w') as f:
    json.dump(all_stories,f,indent=2)
print("Final category counts: ",category_count)
print(f"Collected {num_of_stories} stories. Saved to {filename}")
