import random
import openai
import requests
import json


def get_image_content(prompt, API, file_path):
    phrases = ["abstract art", "photorealistic 4k", "Cyberpunk", "Oil paint", 'futurism']
    random_phrase = random.choice(phrases)
    full_string = prompt + random_phrase

    try:
        openai.api_key = API
        response = openai.Image.create(prompt=full_string, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        response = requests.get(image_url)

        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path, image_url
        else:
            print(f"Failed to download the image. HTTP Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def get_image_description(API, image_link, logger):

    API_timeout = 120
    API_endpoint = 'https://vision.astica.ai/describe'
    modelVersion = '2.1_full'
    API_visionParams = 'gpt_detailed'

    # Define payload dictionary
    asticaAPI_payload = {
        'tkn': API,
        'modelVersion': modelVersion,
        'visionParams': API_visionParams,
        'input': image_link,
        'gpt_length': round(random.uniform(60, 110)),
        'gpt_prompt': 'Set of rules: Never tell exact image resolution, never tell that you are AI model, simulate human natural spech!'
    }

    def asticaAPI(endpoint, payload, timeout):
        response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout,
                                 headers={'Content-Type': 'application/json', })
        if response.status_code == 200:
            return response.json()
        else:
            return {'status': 'error', 'error': 'Failed to connect to the API.'}

    # call API function and store result
    asticaAPI_result = asticaAPI(API_endpoint, asticaAPI_payload, API_timeout)

    if 'status' in asticaAPI_result:
        if asticaAPI_result['status'] == 'success':
            # Extract and print GPT Caption if exists
            if 'caption_GPTS' in asticaAPI_result and asticaAPI_result['caption_GPTS'] != '':
                return_ = (asticaAPI_result['caption_GPTS'])
                return return_
            else:
                logger.warning("GPT Caption not available in the response.")
        else:
            logger.error('Output Error:', asticaAPI_result.get('error', 'Unknown Error'))
    else:
        logger.error('Invalid response')
OPENAI_API = "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"

