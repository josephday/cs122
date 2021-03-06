import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import matplotlib.pylab as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.transforms import Bbox, TransformedBbox
import numpy as np
import os
import tempfile


class Chi_Canvas:


    def __init__(self, xscale=10, yscale=10, title="TreeMap"):
        '''
        initialize a Chi_Canvas
        '''
        plt.close('all')

        # Get the renderer through a hack
        fig = plt.figure()
        fig.add_subplot(111)
        with tempfile.NamedTemporaryFile(suffix='png', delete=True) as tmp_file:
            fig.savefig(tmp_file)
            self._renderer = plt.gca().get_renderer_cache()
        plt.close('all')

        self._figure, self._ax = plt.subplots(figsize=(xscale, yscale))
        self._figure.canvas.set_window_title(title)
        self._figure.patch.set_facecolor('white')
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        self._ax.set_axis_off()


    def draw_rectangle(self, x0, y0, x1, y1, fill='blue', outline='black'):
        '''
        draw a rectangle in the canvas at the specified coordinates with the
        given style
        (x0, y0): coordinates of top left corner
        (x1, y1): coordinates of bottom right corner
        fill: color with which to fill rectangle
        outline: color for border of rectangle
        '''
        rect = mpatches.Rectangle([x0, y0], x1-x0, y1-y0, facecolor=fill,
                                  linewidth=1, linestyle='solid',
                                  edgecolor=outline)
        self._ax.add_patch(rect)


    def draw_text(self, x0, y0, w, txt, fg="black", debug=False):
        '''
        draw text txt horizontally at specified (x0, y0) coordinates
        max width w, color fg
        '''
        # -w/2.0 + 0.02
        self._draw_text_with_rotation(x0, y0, w, 0.03, txt,
                                      offset_x=-w/2.0+0.075, fg=fg, rotation=0,
                                      debug=debug)
        

    def draw_text_vertical(self, x0, y0, h, txt, fg="black", debug=False):
        '''
        draw text txt vertically at specified (x0, y0) coordinates
        max height h, color fg
        '''
        self._draw_text_with_rotation(x0, y0, 0.03, h, txt, offset_y=h/2.0-0.02,
                                      fg=fg, rotation=90, debug=debug)


    def show(self):
        '''
        display the canvas on screen
        '''
        # Draw only the unit box and flip the y axis
        plt.xlim((0, 1))
        plt.ylim((1, 0))

        self._figure.canvas.mpl_connect('draw_event', Chi_Canvas._on_draw)

        plt.show()


    def savefig(self,filename):
        '''
        save the canvas as an image file at filename)
        '''
        # Draw only the unit box and flip the y axis
        plt.xlim((0, 1))
        plt.ylim((1, 0))

        Chi_Canvas._on_draw(fig=self._figure, renderer=self._renderer)

        self._figure.savefig(filename)


    def close(self):
        '''
        clean up a canvas
        '''
        plt.close()


    # Auxiliary functions


    def _draw_text_with_rotation(self, x0, y0, w, h, txt, offset_x=0,
                                 offset_y=0, fg="black", rotation=0,
                                 debug=False):
        '''
        draw text txt at coordinates (x0, y0) and width w, height h
        (additional x offset offset_x and y offset offset_y if desired)
        with rotation and color fg
        '''
        if debug:
            self.draw_rectangle(x0-w/2.0, y0-h/2, x0+w/2.0, y0+h/2.0,
                                fill='none', outline='red')
        clip_rect = mpatches.Rectangle(xy=[x0-w/2.0, y0-h/2.0], width=w,
                                       height=0.1, transform=self._ax.transData)
        textobj = plt.text(x0 + offset_x, y0 + offset_y, txt, color=fg,
                           ha='left', va='center', clip_path=clip_rect,
                           clip_on=True, rotation=rotation)
        # Let's store the clipping box in the object, so that we can use it
        # when clipping text
        textobj._clip = TransformedBbox(bbox=Bbox(((x0-w/2.0, y0-h/2.0),
                                        (x0+w/2, y0+h/2.0))),
                                        transform=self._ax.transData)
        textobj.set_rotation_mode('anchor')


    @classmethod
    def _auto_ellipsis_text(cls, textobj, renderer):
        '''
        abbreviate text with ellipsis if necessary
        '''
        try:
            clip = textobj._clip
        except AttributeError:
            return 

        x0, y0 = textobj.get_transform().transform(textobj.get_position())
        textobj.set_rotation_mode('anchor')
        rotation = textobj.get_rotation()

        if rotation == 90:
            buf = abs(y0 - clip.y1)
            new_width = abs(clip.y1 - clip.y0) - 2*buf
        else:
            buf = abs(x0 - clip.x0)
            new_width = abs(clip.x0 - clip.x1) - 2*buf

        fontsize = textobj.get_size()
        pixels_per_char = 0.5 * renderer.points_to_pixels(fontsize)

        try:
            txt = textobj._old_text
        except:
            txt = textobj.get_text()
            textobj._old_text = txt

        wrap_width = new_width // pixels_per_char
        wrapped_text = txt
        clip_char = max(0, int(wrap_width*0.9))
        if clip_char < len(wrapped_text)-3:
            wrapped_text = txt[:clip_char] + '...'
        textobj.set_text(wrapped_text)


    @classmethod
    def _on_draw(cls, event=None, fig=None, renderer=None):
        '''
        Automatically put ellipsis after overflowing text
        '''
        if event is not None:
            fig = event.canvas.figure
            renderer = event.renderer
            
        for ax in fig.axes:
            for artist in ax.get_children():
                if isinstance(artist, mpl.text.Text):
                    cls._auto_ellipsis_text(artist, renderer)

        if event is not None:
            func_handles = fig.canvas.callbacks.callbacks[event.name]
            fig.canvas.callbacks.callbacks[event.name] = {}
            fig.canvas.draw()
            fig.canvas.callbacks.callbacks[event.name] = func_handles
