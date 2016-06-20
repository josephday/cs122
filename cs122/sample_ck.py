# CS122 W'16: Treemaps
# Sample use of Color_Key

import Chi_Canvas
import Color_Key

def go():
    # create a canvas
    c = Chi_Canvas.Chi_Canvas(10, 10)

    # create a color key
    ck = Color_Key.Color_Key(set(["Streets/Roads", "Water", "Airports"]))

    # draw the color key
    ck.draw_color_key(c,.8,0,1.0,.30)

    # show it
    c.show()

if __name__=="__main__":
    go()
