# CS122 W'16: Treemaps
# Color Key class


import matplotlib as mpl
import numpy as np
import Chi_Canvas

class Color_Key:


    NCOLORS = 256 
    # Creates a color wheel of nice pastel colors
    COLORS = mpl.colors.hsv_to_rgb(np.vstack([
        np.linspace(0, 1, NCOLORS), # Hue
        0.4 * np.ones(NCOLORS),     # Saturation
        1.0 * np.ones(NCOLORS)      # Value
    ]).T[np.newaxis])[0]

    def __init__(self, tags):
        '''
        construct a Color_Key with given tags
        '''
        self.color_map = {}
        incr = self.NCOLORS//len(tags)
        index = 0
        for t in tags:
            self.color_map[t] = Color_Key.COLORS[index]
            index = index + incr


    def get_color(self, t):
        '''
        get color for tag t
        '''
        if t in self.color_map:
            return self.color_map[t]
        return 'gray' 


    def get_color_by_index(self, i):
        '''
        get color i spaces into list
        '''
        return self.color_map.keys()[i]


    def draw_color_key(self, canvas, x0, y0, x1, y1):
        '''
        draw color key in canvas from top-left corner (x0, y0) to
        bottom-right corner (x1, y1)
        '''
        h = abs(y1-y0)
        w = abs(x1-x0)
        keys = self.color_map.keys()
        hincr = h/(len(keys)*1.0)
        y = y0
        items = [i for i in self.color_map.items()]
        items.sort()
        for (key, color) in items:
            canvas.draw_rectangle(x0, y, x1, y+hincr, fill=color)
            canvas.draw_text(x0+w/2, y+hincr/2, w*.95, key)
            y = y + hincr

