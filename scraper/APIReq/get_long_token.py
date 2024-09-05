import requests

def exchange_for_long_lived_token(app_id, app_secret, short_lived_token):
    """
    Exchange a short-lived access token for a long-lived access token.

    :param app_id: Your Facebook App ID.
    :param app_secret: Your Facebook App Secret.
    :param short_lived_token: The short-lived access token you want to extend.
    :return: Long-lived access token if successful, None otherwise.
    """
    url = "https://graph.facebook.com/v20.0/oauth/access_token"
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        long_lived_token = response.json().get('access_token')
        return long_lived_token
    else:
        print(f"Failed to exchange token: {response.status_code}")
        return None

# exchange short lived token with long lived token ( lifetime = 60 days )
APP_ID = "463985053199459"  # Replace with your Facebook App ID
APP_SECRET = "03bbb1f7b89c45cc6a5d2be65aadca31"  # Replace with your Facebook App Secret
SHORT_LIVED_TOKEN = "EAAGlZCfBG7GMBO2puCae9yji0S55XYQku4Xr2R2OiNIv3QWAkOD94IYy7Qw1jEDS37acWhRG2rbAjaNQ8P5xfk2tCVumCOq7RVYLO10p3nWS8KYQ3n1XLRmB4FjbkBMf1xOHtKdm8sTLvvfO7Wgk26YkgTTMhj5hq5EiRzZChYVTG09bcalJHtodihl1yeHOtZAvZAq0XXZBFDHciiNvuCAnR"  # Replace with your short-lived token

# long_lived_token = exchange_for_long_lived_token(APP_ID, APP_SECRET, SHORT_LIVED_TOKEN)

# if long_lived_token:
#     print("Long-Lived Access Token:")
#     print(long_lived_token)
# else:
#     print("Failed to obtain a long-lived access token.")

