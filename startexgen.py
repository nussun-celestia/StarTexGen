import os
import noise
import random
from itertools import product
import numpy as np
from PIL import Image, ImageDraw, ImageShow, ImageChops, ImageEnhance
import math
import PySimpleGUI as sg

def temp_to_color(Temperature):
    Temperature = Temperature / 100
    # Calculate Red:
    if Temperature <= 66:
        Red = 255
    else:
        Red = Temperature - 60
        Red = 329.698727446 * (Red ** -0.1332047592)
        if Red < 0:
            Red = 0
        if Red > 255:
            Red = 255
    # Calculate Green:
    if Temperature <= 66:
        Green = Temperature
        Green = 99.4708025861 * math.log(Green) - 161.1195681661
        if Green < 0:
            Green = 0
        if Green > 255:
            Green = 255
    else:
        Green = Temperature - 60
        Green = 288.1221695283 * (Green ** -0.0755148492)
        if Green < 0:
            Green = 0
        if Green > 255:
            Green = 255
    # Calculate Blue:
    if Temperature >= 66:
        Blue = 255
    else:
        if Temperature <= 19:
            Blue = 0
        else:
            Blue = Temperature - 10
            Blue = 138.5177312231 * math.log(Blue) - 305.0447927307
            if Blue < 0:
                Blue = 0
            if Blue > 255:
                Blue = 255
    return([Red, Green, Blue])

