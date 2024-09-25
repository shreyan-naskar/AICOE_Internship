import requests

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
    
import requests

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


# Function to get comments
def get_comments(access_token, POST_ID, version = 20.0):
    params = {
        'access_token': access_token,
        'summary': 'true',
        'limit': 100  # Number of comments to fetch per request (max 100)
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
def get_all_comments(access_token, POST_ID, url, version = 20.0):
    comments = []
    while url:
        params = {
            'access_token': access_token,
            'limit': 100  # Maximum number of comments/replies per request
        }
        
        url = f'https://graph.facebook.com/v{version}/{POST_ID}/comments'
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

# Get all replies
def get_all_replies(access_token,COMMENT_ID, version = 20.0):
    replies = []
    while url:
        params = {
            'access_token': access_token,
            'limit': 100  # Maximum number of comments/replies per request
        }
        
        url = f'https://graph.facebook.com/v{version}/{COMMENT_ID}/comments'
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
        'limit': 100  # Number of replies to fetch per request (max 100)
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