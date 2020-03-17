import os
import json
import requests

API_KEY = '6c3fca146e274362927e95f872b115b2'
ENDPOINT = 'https://computervisionapitesting.cognitiveservices.azure.com/vision/v1.0/ocr'

#API_KEY = 'b7fc5399a0e34517a37e39145cd90907'
#ENDPOINT = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/ocr'
DIR = 'images'


def handler():
    text = ''
    for filename in sorted(os.listdir(DIR)):
        if filename.endswith(".jpg"):
            pathToImage = '{0}/{1}'.format(DIR, filename)
            results = get_text(pathToImage)
            text += filename + "\n"
            text += parse_text(results)

    open('output.txt', 'w').write(text)


def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    return text


def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'language': 'ja',
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results


if __name__ == '__main__':
    handler()
