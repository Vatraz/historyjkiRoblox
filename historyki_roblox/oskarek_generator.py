import os
import requests

from PIL import Image
from io import BytesIO
from lxml.html import fromstring

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


class OskareGenerator:

    def get_oskarek_from_bing(self, gender: str) -> str:
        search = 'instaboy' if gender == 'MALE' else 'instagirl'
        response = requests.get('https://www.bing.com/images/search', params={'q': search})
        html = fromstring(response.text)

        tmp = 'm' if gender == 'MALE' else 'f'
        images = html.xpath(f"//*[contains(concat(' ', normalize-space(@class), ' '), ' mimg ')]")
        for c, i in enumerate(images):
            src = i.get('src')
            if src is None:
                src = i.get('data-src')
            if src is None:
                continue
            image_response = requests.get(src)
            image_data = BytesIO(image_response.content)
            image = Image.open(image_data)
            image_format = image.format
            image_name = f'{tmp}{c}_bing.{image_format}'
            image.save(f'{ROOT_PATH}/data/oskareks/{image_name}')