def create_noise(size):
        circumference = (2*math.pi)*(float(values['Radius'])*695700)
        scale = 10.0
        width = size
        height = int(size/2)
        if int(values['Temperature']) < 3700:
            freq = ((1500/circumference)*6.275)+0.03
        else:
            freq = (1500/circumference)*6.275
        octaves = 6
        persistence = 0.5
        lacunarity = 1.5

        noise_img = Image.new('RGB', (width, height))

        latitudes = [lat / scale for lat in range(int(-90 * scale), int(90 * scale) + 1)]
        longitudes = [lng / scale for lng in range(int(-180 * scale), int(180 * scale) + 1)]

        radius = size / math.pi
        lng_std = 0
        lat_std = 0

        for x, y in product(range(width), range(height)):
            uvx = x / width
            uvy = y / height
            my = math.sin(uvy * math.pi - math.pi / 2)
            mx = math.cos(uvx * 2 * math.pi) * math.cos(uvy * math.pi - math.pi / 2)
            mz = math.sin(uvx * 2 * math.pi) * math.cos(uvy * math.pi - math.pi / 2)

            z = noise.snoise3(
                (mx + int(values['Seed'])) / freq,
                (my + int(values['Seed'])) / freq,
                mz / freq,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity
            )
            z_normalized = (z + 1) / 2

            color = (int((z+1)/2*430), int((z+1)/2*430), int((z+1)/2*430))

            color = color

            noise_img.putpixel((x, y), color)


        scale1b = 10.0
        freq1b = 1
        octaves1b = 6
        persistence1b = 1.01
        lacunarity1b = 5

        noise_detail = Image.new('RGB', (width, height))

        latitudes = [lat / scale1b for lat in range(int(-90 * scale1b), int(90 * scale1b) + 1)]
        longitudes = [lng / scale1b for lng in range(int(-180 * scale1b), int(180 * scale1b) + 1)]

        radius = size / math.pi
        lng_std = 0
        lat_std = 0

        for x, y in product(range(width), range(height)):
            uvx1b = x / width
            uvy1b = y / height
            my1b = math.sin(uvy1b * math.pi - math.pi / 2)
            mx1b = math.cos(uvx1b * 2 * math.pi) * math.cos(uvy1b * math.pi - math.pi / 2)
            mz1b = math.sin(uvx1b * 2 * math.pi) * math.cos(uvy1b * math.pi - math.pi / 2)

            z1b = noise.snoise3(
                (mx1b + int(values['Seed'])) / freq1b,
                (my1b + int(values['Seed'])) / freq1b,
                mz1b / freq1b,
                octaves=octaves1b,
                persistence=persistence1b,
                lacunarity=lacunarity1b
            )
            z_normalized1b = (z1b + 1) / 2*255

            color_detail = (int(z_normalized1b), int(z_normalized1b), int(z_normalized1b))

            noise_detail.putpixel((x, y), color_detail)


        scale2 = 10.0
        if int(values['Temperature']) < 5772:
            freq2 = 1154.4/float(values['Temperature'])
            if int(values['Temperature']) <= 3700:
                freq2 = freq2+0.6
        elif int(values['Temperature']) == 5772:
            freq2 = 0.2
        else:
            freq2 = float(values['Temperature'])*(0.2/5772)
        freq2 = freq2/(values['Multiplier']/100)
        octaves2 = 6
        
        if int(values['Temperature']) < 5772:
            persistence2 = float(values['Temperature'])*(0.5/5772)
        elif int(values['Temperature']) == 5772:
            persistence2 = 0.5
        else:
            persistence2 = 2886/float(values['Temperature'])

        if int(values['Temperature']) < 5772:
            lacunarity2 = 1.5
            if int(values['Temperature']) <= 3700:
                lacunarity2 = float(values['Temperature'])*(1.5/5772)
        elif int(values['Temperature']) == 5772:
            lacunarity2 = 1.5
        else:
            lacunarity2 = 8658/float(values['Temperature'])

        noise_img2 = Image.new('RGB', (width, height))

        latitudes = [lat / scale2 for lat in range(int(-90 * scale2), int(90 * scale2) + 1)]
        longitudes = [lng / scale2 for lng in range(int(-180 * scale2), int(180 * scale2) + 1)]

        radius = size / math.pi
        lng_std = 0
        lat_std = 0

        for x, y in product(range(width), range(height)):
            uvx2 = x / width
            uvy2 = y / height
            my2 = math.sin(uvy2 * math.pi - math.pi / 2)
            mx2 = math.cos(uvx2 * 2 * math.pi) * math.cos(uvy2 * math.pi - math.pi / 2)
            mz2 = math.sin(uvx2 * 2 * math.pi) * math.cos(uvy2 * math.pi - math.pi / 2)

            z2 = noise.snoise3(
                (mx2 + int(values['Seed'])) / freq2,
                (my2 + int(values['Seed'])) / freq2,
                mz2 / freq2,
                octaves=octaves2,
                persistence=persistence2,
                lacunarity=lacunarity2
            )
            if int(values['Temperature']) <= 5200:

                a1 = 4000
                b1 = 1600
                a2 = 5200
                b2 = 1200
                a = float(values['Temperature'])
                b = (b1+(a-a1)*((b2-b1)/(a2-a1)))
                z_normalized2 = (z2+1)/2*float(values['Temperature'])*(b/5772)
                # print(b)
                if int(values['Temperature']) <= 3700:
                    z_normalized2 = (z2+1)/2*float(values['Temperature'])*(2000/5772)
            else:
                z_normalized2 = (z2+1)/2*float(values['Temperature'])*(1200/5772)
            z_normalized2 = z_normalized2/(values['Multiplier']/100)

            color = (int(z_normalized2), int(z_normalized2), int(z_normalized2))

            color2 = color

            noise_img2.putpixel((x, y), color2)

        scale2b = 10.0
        freq2b = 1154.4/float(values['Temperature'])
        freq2b = freq2b+0.6
        octaves2b = 6
        persistence2b = float(values['Temperature'])*(0.5/5772)
        lacunarity2b = float(values['Temperature'])*(1.5/5772)

        noise_img2b = Image.new('RGB', (width, height))

        latitudes = [lat / scale2b for lat in range(int(-90 * scale2), int(90 * scale2) + 1)]
        longitudes = [lng / scale2b for lng in range(int(-180 * scale2), int(180 * scale2) + 1)]

        radius = size / math.pi
        lng_std = 0
        lat_std = 0

        for x, y in product(range(width), range(height)):
            uvx2b = x / width
            uvy2b = y / height
            my2b = math.sin(uvy2b * math.pi - math.pi / 2)
            mx2b = math.cos(uvx2b * 2 * math.pi) * math.cos(uvy2b * math.pi - math.pi / 2)
            mz2b = math.sin(uvx2b * 2 * math.pi) * math.cos(uvy2b * math.pi - math.pi / 2)

            z2b = noise.snoise3(
                (mx2b + int(values['Seed'])) / freq2b,
                (my2b + int(values['Seed'])) / freq2b,
                mz2b / freq2,
                octaves=octaves2b,
                persistence=persistence2b,
                lacunarity=lacunarity2b
            )
            z_normalized2b = (z2b+1)/2*float(values['Temperature'])*(1325/5772)

            color = (int(z_normalized2b), int(z_normalized2b), int(z_normalized2b))

            color2b = color

            noise_img2b.putpixel((x, y), color2b)

        temperature = eval(values['Temperature'])
        colors = temp_to_color(temperature)
        red = round(colors[0])
        green = round(colors[1])
        blue = round(colors[2])
        img_new = Image.new("RGB", (size, round(size/2)), (red, green, blue))
        draw = ImageDraw.Draw(img_new)
        sharp = ImageEnhance.Sharpness(noise_img)
        sharp_noise = sharp.enhance(2)
        contrast = ImageEnhance.Contrast(sharp_noise)
        new_noise = contrast.enhance(0.125)
        contrast_detail = ImageEnhance.Contrast(noise_detail)
        detail_noise = contrast_detail.enhance(0.075)
        brighter_detail = ImageEnhance.Brightness(detail_noise)
        detail_noise_new = brighter_detail.enhance(1.75)
        contrast2 = ImageEnhance.Contrast(noise_img2)
        new_noise2 = contrast2.enhance(2)
        if int(values['Temperature']) <= 5200:
            c1 = 4000
            d1 = 0.6
            c2 = 5772
            d2 = 1
            c = float(values['Temperature'])
            d = (d1+(c-c1)*((d2-d1)/(c2-c1)))
            contrast_spot2 = ImageEnhance.Contrast(new_noise2)
            contrast_spot_noise2 = contrast_spot2.enhance(d)
            noised = ImageChops.multiply(contrast_spot_noise2, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
            if int(values['Temperature']) <= 3700:
                brighter = ImageEnhance.Brightness(new_noise2)
                spot_noise_new = brighter.enhance(1.25)
                spots = ImageChops.multiply(spot_noise_new, noise_img2b)
                contrast_spot = ImageEnhance.Contrast(spots)
                contrast_spot_noise = contrast_spot.enhance(0.6)
                noised = ImageChops.multiply(contrast_spot_noise, new_noise)
                noised_final = ImageChops.multiply(img_new, noised)
        elif int(values['Temperature']) >= 7500:
            noised_final = ImageChops.multiply(img_new, new_noise)
        else:
            noised = ImageChops.multiply(new_noise2, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
        true_final = ImageChops.multiply(detail_noise_new, noised_final)
        return true_final

sg.theme('DarkGrey6')

layout = [
    [sg.Text('Temperature (Kelvin):'), sg.Input(key='Temperature', default_text='5772')],
    [sg.Text('Radius of star (R☉):'), sg.Input(key='Radius', default_text='1')],
    [sg.Checkbox('Virtual Texture', default=False, key='TexType')],
    [sg.Text('Texture resolution:'), sg.InputCombo(('1024', '2048', '4096', '8192', '16384'), size=(25, 1), key='TexSize', change_submits=True)],
    [sg.Text('Seed:'), sg.Input(key='Seed', size=(25, 1), default_text='0'), sg.Button('Randomize')],
    [sg.Text('Starspot frequency multiplier:'), sg.Slider(range=(80,120), orientation='horizontal', key='Multiplier', default_value=100)],
    [sg.Text('File name:'), sg.Input(key='Filename')],
    [sg.Text('')],
    [sg.Text('Preview:')],
    [sg.Image(r'default.png', key='Preview')],
    [sg.Button('Refresh'), sg.Button('Generate'), sg.Button('Exit'), sg.Text(size=(25, 1), key='Output')],
]

window = sg.Window('Star Texture Generator', layout, icon="icon.ico")
while True:
    event, values = window.read()
    img_temp = Image.new("RGB", (512, 256), (255, 242, 230))
    draw = ImageDraw.Draw(img_temp)
    img_temp.save("temp.png")

    if event == sg.WIN_CLOSED or event == 'Exit':
        os.remove('temp.png')
        break

    if values['TexType'] == True:
        window.FindElement('TexSize').Update(values=('16384','32768','65536'))
    else:
        window.FindElement('TexSize').Update(values=('1024', '2048', '4096', '8192', '16384'))

    if event == 'Randomize':
        window.FindElement('Seed').Update(random.randint(-20000,20000))
    if event == 'Refresh':
        true_final = create_noise(512)
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Generate':
        window['Output'].update('Texture generating...')
        if values['Temperature'] == '':
            window['Output'].update('Error: missing temperature!')
        elif values['TexSize'] == '':
            window['Output'].update('Error: missing texture resolution!')
        else:
            temperature = eval(values['Temperature'])
            colors = temp_to_color(temperature)
            red = round(colors[0])
            green = round(colors[1])
            blue = round(colors[2])
            size = round(eval(values['TexSize']))
            img_new = Image.new("RGB", (size, round(size/2)), (red, green, blue))
            draw = ImageDraw.Draw(img_new)
            if values['Filename'] == '':
                window['Output'].update('Error: missing filename!')
            else:
                true_final = create_noise(size)
                true_final.save("%s.png" % values['Filename'])
                window['Output'].update('Texture generated!')
window.close()
