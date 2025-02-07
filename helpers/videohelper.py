import uuid
import os
import requests
import json
import time
from openai import AzureOpenAI
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

load_dotenv()

SPEECH_ENDPOINT = os.getenv('SPEECH_ENDPOINT')
API_VERSION = "2024-04-15-preview"
SUBSCRIPTION_KEY = os.getenv("SPEECH_KEY")

def generate_video(transcript: str, backgroundColor: str):
    job_id = str(uuid.uuid4())
    download_url = None
    if submit_synthesis(job_id, transcript, backgroundColor):
        while True:
            status = get_synthesis(job_id)
            if status == 'Succeeded':
                print('  - Batch avatar synthesis job succeeded')
                download_url = getdownloadurl(job_id)
                print('  - Download url: ' + download_url)
                
                local_url = f"./temp/{job_id}.mp4"
                
                response = requests.get(download_url)
                with open(local_url, 'wb') as file:
                    file.write(response.content)       
                
                break
            elif status == 'Failed':
                print('  - Batch avatar synthesis job failed')
                error = get_error(job_id)
                print(f'  - Error: {error}')
                break
            else:
                print(f'  - Batch avatar synthesis job is still running, status [{status}]')
                time.sleep(5)
    return local_url

def download_video(url: str):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
        
    return filename
        


def submit_synthesis(job_id: str, transcript: str, backgroundColor: str):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    payload = {
        'synthesisConfig': {
            "voice": 'en-US-AvaMultilingualNeural',
        },
        # Replace with your custom voice name and deployment ID if you want to use custom voice.
        # Multiple voices are supported, the mixture of custom voices and platform voices is allowed.
        # Invalid voice name or deployment ID will be rejected.
        'customVoices': {
            # "YOUR_CUSTOM_VOICE_NAME": "YOUR_CUSTOM_VOICE_ID"
        },
        "inputKind": "SSML",
        "inputs": [
            {
                "content": transcript,
            },
        ],
        "avatarConfig":
        {
            "customized": False, # set to True if you want to use customized avatar
            "talkingAvatarCharacter": 'Lisa',  # talking avatar character
            "talkingAvatarStyle": 'technical-sitting',  #casual-sitting 
            "videoFormat": "mp4",
            "videoCodec": "h264",
            "subtitleType": "external_file", # external_file, soft_embedded, hard_embedded, or none
            "backgroundColor": backgroundColor, # background color in RGBA format, default is white; can be set to 'transparent' for transparent background
        }  
    }

    response = requests.put(url, json.dumps(payload), headers=header)
    if response.status_code < 400:
        print('- Video Batch avatar synthesis job submitted successfully')
        print(f'  - Job ID: {response.json()["id"]}')
        
        return True
    else:
        print(f'- Failed to submit batch avatar synthesis job: [{response.status_code}], {response.text}')


def get_synthesis(job_id):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        if response.json()['status'] == 'Succeeded':
            print(f'  - Batch synthesis job succeeded')
        return response.json()['status']
    else:
        print(f'  - Failed to get batch synthesis job: {response.text}')

def get_error(job_id):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        if response.json()['status'] == 'Succeeded':
            print(f'  - Batch synthesis job succeeded')
        return response.json()['properties']['error']
    else:
        print(f'  - Failed to get batch synthesis job: {response.text}')

def getdownloadurl(job_id):
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses/{job_id}?api-version={API_VERSION}'
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        print('  - Get batch synthesis job successfully')
        #print(response.json())
        if response.json()['status'] == 'Succeeded':
            return response.json()["outputs"]["result"]
    else:
        print(f'  - Failed to get batch synthesis job: {response.text}')



def list_synthesis_jobs(skip: int = 0, max_page_size: int = 100):
    """List all batch synthesis jobs in the subscription"""
    url = f'{SPEECH_ENDPOINT}/avatar/batchsyntheses?api-version={API_VERSION}&skip={skip}&maxpagesize={max_page_size}'
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    response = requests.get(url, headers=header)
    if response.status_code < 400:
        print(f'  - List batch synthesis jobs successfully, got {len(response.json()["values"])} jobs')
        print(response.json())
    else:
        print(f'  - Failed to list batch synthesis jobs: {response.text}')
