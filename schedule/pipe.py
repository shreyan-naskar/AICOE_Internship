import requests
import pandas
from datetime import datetime, timedelta
import csv
import os
import time
import pandas as pd
import os
from dotenv import load_dotenv
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.chat_models import ChatOpenAI

# get post ids of facebook page
def get_post_ids(PAGE_ID, access_token, version = 20.0, limit = 100):
    """
    Get post IDs from a Facebook page using the Graph API.

    :param page_id: ID or username of the Facebook page.
    :param access_token: Facebook Graph API access token.
    :param limit: Number of posts to retrieve.
    :return: List of post IDs.
    """
    base_url = f"https://graph.facebook.com/v{version}/{PAGE_ID}/posts"
    params = {
        'access_token': access_token,
        'limit': limit  # Number of posts to retrieve
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        posts = response.json().get('data', [])
        post_ids = [post['id'] for post in posts]
        return post_ids
    else:
        print(f"Failed to retrieve posts: {response.status_code}")
        return []
    
def get_comments_from_last_n_minutes(ACCESS_TOKEN, post_id, mins, version=20.0):
    # Calculate the timestamp for the specified number of minutes ago
    n_minutes_ago = int((datetime.now() - timedelta(minutes=mins)).timestamp())

    # Create a dictionary for parameters, including specific fields to fetch
    params = {
        "since": n_minutes_ago,
        "access_token": ACCESS_TOKEN,
        "fields": "id,message,is_hidden,created_time"  # Specify fields to retrieve
    }

    comments_url = f"https://graph.facebook.com/v{version}/{post_id}/comments"
    comments_all = []

    while comments_url:
        response = requests.get(comments_url, params=params)
        if response.status_code == 200:
            data = response.json()
            comments = data.get('data', [])
            # print(comments)
            # Filter comments within the specified minutes
            for comment in comments:
                time = comment['created_time']
                utc_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
                
                # Check if the comment was created within the specified timeframe
                if utc_time.timestamp() >= n_minutes_ago:
                    # Extract relevant comment attributes
                    comment_data = {
                        "id": comment.get('id'),
                        "message": comment.get('message'),
                        "is_hidden": comment.get('is_hidden'),
                        "created_time": comment['created_time']
                    }
                    comments_all.append(comment_data)

            # Get the next page comments_url
            comments_url = data.get('paging', {}).get('next')
            params = {}  # Clear params for pagination as URL already has them
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            comments_url = None  # Stop the loop if an error occurs

    return comments_all

def hide_comment(COMMENT_ID, access_token, version = 20.0):
    url = f"https://graph.facebook.com/v{version}/{COMMENT_ID}"
    params = {
        'is_hidden': 'true',
        'access_token': access_token
    }
    
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return f"{COMMENT_ID} - Comment hidden successfully."
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_comment_intent(comment):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, max_tokens=1000 ,openai_api_key=openai_api_key)
    prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are Kolkata Police Department and find out the intent of the comment. Intent can be Abusive or Offensive, Supportive or Appreciative, Question or Inquiry, Complaint or Dissatisfaction, Suggestion or Feedback, General Conversation. The comments can also be in Bengali. You just say the intent only."),
        ("human", "{comment}")
    ]
)

# Create the combined chain using LangChain Expression Language (LCEL)
    chain = prompt_template | model | StrOutputParser()
    result = chain.invoke({"comment": comment})
    intent = result.strip()
    return intent



#main
file_path = "file-path"
comments_all = []
PAGE_ID = "PAGE_ID"
ACCESS_TOKEN = "ACCESS_TOKEN"
openai_api_key="OPENAI-API-KEY"

post_ids = get_post_ids(PAGE_ID, ACCESS_TOKEN, 20.0, 10)
for post_id in post_ids:

    comments = get_comments_from_last_n_minutes(ACCESS_TOKEN, post_id, mins = 10)
    print(post_id, "New Comments - ", len(comments))
    for comment in comments:
        if comment["is_hidden"] == False:
            comments_all.append([comment["id"], comment["message"]])
        else:
            print("Already Hidden ",comment)

print("\nFINAL unhidden", len(comments_all))

# No new comments in last 10 mins
if not comments_all :
    # nothing to do
    print("No recent comments so Exiting")
    exit(0)

comment_df = pandas.DataFrame(data = comments_all, columns = ["COMMENT_ID", "COMMENT"])
comment_df.to_csv(f"{file_path}recent-comms.csv", index=False)

abusive_comments = []

# Open the CSV file
with open(f'{file_path}recent-comms.csv', mode='r',encoding='utf-8') as file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(file)
    
    # Loop through each row
    for row in csv_reader:
        # Access specific columns
        comment_id = row['COMMENT_ID']
        comment = row['COMMENT']
        intent= get_comment_intent(comment)
        
        if intent=="Abusive or Offensive" :
            print(f"Comment ID: {comment_id}, Comment: {comment}, Intent: {intent}")
            abusive_comments.append({
                'COMMENT_ID': comment_id,
                'COMMENT': comment,
            })
        # Print or process the data
if not abusive_comments :
    # nothing to do
    print("No abusive comments so Exiting")
    exit(0)

if abusive_comments:
    with open(f'{file_path}abusive_comments.csv', mode='w', newline='', encoding='utf-8') as outfile:
        # Define the CSV fieldnames
        fieldnames = ['COMMENT_ID', 'COMMENT']
        
        # Create a CSV writer object
        csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header row
        csv_writer.writeheader()
        
        # Write each abusive comment to the new CSV file
        for abusive_comment in abusive_comments:
            csv_writer.writerow(abusive_comment)

    print("Abusive or offensive comments have been written to 'abusive_comments.csv'.")
    
abusive = pandas.read_csv(f"{file_path}abusive_comments.csv")


file = open(f'{file_path}task.txt', 'a')
for idx, row in abusive.iterrows():
    file.write(f'{datetime.now()} - {row[1]} \n')
    comm_id = row[0]
    hide_comment(comm_id, ACCESS_TOKEN)

file.close()
print("Abusive comments hidden.")