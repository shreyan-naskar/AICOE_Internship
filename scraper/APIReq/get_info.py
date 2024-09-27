import requests
from datetime import datetime, timedelta

# 1. get_post_ids
# 2. get_post_date
# 3. get_facebook_post_caption
# 4. get_comment_count
# 5. get_comments
# 6. get_all_comments
# 7. get_n_comments
# 8. get_all_replies
# 9. get_replies
# 10. hide_comment
# 11. delete_comment
# 12. get_reaction_counts
# 13. get_post_ids_within_dates
# 14. get_comment_count



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
    
# Function to get post-ids within dates
def get_post_ids_within_dates(PAGE_ID, ACCESS_TOKEN, start_date, end_date, version = 20.0):
    # Convert to Unix timestamp (optional step, can be directly passed as 'YYYY-MM-DD')
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    # Add 1 day as post-ids are scraped till midnight day before end date
    end_timestamp = int((datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).timestamp())

    # Facebook Graph API URL for fetching posts
    url = f"https://graph.facebook.com/v{version}/{PAGE_ID}/posts"

    # Parameters including the access token, date range, and fields (e.g., post ID)
    params = {
        'access_token': ACCESS_TOKEN,
        'since': start_timestamp,
        'until': end_timestamp,
        'fields': 'id,created_time,message'
    }

    # Send GET request to Facebook Graph API
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        posts = data.get('data', [])
        
        # for post in posts:
        #     post_id = post['id']
            # created_time = post['created_time']
            # message = post.get('message', 'No message')
            # print(f"Post ID: {post_id}, Created Time: {created_time}, Message: {message}")
        return [post['id'] for post in posts]
    else:
        print(f"Failed to retrieve posts. Error: {response.status_code} - {response.text}")

# Function to get date of facebook post
def get_post_date(POST_ID, access_token, version = 20.0):
    url = f"https://graph.facebook.com/v{version}/{POST_ID}"
    params = {
        'fields': 'created_time',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('created_time', 'Date not found')
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to get captions of posts
def get_facebook_post_caption(POST_ID, access_token, version = 20.0):
    """
    Get the caption (message) of a Facebook post using the Graph API.

    :param post_id: ID of the Facebook post.
    :param access_token: Facebook Graph API access token.
    :return: The caption (message) of the post.
    """
    base_url = f"https://graph.facebook.com/v{version}/{POST_ID}"
    params = {
        'access_token': access_token,
        'fields': 'message'  # Specify that we want to retrieve the message field (caption)
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        post_data = response.json()
        caption = post_data.get('message', 'No caption available')
        return caption
    else:
        print(f"Failed to retrieve post: {response.status_code}")
        return None
    
# Function to get count of comments on a facebook post
def get_comment_count(POST_ID, ACCESS_TOKEN, version = 20.0):
    # Facebook Graph API URL to get the number of comments on the post
    url = f"https://graph.facebook.com/v{version}/{POST_ID}"

    # Parameters: access token and fields, including comments summary
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'comments.summary(true)'
    }

    # Send GET request to Facebook Graph API
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        comments_summary = data.get('comments', {}).get('summary', {})
        total_comments = comments_summary.get('total_count', 0)
        
        return total_comments
    else:
        # print(f"Failed to retrieve comments. Error: {response.status_code} - {response.text}")
        return 0

# Function to get comments
def get_comments(access_token, POST_ID, version = 20.0):
    params = {
        'access_token': access_token,
        'summary': 'true',
        'limit': 100,  # Number of comments to fetch per request (max 100)
        'order': 'reverse_chronological'
    }
    GRAPH_API_URL = f'https://graph.facebook.com/v{version}/{POST_ID}/comments'
    response = requests.get(GRAPH_API_URL, params=params)
    if response.status_code == 200:
        data =  response.json()
        return data.get('data', [])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
# Get all comments
def get_all_comments(access_token, POST_ID, version = 20.0):
    comments = []
    url = f'https://graph.facebook.com/v{version}/{POST_ID}/comments'
    while url:
        params = {
            'access_token': access_token,
            'limit': 100,  # Maximum number of comments/replies per request
            'order': 'reverse_chronological'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            comments.extend(data.get('data', []))
            url = data.get('paging', {}).get('next')  # Get the next page URL
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            url = None  # Stop the loop if an error occurs
    return comments

def get_n_comments(post_id, access_token, n, version = 20.0):
    url = f"https://graph.facebook.com/v{version}/{post_id}/comments"
    comments = []
    limit = 100  # Maximum allowed limit
    
    params = {
        'fields': 'from,message,created_time',
        'access_token': access_token,
        'limit': limit,
        'order': 'reverse_chronological'
    }
    
    while url and len(comments) < n:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            
            # Append comments to the list
            comments.extend(data)
            
            # Check if we've reached the desired count
            if len(comments) >= n:
                break
            
            # Get the next page of comments, if available
            paging = response.json().get('paging', {})
            url = paging.get('next', None)  # Update URL to the next page, or None if no more pages
        # else:
        #     print(f"Error: {response.status_code}")
        #     print(response.text)
            return None
    
    # Trim the comments to the exact count needed (if more were retrieved due to pagination)
    return comments[:n]

# Get all replies
def get_all_replies(access_token,COMMENT_ID, version = 20.0):
    url = f'https://graph.facebook.com/v{version}/{COMMENT_ID}/comments'
    replies = []
    while url:
        params = {
            'access_token': access_token,
            'limit': 100,  # Maximum number of comments/replies per request
            'order': 'reverse_chronological'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            replies.extend(data.get('data', []))
            url = data.get('paging', {}).get('next')  # Get the next page URL
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            url = None  # Stop the loop if an error occurs
    return replies

# Function to get replies for a specific comment
def get_replies(access_token, COMMENT_ID, version = 20.0):

    url = f'https://graph.facebook.com/v{version}/{COMMENT_ID}/comments'
    params = {
        'access_token': access_token,
        'summary': 'true',
        'limit': 100,  # Number of replies to fetch per request (max 100)
        'order': 'reverse_chronological'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching replies: {response.status_code}")
        print(response.text)
        return None

# Function to hide comments
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
    
# Function to delete comment
def delete_comment(comment_id, access_token, version = 20.0):
    url = f"https://graph.facebook.com/v18.0/{comment_id}"
    params = {
        'access_token': access_token
    }
    
    response = requests.delete(url, params=params)
    if response.status_code == 200:
        return "Comment deleted successfully."
    else:
        return f"Error: {response.status_code}, {response.text}"
    
# Function to get reaction counts of posts
def get_reaction_counts(POST_ID, access_token, version = 20.0):
    url = f"https://graph.facebook.com/v{version}/{POST_ID}"
    params = {
        'fields': 'reactions.summary(true)',
        'access_token': access_token
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        total_reactions = data.get('reactions', {}).get('summary', {}).get('total_count', 0)
        return total_reactions
    else:
        return f"Error: {response.status_code}, {response.text}"
