# https://stackoverflow.com/questions/62329331/load-svg-image-in-opencv
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from cairosvg import svg2png
import cv2


svg_url = 'https://www.thebalanceffxiv.com/theme-assets/jobs/healers/sage/sage.svg'

svg_data = requests.get(svg_url).content

png = svg2png(bytestring=svg_data, scale=1.5)

pil_img = Image.open(BytesIO(png)).convert('RGBA')

cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
cv2.imwrite('cv.png', cv_img)


