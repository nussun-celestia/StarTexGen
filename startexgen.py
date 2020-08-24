import os
import noise
import random
from itertools import product
import numpy as np
from PIL import Image, ImageDraw, ImageShow, ImageChops, ImageEnhance, ImageOps
import math
import PySimpleGUI as sg

spectra = {
    "Vega": np.array([
        1.49367, 1.54471, 1.81878, 1.91241, 1.2929, 1.79114, 1.77413, 1.70716, 1.56168, 1.11728, 1.52847, 1.50317, 1.44746, 1.4018, 1.36738, 1.32857, 
        1.28946, 1.24422, 1.18237, 0.85037, 1.06147, 1.09692, 1.06894, 1.03883, 1.01305, 0.97619, 0.94761, 0.92189, 0.89605, 0.87237, 0.84757, 0.82806, 
        0.80377, 0.78387, 0.76136, 0.74286, 0.72311, 0.7045, 0.68684, 0.66853, 0.64976, 0.63457, 0.61812, 0.60278, 0.58685, 0.57205, 0.55971, 0.54451, 
        0.53353, 0.51601, 0.50537, 0.49307, 0.47527, 0.37761, 0.43725, 0.44816, 0.4396, 0.42995, 0.42074, 0.41263, 0.40258, 0.39369, 0.38466, 0.37642, 
        0.36723, 0.35911, 0.35233, 0.34516, 0.33668, 0.33015, 0.32281, 0.31598, 0.30998, 0.30301, 0.29675, 0.29095, 0.28478, 0.27771, 0.27262, 0.26772, 
        0.2627, 0.25759, 0.25282, 0.24721, 0.24302, 0.2378, 0.2323, 0.22828, 0.22451
    ]),
    "Sun": np.array([
        1.14262, 0.91021, 1.59446, 1.59842, 1.60575, 1.64867, 1.61866, 1.60261, 1.37227, 1.64495, 1.64123, 1.77152, 1.92485, 1.87994, 1.88343, 1.8611, 
        1.83783, 1.86924, 1.91484, 1.73616, 1.8141, 1.84016, 1.75081, 1.80945, 1.81457, 1.70382, 1.68404, 1.73918, 1.80316, 1.78269, 1.72313, 1.75849, 
        1.74756, 1.74919, 1.69428, 1.71289, 1.69428, 1.73081, 1.70358, 1.7101, 1.62401, 1.66961, 1.63937, 1.65309, 1.6175, 1.56678, 1.59865, 1.55119, 1.55886, 
        1.54397, 1.50582, 1.50675, 1.49837, 1.36063, 1.4658, 1.44393, 1.41461, 1.4081, 1.39228, 1.36342, 1.35133, 1.33085, 1.29362, 1.31363, 1.29269, 1.26896, 
        1.24151, 1.25733, 1.23685, 1.2201, 1.17357, 1.19497, 1.17729, 1.16752, 1.15403, 1.12238, 1.12331, 1.11215, 1.10749, 1.09958, 1.0805, 1.06654, 1.06561, 
        1.04281, 1.03955, 1.03164, 1.00791, 1.00372, 0.99581
    ])
}
    
cmf = np.array([
    [390.0, 0.0015, -0.0004, 0.0062],
    [395.0, 0.0038, -0.001, 0.0161],
    [400.0, 0.0089, -0.0025, 0.04],
    [405.0, 0.0188, -0.0059, 0.0906],
    [410.0, 0.035, -0.0119, 0.1802],
    [415.0, 0.0531, -0.0201, 0.3088],
    [420.0, 0.0702, -0.0289, 0.467],
    [425.0, 0.0763, -0.0338, 0.6152],
    [430.0, 0.0745, -0.0349, 0.7638],
    [435.0, 0.0561, -0.0276, 0.8778],
    [440.0, 0.0323, -0.0169, 0.9755],
    [445.0, -0.0044, 0.0024, 1.0019],
    [450.0, -0.0478, 0.0283, 0.9996],
    [455.0, -0.097, 0.0636, 0.9139],
    [460.0, -0.1586, 0.1082, 0.8297],
    [465.0, -0.2235, 0.1617, 0.7417],
    [470.0, -0.2848, 0.2201, 0.6134],
    [475.0, -0.3346, 0.2796, 0.472],
    [480.0, -0.3776, 0.3428, 0.3495],
    [485.0, -0.4136, 0.4086, 0.2564],
    [490.0, -0.4317, 0.4716, 0.1819],
    [495.0, -0.4452, 0.5491, 0.1307],
    [500.0, -0.435, 0.626, 0.091],
    [505.0, -0.414, 0.7097, 0.058],
    [510.0, -0.3673, 0.7935, 0.0357],
    [515.0, -0.2845, 0.8715, 0.02],
    [520.0, -0.1855, 0.9477, 0.0095],
    [525.0, -0.0435, 0.9945, 0.0007],
    [530.0, 0.127, 1.0203, -0.0043],
    [535.0, 0.3129, 1.0375, -0.0064],
    [540.0, 0.5362, 1.0517, -0.0082],
    [545.0, 0.7722, 1.039, -0.0094],
    [550.0, 1.0059, 1.0029, -0.0097],
    [555.0, 1.271, 0.9698, -0.0097],
    [560.0, 1.5574, 0.9162, -0.0093],
    [565.0, 1.8465, 0.8571, -0.0087],
    [570.0, 2.1511, 0.7823, -0.008],
    [575.0, 2.425, 0.6953, -0.0073],
    [580.0, 2.6574, 0.5966, -0.0063],
    [585.0, 2.9151, 0.5063, -0.00537],
    [590.0, 3.0779, 0.4203, -0.00445],
    [595.0, 3.1613, 0.336, -0.00357],
    [600.0, 3.1673, 0.2591, -0.00277],
    [605.0, 3.1048, 0.1917, -0.00208],
    [610.0, 2.9462, 0.1367, -0.0015],
    [615.0, 2.7194, 0.0938, -0.00103],
    [620.0, 2.4526, 0.0611, -0.00068],
    [625.0, 2.17, 0.0371, -0.000442],
    [630.0, 1.8358, 0.0215, -0.000272],
    [635.0, 1.5179, 0.0112, -0.000141],
    [640.0, 1.2428, 0.0044, -5.49e-05],
    [645.0, 1.007, 7.8e-05, -2.2e-06],
    [650.0, 0.7827, -0.001368, 2.37e-05],
    [655.0, 0.5934, -0.001988, 2.86e-05],
    [660.0, 0.4442, -0.002168, 2.61e-05],
    [665.0, 0.3283, -0.002006, 2.25e-05],
    [670.0, 0.2394, -0.001642, 1.82e-05],
    [675.0, 0.1722, -0.001272, 1.39e-05],
    [680.0, 0.1221, -0.000947, 1.03e-05],
    [685.0, 0.0853, -0.000683, 7.38e-06],
    [690.0, 0.0586, -0.000478, 5.22e-06],
    [695.0, 0.0408, -0.000337, 3.67e-06],
    [700.0, 0.0284, -0.000235, 2.56e-06],
    [705.0, 0.0197, -0.000163, 1.76e-06],
    [710.0, 0.0135, -0.000111, 1.2e-06],
    [715.0, 0.00924, -7.48e-05, 8.17e-07],
    [720.0, 0.00638, -5.08e-05, 5.55e-07],
    [725.0, 0.00441, -3.44e-05, 3.75e-07],
    [730.0, 0.00307, -2.34e-05, 2.54e-07],
    [735.0, 0.00214, -1.59e-05, 1.71e-07],
    [740.0, 0.00149, -1.07e-05, 1.16e-07],
    [745.0, 0.00105, -7.23e-06, 7.85e-08],
    [750.0, 0.000739, -4.87e-06, 5.31e-08],
    [755.0, 0.000523, -3.29e-06, 3.6e-08],
    [760.0, 0.000372, -2.22e-06, 2.44e-08],
    [765.0, 0.000265, -1.5e-06, 1.65e-08],
    [770.0, 0.00019, -1.02e-06, 1.12e-08],
    [775.0, 0.000136, -6.88e-07, 7.53e-09],
    [780.0, 9.84e-05, -4.65e-07, 5.07e-09],
    [785.0, 7.13e-05, -3.12e-07, 3.4e-09],
    [790.0, 5.18e-05, -2.08e-07, 2.27e-09],
    [795.0, 3.77e-05, -1.37e-07, 1.5e-09],
    [800.0, 2.76e-05, -8.8e-08, 9.86e-10],
    [805.0, 2.03e-05, -5.53e-08, 6.39e-10],
    [810.0, 1.49e-05, -3.36e-08, 4.07e-10],
    [815.0, 1.1e-05, -1.96e-08, 2.53e-10],
    [820.0, 8.18e-06, -1.09e-08, 1.52e-10],
    [825.0, 6.09e-06, -5.7e-09, 8.64e-11],
    [830.0, 4.55e-06, -2.77e-09, 4.42e-11]
])
cells = cmf[:, 1:]
cells /= np.sum(cells, axis=0)

