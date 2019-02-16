#
# themes.py
#
# author: caustik
# desc: generate ableton themes
# 

from lxml import html as Html
from lxml import etree

import multiprocessing, collections, contextlib, subprocess, threading, platform, requests, argparse, ctypes, psutil, math, time, json, sys, os, io, re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

THEME_FILE_INP = "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\Themes\\00Light.ask"
THEME_FILE_OUT = "C:\\ProgramData\\Ableton\\Live 10 Suite\\Resources\\Themes\\PG {}.ask"

COLORS = 154

THEMES = [
    {
        "name": "CubeHelix",
        "colors": sns.cubehelix_palette(start=2.8, rot=.1, n_colors=COLORS)
    }
]

#for name in plt.colormaps():
for name in [ 'viridis', 'plasma', 'inferno', 'magma', 'cividis' 
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn' ]:
    try:
        THEMES.append( {
            "name": "{}".format(name),
            "colors": sns.color_palette("{}".format(name), n_colors=COLORS)
        })
    except:
        pass


class CommandLine:
    def __init__(self):
        # prepare command line argument parser
        commands = [ "generate" ]
        arg_parser = argparse.ArgumentParser(description="generate ableton palettes", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        arg_parser.add_argument('-c', dest='command', choices=commands, required=False, default="generate", help='command')
        # parse command line arguments
        self.args = arg_parser.parse_args()
        # execute command
        getattr(globals()['CommandLine'], self.args.command)(self)

    def generate(self):
        for theme in THEMES:
            with open(THEME_FILE_INP, "rb") as xml:
                tree = etree.parse(xml)
                R = tree.xpath('//R')
                G = tree.xpath('//G')
                B = tree.xpath('//B')
                sorted = []
                for i in range(COLORS):
                    r = float(R[i].attrib["Value"]) / 255
                    g = float(G[i].attrib["Value"]) / 255
                    b = float(B[i].attrib["Value"]) / 255
                    p = math.sqrt(0.2999 * r * r + 0.587 * g * g + 0.114 * b *b)
                    sorted.append( (p, i) )
                sorted.sort(key = lambda x: x[0])
                sorted.reverse()
                colors = theme["colors"]
                for i in range(COLORS):
                    r = colors[i][0]
                    g = colors[i][1]
                    b = colors[i][2]
                    R[sorted[i][1]].attrib["Value"] = str(int(r * 255))
                    G[sorted[i][1]].attrib["Value"] = str(int(g * 255))
                    B[sorted[i][1]].attrib["Value"] = str(int(b * 255))
                #sns.palplot(colors)
            with open(THEME_FILE_OUT.format(theme["name"]), "wb") as output:
                tree.write(output, pretty_print=True, xml_declaration=True, encoding='utf-8')
                #plt.savefig(theme["name"] + ".png", dpi=400)

if __name__ == "__main__":
    themes = CommandLine()
