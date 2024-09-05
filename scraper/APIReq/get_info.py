import requests

def get_post_ids(page_id, access_token, base_url, limit=100):
    """
    Get post IDs from a Facebook page using the Graph API.

    :param page_id: ID or username of the Facebook page.
    :param access_token: Facebook Graph API access token.
    :param limit: Number of posts to retrieve.
    :return: List of post IDs.
    """
    base_url = base_url.format(PAGE_ID = page_id)
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
    
def get_facebook_post_caption(post_id, access_token, base_url):
    """
    Get the caption (message) of a Facebook post using the Graph API.

    :param post_id: ID of the Facebook post.
    :param access_token: Facebook Graph API access token.
    :return: The caption (message) of the post.
    """
    base_url = base_url.format(POST_ID = post_id)
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
def get_comments(access_token, post_ID, GRAPH_API_URL):
    params = {
        'access_token': access_token,
        'summary': 'true',
        'limit': 100  # Number of comments to fetch per request (max 100)
    }
    GRAPH_API_URL = GRAPH_API_URL.format(POST_ID = post_ID)
    response = requests.get(GRAPH_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
# Get all comments
def get_all_comments(access_token,post_id, url):
    comments = []
    while url:
        params = {
            'access_token': access_token,
            'limit': 100  # Maximum number of comments/replies per request
        }
        
        url = url.format(POST_ID = post_id)
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
def get_all_replies(access_token,comment_id, url):
    replies = []
    while url:
        params = {
            'access_token': access_token,
            'limit': 100  # Maximum number of comments/replies per request
        }
        
        url = url.format(COMMENT_ID = comment_id)
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
def get_replies(access_token, comment_id, url):
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
    
