import json
import os

from historyki_roblox.voice_generator import VoiceGenerator

api_key = os.environ.get('GTTS_API_KEY')
voice_generator = VoiceGenerator(api_key)
# voice_generator.get_voices()
voice_generator.synthesize('Hejka kochani gracie dzisiaj w roblox???', 'pl-PL-Standard-B')
