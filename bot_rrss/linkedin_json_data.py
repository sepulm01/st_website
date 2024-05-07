import requests
import json

# Define your LinkedIn API endpoint and access token
API_ENDPOINT = "https://api.linkedin.com/v2/ugcPosts"
API_ENDPOINT_1 = "https://api.linkedin.com/v2/assets?action=registerUpload"
ACCESS_TOKEN = "AQXoKJDxWITsJzdhf544Hu8DTtwo7y8gClvt4I691LezX0SlIp-9JiEG7Mgnv2NxqIbPq0fW8gV07eja47JCnr-ubcJ2LXs56dSX0Z7Yjc4pdiCR8U36VMd9Idzq0ZeJrqGpt7aLb4gKPjGSjcsSyGaDCxcKOASazwZRt6iQxMOimGCJKl_CYUpr5jc6wM6SirPUAxUvC--0mZRD47E6-WE-o_dvOJpCBV9vkVv3ETFcUvLGgJwGmHVJr0irpmyEsrTocqBy1gNwCcxaPetdqHKgUMCsOd8A7euEs9zo1xzeGCPJXYjA4fkfOEIsf-vZ2CzgeIqEZT4pLfRBRpKVEhP7ZAkUsA" #Get Access Token from Linkedin developer account
register_upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
share_url = API_ENDPOINT
access_token = ACCESS_TOKEN
person_urn = "urn:li:person:BSUE_tDK6K" #Get URN-ID from Postman

def create_text_post(text_content):
    # Define the JSON data to share on LinkedIn
    data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text_content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Convert the data to JSON format
    json_data = json.dumps(data)

    # Define headers for the POST request
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "x-li-format": "json"
    }

    # Send the POST request to LinkedIn API
    response = requests.post(API_ENDPOINT, data=json_data, headers=headers)

    # Check the response
    if response.status_code == 201:
        print("Successfully shared content on LinkedIn!")
        
    else:
        print(f"Failed to share content on LinkedIn. Status code: {response.status_code}")
        print(response.text)

    return response.status_code

def create_article_post(article_description, link_description, blog_url, title):
    # Define the JSON data to share an article or URL
    data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": article_description
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": link_description
                        },
                        "originalUrl": blog_url,
                        "title": {
                            "text": title
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Convert the data to JSON format
    json_data = json.dumps(data)

    # Define headers for the POST request
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "x-li-format": "json"
    }

    # Send the POST request to LinkedIn API
    response = requests.post(API_ENDPOINT, data=json_data, headers=headers)

    # Check the response
    if response.status_code == 201:
        # Extract the X-RestLi-Id from the response headers
        x_restli_id = response.headers.get("X-RestLi-Id")
        print(f"Successfully shared the article on LinkedIn! Post ID: {x_restli_id}")
    else:
        print(f"Failed to share the article on LinkedIn. Status code: {response.status_code}")
        print(response.text)

def register_upload_and_share_image(image_share_text, image_title, image_path):
    # Step 1: Register the image upload
    register_upload_data = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(register_upload_url, json=register_upload_data, headers=headers)
    upload_response_data = response.json()

    # Extract the upload URL and asset ID from the response
    upload_url = upload_response_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
    asset_id = upload_response_data["value"]["asset"]

    # Step 2: Upload the image file
    image_file_path = image_path  # Replace with your image file path

    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(upload_url, data=image_data, headers=headers)

    # Step 3: Create the image share
    share_data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": image_share_text
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {
                            "text": "Center stage!"
                        },
                        "media": asset_id,
                        "title": {
                            "text": image_title
                        }
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(share_url, json=share_data, headers=headers)

    # Check for a successful response (201 Created)
    if response.status_code == 201:
        print("Image share created successfully.")
        print("X-RestLi-Id:", response.headers.get("X-RestLi-Id"))
    else:
        print("Error creating image share. Status code:", response.status_code)
        print("Response content:", response.content.decode())


