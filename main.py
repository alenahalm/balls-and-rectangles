from collections import defaultdict
from re import T
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from skimage.measure import label, regionprops
from skimage import color

def count_colors(colors):    
    cur_index = 1
    colours=defaultdict(lambda:0)
    diff = np.diff(colors)
    delta = np.std(diff) * 2
    for i in range(1, len(colors)):
        if colors[i] - colors[i-1] >= delta:
            cur_index += 1
        colours[cur_index] += 1
    return colours

image = plt.imread('balls_and_rects.png')
hsv = color.rgb2hsv(image)
binary = image.sum(2)
binary[binary > 0] = 1

labeled = label(binary)

regions = regionprops(labeled)

print(labeled.max(), end=' objects\n')

props_balls = []
props_rects = []

for region in regions:
    if region.eccentricity == 0:
        props_balls.append(region)
    else:
        props_rects.append(region)

colors_balls=[]
colors_rects=[]

for region in regions:
    cy, cx = region.centroid
    colour = hsv[int(cy), int(cx)][0]
    if region in props_balls:
        colors_balls.append(colour)
    else:
        colors_rects.append(colour)

colors_balls.sort()
colors_rects.sort()

balls = count_colors(colors_balls)
rects = count_colors(colors_rects)

for i in balls.keys():
    print(f"Color {i}: {balls[i]} balls, {rects[i]} rectangles")
