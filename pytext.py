# MIT License
#
# Copyright (c) 2020 Russ Hughes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
@micropython.native
def displine(disp,x1,y1,x2,y2):
    #    // general purpose line
    #// lines are either "shallow" or "steep" based on whether the x delta
    #// is greater than the y delta
    dx = x2 - x1;
    dy = y2 - y1;
    if dx == 0 & dy == 0:
        disp.pixel(x1,y1)
        return
    
    shallow = abs(dx) > abs(dy)
    if shallow:
        s = abs(dx);       #// number of steps
        sx = -1 if dx < 0 else 1;   #// x step value
        sy = (dy << 16) / s;    #// y step value in fixed 16:16
        x = x1;
        y = int(y1 << 16);
        while s:
            disp.pixel(x, int(y) >> 16);
            y += sy;
            x += sx;
            s -= 1
      
    else:
        #// steep version
        s = abs(dy);       #// number of steps
        sy = -1 if dy < 0 else 1;   #// y step value
        sx = (dx << 16) / s;    #// x step value in fixed 16:16
        y = y1;
        x = int(x1 << 16);
        while s:
            disp.pixel(int(x) >> 16, y);
            y += sy;
            x += sx;
            s -= 1

def text(display, font, message, row=32, column=0):
    '''
    Write `text` on `display` starting on `row` stating in `column` using
    `font` in `color`

    Args:
        display: The display device to write on
        font: The pyfont module to use
        message: The message to write
        row: Row to start at, defaults to 32
        column: Column to start at, defaults to 0
        color: The color to write in
    '''
    from_x = to_x = pos_x = column
    from_y = to_y = pos_y = row

    for char in [ord(char) for char in message]:
        penup = True
        if 32 <= char <= 127:
            data = bytearray(font.get_ch(char))
            length = data[0]
            left = data[1] - 0x52
            right = data[2] - 0x52
            width = right - left

            for vect in range (3, len(data), 2):
                vector_x = data[vect] - 0x52
                vector_y = data[vect+1] - 0x52

                if vector_x == -50:
                    penup = True
                    continue

                if not vect or penup:
                    from_x = pos_x + vector_x - left
                    from_y = pos_y + vector_y
                else:
                    to_x = pos_x + vector_x - left
                    to_y = pos_y + vector_y

                    displine(display, from_x, from_y, to_x, to_y)

                    from_x = to_x
                    from_y = to_y
                penup = False

            pos_x += width
