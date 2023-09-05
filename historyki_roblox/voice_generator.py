import base64
import json
import os
import requests

from typing import Optional

from historyki_roblox.resource_manager import ResourceManager


class VoiceGeneratorException(Exception):
    pass


class VoiceGenerator:

    def __init__(self, api_key: Optional[str] = None):
        self.resource_manager = ResourceManager()
        self.api_key = api_key or self.resource_manager.get_gtts_api_key()
        self.base_url = 'https://texttospeech.googleapis.com/v1'

    def synthesize(self, text: str, voice: str, pitch: int = 0, speaking_rate: int = 0) -> str:
        # valid speaking_rate is between 0.25 and 4.0.
        # Out of range: valid pitch is between -20.0 and 20.0.
        filepath = self.resource_manager.get_dialogue_path(f'{voice}-{pitch}-{speaking_rate}', text)
        if os.path.exists(filepath):
            return filepath

        body = {
            'audioConfig': {'audioEncoding': 'MP3', 'pitch': pitch, 'speakingRate': speaking_rate},
            'input': {'text': text},
            'voice': {'languageCode': 'pl-PL', 'name': voice}
        }
        params = {'key': self.api_key}
        response = requests.post(f'{self.base_url}/text:synthesize', params=params, json=body)
        if response.status_code != 200:
            raise VoiceGenerator(f'response status code: {response.status_code}\n{response.text}')

        binary_data = base64.b64decode(response.json()['audioContent'].encode())
        with open(filepath, 'wb') as f:
            f.write(binary_data)

        return filepath

    def get_voices(self, language_code: str='pl-PL') -> None:
        params = {'key': self.api_key, 'languageCode': language_code}
        response = requests.get(f'{self.base_url}/voices', params=params)
        if response.status_code != 200:
            return
        
        with open(f'{ROOT_PATH}/voices.json', 'w') as f:
            json.dump(response.json(), f)
