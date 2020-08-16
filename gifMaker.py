import numpy as np 
import sys
sys.path.append('..')
import glob
import moviepy.editor as mpy

gif_name = 'styleTransform'
fpsFast = 12

# Make the Gif
path = "C:/Users/benjj/Pictures/gifs2/*.png"
file_list = glob.glob(path)
list.sort(file_list, key = lambda x: int(x.split('_')[1].split('.png')[0]))
clip = mpy.ImageSequenceClip(file_list, fps = fpsFast) 
clip.write_gif('{}.gif'.format(gif_name), fps=fpsFast)
