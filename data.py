from googleapiclient.discovery import build
  
api_key = 'AIzaSyB8RLyfOy62Y33JKvcDoVRARQYXu7-DH5k'
import re
import pandas as pd
csv = pd.read_csv('Book1.csv')

name = 1


from html import unescape
import re, string, unicodedata

import urllib.parse as urlparse

def video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

def remove_URL(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", sample)


def video_comments(url, category):
    # empty list for storing reply
    replies = []
    counter = 0
  
    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=url
    ).execute()

    # iterate video response
    while video_response:
        
        # extracting required info
        # from each result object 
        for item in video_response['items']:
            if counter >= 20000:
                break
            counter+=1
            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
              
            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']
  
            # if reply is there
            if replycount>0:
                
                # iterate through all reply
                for reply in item['replies']['comments']:

                    
                    # Extract reply
                    reply = reply['snippet']['textDisplay']
                      
                    # Store reply is list
                    replies.append(reply)
            comment = remove_URL(comment)
         
            # print comment with list of reply
            comment = (unescape(comment)).replace("<br>", " ")
            comment = comment.replace("\n", " ")
            comment = comment.replace("@", " ")
            comment = comment.replace('<a href="', " ")
            file.write(comment+ ", " + category+ "\n")

            for resp in replies:
                if counter >= 20000:
                    break
                counter+=1
                resp = remove_URL(resp)
       

                # print comment with list of replyprint(resp, replies, end = '\n\n')
               
                resp = (unescape(resp)).replace("<br>", " ")
                resp = resp.replace("@", " ")
                resp = resp.replace('<a href="', " ")
                file.write(resp+ ", " + category+ "\n")
            # empty reply list
            replies = []
            
        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    videoId = url
                ).execute()
        else:
            break
  
# Enter video id

  
# Call function
count = 0
temp = 0
for index, row in csv.iterrows():
    s = video_id(row[0])
    print("------------------------")
    print("performing for : ", name)
    print("------------------------")
    file = open(str(name)+".txt", "w")
    try:
        video_comments(s, row[1])
    except Exception as e:
        count += 1
        print(e)
        pass
    name+=1
    file.close()
print(count)
file.close()
