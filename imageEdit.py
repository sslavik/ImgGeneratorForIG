import requests
from PIL import Image, ImageDraw, ImageFont
import glob
import ntpath
from pyquery import PyQuery as pq
import textwrap

## Variables

fontPath = 'fonts/inter-Bold.ttf'
width = 1080
heigth = 1920
innerImageSize = (240,240)
logoImageSize = (400,400)
imgLogo = Image.open("./logo/logoN.png").convert("RGBA")
imgLogo.thumbnail(logoImageSize, Image.ANTIALIAS)

urls = ["https://www.elmundo.es/horoscopo/aries.html", 
"https://www.elmundo.es/horoscopo/tauro.html",
 "https://www.elmundo.es/horoscopo/geminis.html", 
 "https://www.elmundo.es/horoscopo/cancer.html", 
 "https://www.elmundo.es/horoscopo/leo.html", "https://www.elmundo.es/horoscopo/virgo.html",
  "https://www.elmundo.es/horoscopo/libra.html", "https://www.elmundo.es/horoscopo/escorpio.html", 
  "https://www.elmundo.es/horoscopo/sagitario.html","https://www.elmundo.es/horoscopo/capricornio.html",
   "https://www.elmundo.es/horoscopo/acuario.html", "https://www.elmundo.es/horoscopo/piscis.html"]

for imgPath in glob.glob("./astrology/*.png"):
    # IMAGE COMPOSITION
    background = Image.new('RGBA', (width, heigth), color = (240,240,240))
    imgContained = Image.open(imgPath).convert("RGBA")
    imgContained.thumbnail(innerImageSize, Image.ANTIALIAS)

    offset = (((width // 2) - (imgContained.size[0] // 2)), 100)
    offsetLogo =((width - imgLogo.size[0]) // 2, (heigth - (imgLogo.size[1] + 100)) )
    background.paste(imgContained, offset, imgContained)
    background.paste(imgLogo, offsetLogo, imgLogo)
    
    # TEXT COMPOSITION
    for url in urls:
        pathSplited = ntpath.basename(imgPath).split('.')
        if(pathSplited[0].lower() in url):
            content = requests.get(url).text
            html = pq(content)
            text = html(".col-5b").children("p").eq(0).text()

            font = ImageFont.truetype(fontPath, 55)
            fontHeader = ImageFont.truetype(fontPath, 63)
            draw = ImageDraw.Draw(background)
            #Header
            headerWidth, headerHeight = draw.textsize(pathSplited[0],fontHeader)
            draw.text(((width/2 - headerWidth/2 - 25), 150 + innerImageSize[0]), pathSplited[0].upper(), font= fontHeader, fill=(30,30,30))
            #Content
            draw.text((width/6,heigth/3), "\n".join(textwrap.wrap(text,25)), font= font, fill=(30,30,30))
            

            # SAVE

            background.save("./res/new_" + ntpath.basename(imgPath))