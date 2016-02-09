#!/usr/bin/env python3
# coding: utf-8

# Created by Louis ETIENNE

import math

try:
    import simpleSVG
except Exception as e:
    print("Le fichier 'simpleSVG.py' doit être au même emplacement que ce fichier.")
    print("Pour le télécharger : http://12characters.net/simpleSVG/")
    exit(0)

RESOLUTION = 600
OUTPUT_NAME = 'output'

def to_global_coords(n):
    return math.floor((n+1) * (RESOLUTION/2))

def to_x(n):
    return math.sin(n * 2 * math.pi)


def to_y(n):
    return math.cos(n * 2 * math.pi)


def to_coords(n):
    return {'x': to_x(n), 'y': to_y(n)}


def build_circle(modulo, factor):
    # Calcule les coordonnées des lignes
    chords = []
    for index in range(modulo):
        chords.append({ 'start': to_coords(float(index) / modulo), 
                        'end': to_coords(((factor * float(index)) % modulo) / modulo) })
    return chords


def build_image(modulo, factor, reverse=True, text=True):
    stroke = 'black'
    circle = build_circle(modulo, factor)

    if reverse:
        draw = simpleSVG.svg_class(fname="{}.svg".format(OUTPUT_NAME), bbx=RESOLUTION, bby=RESOLUTION, whiteback=False)
        draw.rect(0, 0, RESOLUTION, RESOLUTION, fill='black') 
        stroke = 'white'
    else:
        draw = simpleSVG.svg_class(fname="{}.svg".format(OUTPUT_NAME), bbx=RESOLUTION, bby=RESOLUTION)
    draw.scale()

    draw.circle(.5, .5, 300, stroke=stroke, stroke_width=1)

    if text:
        draw.text(10, RESOLUTION - 10, 0, 'Modulo : %d, Facteur : %.2f' % (modulo, factor), stroke=stroke)

    for chord in circle:
        draw.line(to_global_coords(chord['start']['x']), to_global_coords(chord['start']['y']),
                  to_global_coords(chord['end']['x']), to_global_coords(chord['end']['y']),
                  stroke=stroke, stroke_width=1)

    draw.close()
    return draw


def save_image_to_png(path):
    try:
        import cairosvg
    except Exception as e:
        print("Vous devez installer 'cairosvg' pour pouvoir enregistrer votre image.")
        print("Pour en savoir plus : http://cairosvg.org/")
        exit(0)

    cairosvg.svg2png(url='{}.svg'.format(OUTPUT_NAME), write_to=path)


if __name__ == '__main__':
    while True:
        modulo = int(input("Entrez le modulo : "))
        factor = float(input("Entrez le facteur : "))

        draw = build_image(modulo, factor)
        draw.display()
