import os
import base64
import json
import requests

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class VoiceGenerator:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://texttospeech.googleapis.com/v1'

    def synthesize(self, text: str, voice: str, pitch: int=0, speaking_rate: int=0) -> str:
        # valid speaking_rate is between 0.25 and 4.0.
        # Out of range: valid pitch is between -20.0 and 20.0.
        dir_name = f'{ROOT_PATH}/dialogues/{voice}-{pitch}-{speaking_rate}'
        if os.path.exists(dir_name) is False:
            os.mkdir(dir_name)

        mp3_filename = text.lower().replace(' ', '_') + '.mp3'
        mp3_filepath = f'{dir_name}/{mp3_filename}'
        if os.path.exists(mp3_filepath) is True:
            return mp3_filepath

        body = {
            'audioConfig': {'audioEncoding': 'MP3', 'pitch': pitch, 'speakingRate': speaking_rate},
            'input': {'text': text},
            'voice': {'languageCode': 'pl-PL', 'name': voice}
        }
        params = {'key': self.api_key}
        response = requests.post(f'{self.base_url}/text:synthesize', params=params, json=body)
        if response.status_code != 200:
            print(response.text)
            return

        binary_data = base64.b64decode(response.json()['audioContent'].encode())
        with open(mp3_filepath, 'wb') as f:
            f.write(binary_data)
        return mp3_filepath

    def get_voices(self, language_code: str='pl-PL') -> None:
        params = {'key': self.api_key, 'languageCode': language_code}
        response = requests.get(f'{self.base_url}/voices', params=params)
        if response.status_code != 200:
            return
        
        with open(f'{ROOT_PATH}/voices.json', 'w') as f:
            json.dump(response.json(), f)
