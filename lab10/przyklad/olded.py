#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

def oledtest():
    disp = SSD1331.SSD1331()
    
    # Inicjalizacja wyświetlacza
    disp.Init()
    disp.clear()
    
    # Tworzenie pustego obrazu do rysowania
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    
    # Ładowanie czcionek
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 13)
    
    print("- draw line")
    # Rysowanie linii
    draw.line([(0, 0), (0, 63)], fill="BLUE", width=5)
    draw.line([(0, 0), (95, 0)], fill="BLUE", width=5)
    draw.line([(0, 63), (95, 63)], fill="BLUE", width=5)
    draw.line([(95, 0), (95, 63)], fill="BLUE", width=5)
    
    print("- draw rectangle")
    # Rysowanie prostokąta
    draw.rectangle([(5, 5), (90, 30)], fill="BLUE")
    
    print("- draw text")
    # Rysowanie tekstu
    draw.text((8, 0), u'Hello', font=fontLarge, fill="WHITE")
    draw.text((12, 40), 'World !!!', font=fontSmall, fill="BLUE")
    
    # Wyświetlenie obrazu
    disp.ShowImage(image1, 0, 0)
    time.sleep(2)
    
    print("- draw image")
    # Rysowanie obrazu
    image = Image.open('./lib/oled/pic.jpg')
    disp.ShowImage(image, 0, 0)
    time.sleep(2)
    
    # Czyszczenie ekranu
    disp.clear()
    disp.reset()

def test():
    print('\nThe OLED screen test.')
    oledtest()

if __name__ == "__main__":
    test()