H = 6.626e-34
C = 299792458
K = 1.381e-23
def blackbody(nm, t):
    m = nm / 1e9
    return 2*H * C**2 / m**5 / (np.exp(H*C/(m*K*t)) - 1)

def spec_to_color(spectrum):
    rgb = np.sum(spectrum[:, np.newaxis] * cells, axis=0)
    rgb = (rgb / np.max(rgb))**(1/2.2) * 255
    return [int(color) for color in rgb]

def temp_to_color(temperature):
    return spec_to_color(blackbody(cmf[:, 0], temperature))

def temp_to_color_D65(Temperature):
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

def create_noise(size, temperature, radius, colors, spectrum=None, type='Main sequence (V)'):
        circumference = (2*math.pi)*(float(radius)*695700)
        scale = 10.0
        width = size
        height = int(size/2)
        if type == 'Subgiant (IV)':
            freq = ((1500/circumference)*7.986)+0.02
        elif type == 'Giant (III)':
            freq = 400/float(temperature)
        elif type == 'Bright Giant (II)' or type == 'Carbon star (C)':
            freq = 550/float(temperature)
        elif type == 'Supergiant (Ib)':
            freq = 585/float(temperature)
        elif type == 'Supergiant (Iab)':
            freq = 600/float(temperature)
        elif type == 'Supergiant (Ia)':
            freq = 615/float(temperature)
        elif type == 'Hypergiant (Ia+)':
            freq = 650/float(temperature)
        elif int(temperature) < 3700:
            freq = ((1500/circumference)*7.986)+0.03
        else:
            freq = (1500/circumference)*7.986
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

            z_normalized_b = 1-z_normalized

            color_a = (int(z_normalized_b*255), int(z_normalized_b*255), int(z_normalized_b*255))

            color_b = (int(z_normalized*255), int(z_normalized*255), int(z_normalized*255))

            if z_normalized < .5:
                color = color_a
            else:
                color = color_b
    
            #color = (int((z+1)/2*430), int((z+1)/2*430), int((z+1)/2*430))

            #color = color

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
        if type == 'Bright Giant (II)' or type == 'Carbon star (C)':
            if float(temperature) >= 10000:
                freq2 = float(temperature)*0.00003000
            else:
                freq2 = 3000/float(temperature)
            octaves2 = 6
            persistence2 = 0.65
            lacunarity2 = 2
        elif type == 'Supergiant (Ib)':
            if float(temperature) >= 10000:
                freq2 = float(temperature)*0.00003300
            else:
                freq2 = 3300/float(temperature)
            octaves2 = 6
            persistence2 = 0.65
            lacunarity2 = 2
        elif type == 'Supergiant (Iab)':
            if float(temperature) >= 10000:
                freq2 = float(temperature)*0.00003630
            else:
                freq2 = 3630/float(temperature)
            octaves2 = 6
            persistence2 = 0.65
            lacunarity2 = 2
        elif type == 'Supergiant (Ia)':
            if float(temperature) >= 10000:
                freq2 = float(temperature)*0.00003993
            else:
                freq2 = 3993/float(temperature)
            octaves2 = 6
            persistence2 = 0.65
            lacunarity2 = 2
        elif type == 'Hypergiant (Ia+)':
            if float(temperature) >= 10000:
                freq2 = float(temperature)*0.00004250
            else:
                freq2 = 4250/float(temperature)
            octaves2 = 6
            persistence2 = 0.65
            lacunarity2 = 2  
        else:
            if int(temperature) < 5772:
                freq2 = 1154.4/float(temperature)
                if int(temperature) <= 3700:
                    freq2 = freq2+0.6
            elif int(temperature) == 5772:
                freq2 = 0.2
            else:
                freq2 = float(temperature)*(0.2/5772)
            freq2 = freq2/(values['Multiplier']/100)
            octaves2 = 6
        
            if int(temperature) < 5772:
                persistence2 = float(temperature)*(0.5/5772)
            elif int(temperature) == 5772:
                persistence2 = 0.5
            else:
                persistence2 = 2886/float(temperature)

            if int(temperature) < 5772:
                lacunarity2 = 1.5
                if int(temperature) <= 3700:
                    lacunarity2 = float(temperature)*(1.5/5772)
            elif int(temperature) == 5772:
                lacunarity2 = 1.5
            else:
                lacunarity2 = 8658/float(temperature)

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
            if type == 'Bright Giant (II)' or type == 'Supergiant (Ib)' or type == 'Supergiant (Iab)' or type == 'Supergiant (Ia)' or type == 'Hypergiant (Ia+)' or type == 'Carbon star (C)':
                z_normalized2 = (z2+1)/2*255
            else:
                if int(temperature) <= 5200:

                    a1 = 4000
                    b1 = 1600
                    a2 = 5200
                    b2 = 1200
                    a = float(temperature)
                    b = (b1+(a-a1)*((b2-b1)/(a2-a1)))
                    z_normalized2 = (z2+1)/2*float(temperature)*(b/5772)
                    #z_normalized2_b = (1-((z2+1)/2))*float(temperature)*(b/5772)
                    if int(temperature) <= 3700:
                        z_normalized2 = (z2+1)/2*float(temperature)*(2000/5772)
                        #z_normalized2_b = (1-((z2+1)/2))*float(temperature)*(2000/5772)
                else:
                    z_normalized2 = (z2+1)/2*float(temperature)*(1200/5772)
                    #z_normalized2_b = (1-((z2+1)/2))*float(temperature)*(1200/5772)
            z_normalized2 = z_normalized2/(values['Multiplier']/100)

            #print(z_normalized2_b)

            #color2_a = (int(z_normalized2_b), int(z_normalized2_b), int(z_normalized2_b))

            color2_b = (int(z_normalized2), int(z_normalized2), int(z_normalized2))

            #if (z2+1)/2 < .5:
                #color2 = color2_b
            #else:
            color2 = color2_b

            # color = (int(z_normalized2), int(z_normalized2), int(z_normalized2))

            # color2 = color

            noise_img2.putpixel((x, y), color2)

        scale2b = 10.0
        freq2b = 1154.4/float(temperature)
        freq2b = freq2b+0.6
        octaves2b = 6
        persistence2b = float(temperature)*(0.5/5772)
        lacunarity2b = float(temperature)*(1.5/5772)

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
            z_normalized2b = (z2b+1)/2*float(temperature)*(1325/5772)

            color = (int(z_normalized2b), int(z_normalized2b), int(z_normalized2b))

            color2b = color

            noise_img2b.putpixel((x, y), color2b)
        
        if spectrum is None:
            temperature2 = float(temperature)
            #colors = temp_to_color(temperature2)
            if colors == 'D65':
                temperature2 = float(temperature)
                colors = temp_to_color_D65(temperature2)
            else:
                temperature2 = float(temperature)
                colors = temp_to_color(temperature2)
        else:
            colors = spec_to_color(spectrum)
        red = round(colors[0])
        green = round(colors[1])
        blue = round(colors[2])
        img_new = Image.new("RGB", (size, round(size/2)), (red, green, blue))
        draw = ImageDraw.Draw(img_new)
        sharp = ImageEnhance.Sharpness(noise_img)
        sharp_noise = sharp.enhance(2)
        contrast = ImageEnhance.Contrast(sharp_noise)
        if type == 'Giant (III)':
            new_noise_contrast = contrast.enhance(0.35)
        elif type == 'Bright Giant (II)' or type == 'Carbon star (C)':
            new_noise_contrast = contrast.enhance(0.4)
        elif type == 'Supergiant (Ib)' or type == 'Supergiant (Iab)' or type == 'Supergiant (Ia)' or type == 'Hypergiant (Ia+)':
            new_noise_contrast = contrast.enhance(0.425)
        else:
            new_noise_contrast = contrast.enhance(0.175)
        new_noise_bright = ImageEnhance.Brightness(new_noise_contrast)
        if type == 'Bright Giant (II)' or type == 'Carbon star (C)':
            new_noise = new_noise_bright.enhance(1.625)
        elif type == 'Supergiant (Ib)' or type == 'Supergiant (Iab)' or type == 'Supergiant (Ia)':
            new_noise = new_noise_bright.enhance(1.475)
        elif type == 'Hypergiant (Ia+)':
            new_noise = new_noise_bright.enhance(1.55)
        else:
            new_noise = new_noise_bright.enhance(1.25)
        contrast_detail = ImageEnhance.Contrast(noise_detail)
        detail_noise = contrast_detail.enhance(0.075)
        brighter_detail = ImageEnhance.Brightness(detail_noise)
        detail_noise_new = brighter_detail.enhance(1.75)
        contrast2 = ImageEnhance.Contrast(noise_img2)
        new_noise2 = contrast2.enhance(2)
        if int(temperature) <= 3700 or type == 'Bright Giant (II)' or type == 'Supergiant (Ib)' or type == 'Supergiant (Iab)' or type == 'Supergiant (Ia)' or type == 'Hypergiant (Ia+)' or type == 'Carbon star (C)':
            fixed_starspots = new_noise2
        else:
            invert = ImageChops.invert(new_noise2)
            gradient = Image.open("starspot gradient map.png")
            gradient_map = gradient.convert('RGB')
            gradient_map2 = ImageOps.scale(gradient_map, size/3600)
            fixed_starspots_notinvert = ImageChops.multiply(gradient_map2, invert)
            fixed_starspots = ImageChops.invert(fixed_starspots_notinvert)
        if int(temperature) <= 5200:
            c1 = 4000
            d1 = 0.6
            c2 = 5772
            d2 = 1
            c = float(temperature)
            d = (d1+(c-c1)*((d2-d1)/(c2-c1)))
            contrast_spot2 = ImageEnhance.Contrast(fixed_starspots)
            contrast_spot_noise2 = contrast_spot2.enhance(d)
            noised = ImageChops.multiply(contrast_spot_noise2, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
            if int(temperature) <= 3700:
                brighter = ImageEnhance.Brightness(fixed_starspots)
                spot_noise_new = brighter.enhance(1.25)
                spots = ImageChops.multiply(spot_noise_new, noise_img2b)
                contrast_spot = ImageEnhance.Contrast(spots)
                contrast_spot_noise = contrast_spot.enhance(0.6)
                noised = ImageChops.multiply(contrast_spot_noise, new_noise)
                noised_final = ImageChops.multiply(img_new, noised)
        if type == 'Bright Giant (II)' or type == 'Carbon star (C)':
            contrast_spot = ImageEnhance.Contrast(fixed_starspots)
            contrast_spot_noise = contrast_spot.enhance(0.3)
            brighter = ImageEnhance.Brightness(contrast_spot_noise)
            spot_noise_new = brighter.enhance(1.75)
            spots = ImageChops.multiply(spot_noise_new, noise_img2b)
            noised = ImageChops.multiply(spot_noise_new, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
        elif type == 'Supergiant (Ib)' or type == 'Supergiant (Iab)' or type == 'Supergiant (Ia)':
            contrast_spot = ImageEnhance.Contrast(fixed_starspots)
            contrast_spot_noise = contrast_spot.enhance(0.4)
            brighter = ImageEnhance.Brightness(contrast_spot_noise)
            spot_noise_new = brighter.enhance(1.5)
            spots = ImageChops.multiply(spot_noise_new, noise_img2b)
            noised = ImageChops.multiply(spot_noise_new, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
        elif type == 'Hypergiant (Ia+)':
            contrast_spot = ImageEnhance.Contrast(fixed_starspots)
            contrast_spot_noise = contrast_spot.enhance(0.35)
            brighter = ImageEnhance.Brightness(contrast_spot_noise)
            spot_noise_new = brighter.enhance(1.55)
            spots = ImageChops.multiply(spot_noise_new, noise_img2b)
            noised = ImageChops.multiply(spot_noise_new, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
        elif type == 'Giant (III)':
            noised_final = ImageChops.multiply(img_new, new_noise)
        elif int(temperature) >= 7500:
            noised_final = ImageChops.multiply(img_new, new_noise)

        else:
            noised = ImageChops.multiply(fixed_starspots, new_noise)
            noised_final = ImageChops.multiply(img_new, noised)
        true_final = ImageChops.multiply(detail_noise_new, noised_final)
        return true_final

sg.theme('DarkGrey6')

#def second_window():



#def getVarFromFile(filename):
#    import imp
#    f = open(filename)
#    global data
#    data = imp.load_source('data', '', f)
#    f.close()

#def third_window():



menu_def = [['Edit', ['Presets', [
            'Real spectra',
            ["Vega (real spectrum)", "Sun (real spectrum)"],

            'Main sequence (V)',
            ['Zeta Ophiuchi', 'Regulus', 'Sirius', 'Tabit', 'Sun', 'Epsilon Eridani', 'Proxima Centauri'],

            'Subgiant (IV)',
            ['14 Cephei', 'Shaula', 'Alhena', 'Procyon', 'Delta Pavonis', 'Rana'],
            
            'Giant (III)',
            ['Hatysa', 'Alcyone', 'Miaplacidus', 'Caph', 'Capella', 'Arcturus', 'Gacrux'],

            'Bright Giant (II)',
            ['Mintaka', 'Sheliak', 'Canopus', 'Sargas', 'Kraz', 'Tarazed', 'Delta Sagittae'],

            'Supergiant (Ib)',
            ['19 Cephei', 'Tseen Ke', 'Aspidiske', 'Mirfak', 'Mebsuta', 'Enif', 'Rasalgethi'],

            'Supergiant (Iab)',
            ['Alnitak', 'Polis', 'Nu Cephei', 'Eta Aquilae', 'Azmidi', 'Omicron1 Cygni', 'Betelgeuse'],

            'Supergiant (Ia)',
            ['Alpha Camelopardalis', 'Rigel', 'Deneb', 'Wezen', 'Y Ophiuchi', '5 Lacertae', 'Mu Cephei'],

            'Hypergiant (Ia+)',
            ['P Cygni', '6 Cassiopeiae', 'IRC +10420', 'V382 Carinae', 'RW Cephei', 'VY Canis Majoris'],

            'Carbon star (C)',
            ['RU Camelopardalis', 'V Arietis', 'La Superba', 'R Leporis'],

            'Wolf-rayet (W)',
            ['Regor', 'R136a1', 'V574 Carinae'],

            #'Luminous blue variable (LBV)',
            #['Pistol Star', 'Eta Carinae', 'S Doradus'],

            'White dwarf (D)',
            ['Sirius B', 'Procyon B', 'Van Maanen 2', 'HZ 21', 'Stein 2051 B', 'WG 44'],

            'Neutron star',
            ['Vela Pulsar', 'Crab Pulsar'],
            
            'All presets',
            ['14 Cephei',
             '19 Cephei',
             '5 Lacertae',
             '6 Cassiopeiae',
             'Alcyone',
             'Alhena',
             'Alnitak',
             'Alpha Camelopardalis',
             'Arcturus',
             'Aspidiske',
             'Azmidi',
             'Betelgeuse',
             'Canopus',
             'Capella',
             'Caph',
             'Crab Pulsar',
             'Delta Pavonis',
             'Delta Sagittae',
             'Deneb',
             'Enif',
             'Epsilon Eridani',
             'Eta Aquilae',
             'Gacrux',
             'Hatysa',
             'HZ 21',
             'IRC +10420',
             'Kraz',
             'La Superba',
             'Mebsuta',
             'Miaplacidus',
             'Mintaka',
             'Mirfak',
             'Mu Cephei',
             'Nu Cephei',
             'Omicron1 Cygni',
             'P Cygni',
             'Polis',
             'Procyon',
             'Procyon B',
             'Proxima Centauri',
             'R136a1',
             'Rana',
             'Rasalgethi',
             'Regor',
             'Regulus',
             'Rigel',
             'R Leporis',
             'RU Camelopardalis',
             'RW Cephei',
             'Sargas',
             'Shaula',
             'Sheliak',
             'Sirius',
             'Sirius B',
             'Stein 2051 B',
             'Sun',
             'Sun (real spectrum)',
             'Tabit',
             'Tarazed',
             'Tseen Ke',
             'V382 Carinae',
             'V574 Carinae',
             'Van Maanen 2',
             'V Arietis',
             'Vega (real spectrum)',
             'Vela Pulsar',
             'VY Canis Majoris',
             'Wezen',
             'WG 44',
             'Y Ophiuchi',
             'Zeta Ophiuchi'],],
            'Custom Presets', ['Create preset...', 'Import preset...', 'Import preset from database...'], 'Reset'], ],
            ['Help', 'About...'], ]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text('Temperature (Kelvin):'), sg.Input(key='Temperature', default_text='5772', enable_events=True)],
    [sg.Text('Radius of star (R☉):'), sg.Input(key='Radius', default_text='1', disabled_readonly_background_color='#bbbbbb', enable_events=True)],
    [sg.Text('Star type (Luminosity class):'), sg.InputCombo(('Main sequence (V)', 'Subgiant (IV)', 'Giant (III)', 'Bright Giant (II)', 'Supergiant (Ib)', 'Supergiant (Iab)', 'Supergiant (Ia)', 'Hypergiant (Ia+)',
                                                              'Carbon star (C)', 'Wolf-rayet (W)', 'White dwarf (D)', 'Neutron star'), size=(25, 1), key='Type', default_value='Main sequence (V)', enable_events=True)],
    [sg.Checkbox('Virtual Texture', default=False, key='TexType')],
    [sg.Text('Texture resolution:'), sg.InputCombo(('1024', '2048', '4096', '8192', '16384'), size=(25, 1), key='TexSize', change_submits=True)],
    [sg.Text('Seed:'), sg.Input(key='Seed', size=(25, 1), default_text='0', enable_events=True), sg.Button('Randomize')],
    [sg.Text('Starspot frequency multiplier:'), sg.Slider(range=(80,120), orientation='horizontal', key='Multiplier', default_value=100, enable_events=True)],
    [sg.Text('Colors:'), sg.InputCombo(('D65', 'Spectrum'), size=(25, 1), key='TexColor', default_value='D65', enable_events=True)],
    #[#sg.Text('Spectrum:'),
    [sg.InputCombo(('None', 'Sun', 'Vega'), size=(25, 1), key='Spectrum', default_value='None', visible=False)],
    [sg.Text('File name:'), sg.Input(key='Filename')],
    [sg.Text('')],
    [sg.Text('Preview:')],
    [sg.Image(r'default.png', key='Preview')],
    [sg.Checkbox('Auto-refresh', default=False, key='Auto')],
    [sg.Button('Refresh'), sg.Button('Generate'), sg.Button('Exit'), sg.Text(size=(25, 1), key='Output')],
    #[sg.Text(size=(15,1),  key='-OUTPUT-', visible=False)],
]

window = sg.Window('Star Texture Generator', layout, icon="icon.ico")
# win2_active=False
while True:
#    ev1, vals1 = window.read(timeout=100)
#    if ev1 == sg.WIN_CLOSED:
#        break
#    window.FindElement('-OUTPUT-').update(vals1[0])
#
#    if ev1 == 'Create preset...'  and not win2_active:
#        win2_active = True
#        window.Hide()
#        layout2 = [
#            [sg.Text('Temperature:'), sg.Input(key='TemperatureCustom', default_text='5772')],
#            [sg.Text('Radius:'), sg.Input(key='RadiusCustom', default_text='1', disabled_readonly_background_color='#bbbbbb')],
#            [sg.Text('Star type:'), sg.InputCombo(('Main sequence (V)', 'Subgiant (IV)', 'Giant (III)', 'Bright Giant (II)', 'Supergiant (Ib)', 'Supergiant (Iab)', 'Supergiant (Ia)', 'Hypergiant (Ia+)',
#                                                   'Carbon star (C)', 'Wolf-rayet (W)', 'White dwarf (D)', 'Neutron star'), size=(25, 1), key='TypeCustom', default_value='Main-sequence (V)', enable_events=True)],
#            [sg.Text('Preset name:'), sg.Input(key='Presetname')],
#            [sg.Button('Save'), sg.Button('Exit')]]
#
#        win2 = sg.Window('Custom preset menu', layout2, icon="icon.ico")
#        while True:
#            ev2, vals2 = win2.read()
#            if ev2 == sg.WIN_CLOSED or ev2 == 'Exit':
#                win2.close()
#                win2_active = False
#                window.UnHide()
#                break
#while True:
    event, values = window.read()
    #window.FindElement('Spectrum').Update(visible=False)
    img_temp = Image.new("RGB", (512, 256), (255, 242, 230))
    draw = ImageDraw.Draw(img_temp)
    img_temp.save("temp.png")

    if event == sg.WIN_CLOSED or event == 'Exit':
        os.remove('temp.png')
        window_has_closed = True
        break

    #if event.startswith('Auto'):
    #if values['Auto'] == True:
        # while values['Auto-refresh'] == True:
        #while True:
            #if event.startswith('Temperature'):
                #if values['Type'] == 'Subgiant (IV)':
                    #true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Subgiant (IV)')
                #elif values['Type'] == 'Giant (III)':
                    #true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Giant (III)')
                #elif values['Spectrum'] == 'None':
                    #true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'])
                #elif values['Spectrum'] == 'Sun':
                    #true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], spectrum=spectra["Sun"])
                #elif values['Spectrum'] == 'Vega':
                    #true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], spectrum=spectra["Vega"])
                #true_final.save("temp.png")
                #window['Preview'].update("temp.png")

    if event == 'Create preset...':
        window.Hide()
        layout2 = [
            [sg.Text('Temperature:'), sg.Input(key='TemperatureCustom', default_text='5772')],
            [sg.Text('Radius:'), sg.Input(key='RadiusCustom', default_text='1', disabled_readonly_background_color='#bbbbbb')],
            [sg.Text('Star type:'), sg.InputCombo(('Main sequence (V)', 'Subgiant (IV)', 'Giant (III)', 'Bright Giant (II)', 'Supergiant (Ib)', 'Supergiant (Iab)', 'Supergiant (Ia)', 'Hypergiant (Ia+)',
                                                    'Carbon star (C)', 'Wolf-rayet (W)', 'White dwarf (D)', 'Neutron star'), size=(25, 1), key='TypeCustom', default_value='Main sequence (V)', enable_events=True)],
            [sg.Text('Preset name:'), sg.Input(key='PresetName')],
            [sg.Button('Save'), sg.Button('Cancel'), sg.Text(size=(25, 1), key='PresetOutput')]]
        
        window2 = sg.Window('Custom preset menu', layout2, icon="icon.ico")
        
        while True:
            event2, values2 = window2.read()
            if event2 == sg.WIN_CLOSED or event2 == 'Cancel':
                break

            if event2.startswith('TypeCustom'):
                if values2['TypeCustom'] == 'Giant (III)' or values2['TypeCustom'] == 'Bright Giant (II)' or values2['TypeCustom'] == 'Supergiant (Ib)' or values2['TypeCustom'] == 'Supergiant (Iab)' or values2['TypeCustom'] == 'Supergiant (Ia)' or values2['TypeCustom'] == 'Hypergiant (Ia+)' or values2['TypeCustom'] == 'Carbon star (C)':
                    window2['RadiusCustom'].update(disabled=True, #background_color='#869A9E',
                                            text_color='#444444')
                else:
                    window2['RadiusCustom'].update(disabled=False, #background_color='#68868C',
                                            text_color='#FFFFFF')
        
            if event2 == "Save":
                if values2['PresetName'] == '':
                    window2['PresetOutput'].update('Error: missing preset name!')
                else:
                    T = "T = "
                    Tinput = values2['TemperatureCustom']
                    R = "\nR = "
                    Rinput = values2['RadiusCustom']
                    Type = "\nType = "
                    Typeinput = values2['TypeCustom']
                    Text = T + Tinput + R + Rinput + Type + Typeinput
                    if not os.path.exists('Custom presets'):
                        os.mkdir('Custom presets')
                        text_file = open("Custom presets/%s.txt" % values2['PresetName'], "w")
                    else:    
                        text_file = open("Custom presets/%s.txt" % values2['PresetName'], "w")
                    text_file.write(Text)
                    text_file.close()
                    window2['PresetOutput'].update('Saved!')
        window2.close()
        window.UnHide()

    if event == 'Import preset...':
        window.Hide()
        layout3 = [
            [sg.In(key='SelectedPreset'), sg.FileBrowse(file_types=(("Presets", "*.txt"),))],
            [sg.Button('Import'), sg.Button('Cancel')]]

        window3 = sg.Window('Select preset', layout3, icon="icon.ico")
        
        while True:
            event3, values3 = window3.read()
            if event3 == sg.WIN_CLOSED or event3 == 'Cancel':
                break

            if event3 == "Import":
                path = values3['SelectedPreset']
                #path = path.replace("/", "\\")
                lst = []
                with open(path) as fo:
                    lines = fo.read().splitlines()
                for line in lines:
                    a,b = line.split(" = ")
                    lst.append((a,b))
                data = dict(lst)
                #print(data)
                window.FindElement('Temperature').Update(data["T"])
                window.FindElement('Radius').Update(data["R"])
                window.FindElement('Type').Update(data["Type"])
                if data["Type"] == 'Subgiant (IV)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Subgiant (IV)')
                elif data["Type"] == 'Giant (III)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Giant (III)')
                elif data["Type"] == 'Bright Giant (II)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Bright Giant (II)')
                elif data["Type"] == 'Supergiant (Ib)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Supergiant (Ib)')
                elif data["Type"] == 'Supergiant (Iab)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Supergiant (Iab)')
                elif data["Type"] == 'Supergiant (Ia)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Supergiant (Ia)')
                elif data["Type"] == 'Hypergiant (Ia+)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Hypergiant (Ia+)')
                elif data["Type"] == 'Carbon star (C)':
                    window['Radius'].update(disabled=True, text_color='#444444')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'], type='Carbon star (C)')
                else:
                    window['Radius'].update(disabled=False, text_color='#FFFFFF')
                    true_final = create_noise(512, data["T"], data["R"], values['TexColor'])
                true_final.save("temp.png")
                window['Preview'].update("temp.png")
                break
                
                #preset = open(values['SelectedPreset'], "r+")
                #print(preset.read())
                #print(path)
                #getVarFromFile(path)
                #print(data.R)
                #print(data.T)
                #print(data.Type)
        window3.close()
        window.UnHide()

    if event.startswith('Type'):
        if values['Type'] == 'Giant (III)' or values['Type'] == 'Bright Giant (II)' or values['Type'] == 'Supergiant (Ib)' or values['Type'] == 'Supergiant (Iab)' or values['Type'] == 'Supergiant (Ia)' or values['Type'] == 'Hypergiant (Ia+)' or values['Type'] == 'Carbon star (C)':
            window['Radius'].update(disabled=True, #background_color='#869A9E',
                                    text_color='#444444')
        else:
            window['Radius'].update(disabled=False, #background_color='#68868C',
                                    text_color='#FFFFFF')

    if event == 'About...':
        window.disappear()
        sg.popup('About this program:', "This is a program that generates star textures for use in Celestia or whatever program you like. It's still a work-in-progress and the code is pretty messy.",
                 '', 'Current version: Version Beta 1.0')
        window.reappear()

    if event == 'Sun (real spectrum)':
        window.FindElement('Temperature').Update(5772)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        window.FindElement('Spectrum').Update('Sun')
        true_final = create_noise(512, 5772, 1, values['TexColor'], spectrum=spectra["Sun"])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Vega (real spectrum)':
        window.FindElement('Temperature').Update(9602)
        window.FindElement('Radius').Update(2.818)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        window.FindElement('Spectrum').Update('Vega')
        true_final = create_noise(512, 9602, 1, values['TexColor'], spectrum=spectra["Vega"])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Vega (blackbody spectrum)':
        window.FindElement('Temperature').Update(9602)
        window.FindElement('Radius').Update(2.818)
        true_final = create_noise(512, 9602, 1, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
            
    if event == 'Zeta Ophiuchi':
        window.FindElement('Temperature').Update(34000)
        window.FindElement('Radius').Update(8.5)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 34000, 8.5, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Regulus':
        window.FindElement('Temperature').Update(12460)
        window.FindElement('Radius').Update(3.092)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 12460, 3.092, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Sirius':
        window.FindElement('Temperature').Update(9940)
        window.FindElement('Radius').Update(1.711)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 9940, 1.711, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Tabit':
        window.FindElement('Temperature').Update(6516)
        window.FindElement('Radius').Update(1.323)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 6516, 1.323, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Sun':
        window.FindElement('Temperature').Update(5772)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 5772, 1, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Epsilon Eridani':
        window.FindElement('Temperature').Update(5084)
        window.FindElement('Radius').Update(0.735)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 5084, 0.735, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Proxima Centauri':
        window.FindElement('Temperature').Update(3042)
        window.FindElement('Radius').Update(0.1542)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 3042, 0.1542, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == '14 Cephei':
        window.FindElement('Temperature').Update(32000)
        window.FindElement('Radius').Update(11.7)
        window.FindElement('Type').Update('Subgiant (IV)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 32000, 11.7, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Shaula':
        window.FindElement('Temperature').Update(25000)
        window.FindElement('Radius').Update(8.8)
        window.FindElement('Type').Update('Subgiant (IV)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 25000, 8.8, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Alhena':
        window.FindElement('Temperature').Update(9260)
        window.FindElement('Radius').Update(3.3)
        window.FindElement('Type').Update('Subgiant (IV)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 9260, 3.3, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Procyon':
        window.FindElement('Temperature').Update(6530)
        window.FindElement('Radius').Update(2.048)
        window.FindElement('Type').Update('Subgiant (IV)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 6530, 2.048, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Delta Pavonis':
        window.FindElement('Temperature').Update(5604)
        window.FindElement('Radius').Update(1.22)
        window.FindElement('Type').Update('Subgiant (IV)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 5604, 1.22, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Rana':
        window.FindElement('Temperature').Update(5055)
        window.FindElement('Radius').Update(2.327)
        window.FindElement('Type').Update('Subgiant (IV)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 5055, 2.327, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Hatysa':
        window.FindElement('Temperature').Update(32500)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 32500, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Alcyone':
        window.FindElement('Temperature').Update(12258)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 12258, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Miaplacidus':
        window.FindElement('Temperature').Update(8866)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 8866, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Caph':
        window.FindElement('Temperature').Update(7079)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 7079, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Capella':
        window.FindElement('Temperature').Update(4970)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4970, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Arcturus':
        window.FindElement('Temperature').Update(4286)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4286, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Gacrux':
        window.FindElement('Temperature').Update(3689)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Giant (III)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3689, 1, values['TexColor'], type='Giant (III)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Mintaka':
        window.FindElement('Temperature').Update(29500)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 29500, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Sheliak':
        window.FindElement('Temperature').Update(13300)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 13300, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Canopus':
        window.FindElement('Temperature').Update(7400)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 7400, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Sargas':
        window.FindElement('Temperature').Update(7268)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 7268, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Kraz':
        window.FindElement('Temperature').Update(5100)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 5100, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Tarazed':
        window.FindElement('Temperature').Update(4210)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4210, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Delta Sagittae':
        window.FindElement('Temperature').Update(3660)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Bright Giant (II)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3660, 1, values['TexColor'], type='Bright Giant (II)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == '19 Cephei':
        window.FindElement('Temperature').Update(32983)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 32983, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Tseen Ke':
        window.FindElement('Temperature').Update(14600)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 14600, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Aspidiske':
        window.FindElement('Temperature').Update(7500)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 7500, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Mirfak':
        window.FindElement('Temperature').Update(6350)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 6350, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Mebsuta':
        window.FindElement('Temperature').Update(4662)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4662, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Enif':
        window.FindElement('Temperature').Update(4379)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4379, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Rasalgethi':
        window.FindElement('Temperature').Update(3280)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ib)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3280, 1, values['TexColor'], type='Supergiant (Ib)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Alnitak':
        window.FindElement('Temperature').Update(29500)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 29500, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Polis':
        window.FindElement('Temperature').Update(12000)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 12000, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Nu Cephei':
        window.FindElement('Temperature').Update(8800)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 8800, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Eta Aquilae':
        window.FindElement('Temperature').Update(6000)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 6000, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Azmidi':
        window.FindElement('Temperature').Update(4880)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4880, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Omicron1 Cygni':
        window.FindElement('Temperature').Update(4043)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 4043, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Betelgeuse':
        window.FindElement('Temperature').Update(3500)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Iab)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3500, 1, values['TexColor'], type='Supergiant (Iab)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Alpha Camelopardalis':
        window.FindElement('Temperature').Update(30000)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 30000, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Rigel':
        window.FindElement('Temperature').Update(12100)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 12100, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Deneb':
        window.FindElement('Temperature').Update(8525)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 8525, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Wezen':
        window.FindElement('Temperature').Update(6390)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 6390, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'Y Ophiuchi':
        window.FindElement('Temperature').Update(5250)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 5250, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == '5 Lacertae':
        window.FindElement('Temperature').Update(3713)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3713, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Mu Cephei':
        window.FindElement('Temperature').Update(3551)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Supergiant (Ia)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3551, 1, values['TexColor'], type='Supergiant (Ia)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'P Cygni':
        window.FindElement('Temperature').Update(18700)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Hypergiant (Ia+)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 18700, 1, values['TexColor'], type='Hypergiant (Ia+)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == '6 Cassiopeiae':
        window.FindElement('Temperature').Update(10023)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Hypergiant (Ia+)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 10023, 1, values['TexColor'], type='Hypergiant (Ia+)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'IRC +10420':
        window.FindElement('Temperature').Update(7930)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Hypergiant (Ia+)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 7930, 1, values['TexColor'], type='Hypergiant (Ia+)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'V382 Carinae':
        window.FindElement('Temperature').Update(5625)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Hypergiant (Ia+)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 5625, 1, values['TexColor'], type='Hypergiant (Ia+)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'RW Cephei':
        window.FindElement('Temperature').Update(3956)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Hypergiant (Ia+)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3956, 1, values['TexColor'], type='Hypergiant (Ia+)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'VY Canis Majoris':
        window.FindElement('Temperature').Update(3490)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Hypergiant (Ia+)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3490, 1, values['TexColor'], type='Hypergiant (Ia+)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'RU Camelopardalis':
        window.FindElement('Temperature').Update(5250)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Carbon star (C)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 5250, 1, values['TexColor'], type='Carbon star (C)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'V Arietis':
        window.FindElement('Temperature').Update(3540)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Carbon star (C)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 3540, 1, values['TexColor'], type='Carbon star (C)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if event == 'La Superba':
        window.FindElement('Temperature').Update(2750)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Carbon star (C)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 2750, 1, values['TexColor'], type='Carbon star (C)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'R Leporis':
        window.FindElement('Temperature').Update(2290)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Carbon star (C)')
        window['Radius'].update(disabled=True, text_color='#444444')
        true_final = create_noise(512, 2290, 1, values['TexColor'], type='Carbon star (C)')
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Reset':
        window.FindElement('Temperature').Update(5772)
        window.FindElement('Radius').Update(1)
        window.FindElement('Type').Update('Main sequence (V)')
        window['Radius'].update(disabled=False, text_color='#FFFFFF')
        true_final = create_noise(512, 5772, 1, values['TexColor'])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")
        
    if values['TexType'] == True:
        window.FindElement('TexSize').Update(values=('16384','32768','65536'))
    else:
        window.FindElement('TexSize').Update(values=('1024', '2048', '4096', '8192', '16384'))

    if event == 'Randomize':
        window.FindElement('Seed').Update(random.randint(-20000,20000))
    if event == 'Refresh':
        if values['Type'] == 'Subgiant (IV)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Subgiant (IV)')
        elif values['Type'] == 'Giant (III)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Giant (III)')
        elif values['Type'] == 'Bright Giant (II)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Bright Giant (II)')
        elif values['Type'] == 'Supergiant (Ib)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Supergiant (Ib)')
        elif values['Type'] == 'Supergiant (Iab)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Supergiant (Iab)')
        elif values['Type'] == 'Supergiant (Ia)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Supergiant (Ia)')
        elif values['Type'] == 'Hypergiant (Ia+)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Hypergiant (Ia+)')
        elif values['Type'] == 'Carbon star (C)':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], type='Carbon star (C)')
        elif values['Spectrum'] == 'None':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'])
        elif values['Spectrum'] == 'Sun':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], spectrum=spectra["Sun"])
        elif values['Spectrum'] == 'Vega':
            true_final = create_noise(512, values['Temperature'], values['Radius'], values['TexColor'], spectrum=spectra["Vega"])
        true_final.save("temp.png")
        window['Preview'].update("temp.png")

    if event == 'Generate':
        window['Output'].update('Texture generating...')
        if values['Temperature'] == '':
            window['Output'].update('Error: missing temperature!')
        elif values['TexSize'] == '':
            window['Output'].update('Error: missing texture resolution!')
        else:
            size = round(eval(values['TexSize']))
            if values['Type'] == 'Subgiant (IV)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Subgiant (IV)')
            elif values['Type'] == 'Giant (III)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Giant (III)')
            elif values['Type'] == 'Bright Giant (II)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Bright Giant (II)')
            elif values['Type'] == 'Supergiant (Ib)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Supergiant (Ib)')
            elif values['Type'] == 'Supergiant (Iab)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Supergiant (Iab)')
            elif values['Type'] == 'Supergiant (Ia)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Supergiant (Ia)')
            elif values['Type'] == 'Hypergiant (Ia+)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Hypergiant (Ia+)')
            elif values['Type'] == 'Carbon star (C)':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], type='Carbon star (C)')
            elif values['Spectrum'] == 'None':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'])
            elif values['Spectrum'] == 'Sun':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], spectrum=spectra["Sun"])
            elif values['Spectrum'] == 'Vega':
                true_final = create_noise(size, values['Temperature'], values['Radius'], values['TexColor'], spectrum=spectra["Vega"])
                
            if values['Filename'] == '':
                #window['Output'].update('Error: missing filename!')
                STG = 'StarTex'
                dash = '-'
                Sn = values['Seed']
                St = values['Temperature']
                Sr = values['Radius']
                if values['Type'] == 'Main sequence (V)':
                    Stype = '1'
                elif values['Type'] == 'Subgiant (IV)':
                    Stype = '2'
                elif values['Type'] == 'Giant (III)':
                    Stype = '3'
                elif values['Type'] == 'Bright Giant (II)':
                    Stype = '4'
                elif values['Type'] == 'Supergiant (Ib)':
                    Stype = '5'
                elif values['Type'] == 'Supergiant (Iab)':
                    Stype = '6'
                elif values['Type'] == 'Supergiant (Ia)':
                    Stype = '7'
                elif values['Type'] == 'Hypergiant (Ia+)':
                    Stype = '8'
                elif values['Type'] == 'Carbon star (C)':
                    Stype = '9'
                elif values['Type'] == 'Wolf-rayet (W)':
                    Stype = '10'
                elif values['Type'] == 'White dwarf (D)':
                    Stype = '11'
                elif values['Type'] == 'Neutron star':
                    Stype = '12'

                if values['TexColor'] == 'D65':
                    Stc = '1'
                elif values['TexColor'] == 'Spectrum':
                    Stc = '2'
                Str = values['TexSize']
                name = STG + dash + Sn + dash + St + dash + Sr + dash + Stype + dash + Stc + dash + Str
                true_final.save('%s.png' % name)
            else:
                true_final.save('%s.png' % values['Filename'])
            window['Output'].update('Texture generated!')
window.close()
#window3.close()
