import numpy as np
from bokeh.io import curdoc, show
from bokeh.models.widgets import Slider, TextInput
import colorsys
import yaml
from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Slider
from bokeh.plotting import figure, output_notebook, show, curdoc
from bokeh.themes import Theme

def generate_color_range(N, I, wl):
    HSV_tuples = [( WavelengthToHue(wl), .7, x) for x in I/np.amax(I) ]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    for_conversion = []
    for RGB_tuple in RGB_tuples:
        for_conversion.append((int(RGB_tuple[0]*255), int(RGB_tuple[1]*255), int(RGB_tuple[2]*255)))
    hex_colors = [ rgb_to_hex(RGB_tuple) for RGB_tuple in for_conversion ]
    return hex_colors, for_conversion

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
def WavelengthToHue(wl):
    fromthecenter = abs(wl - 535)
    if wl > 535:
        wl = wl - (fromthecenter * 2)
    else:
        wl = wl + (fromthecenter * 2)
        
        
    numerator = .7 * (wl - 450)
    result = numerator / 170
    
    
    if result < 0:
        result = 0
    elif result > .7:
        result = .7
    
    return result
#        (.8-0)(x - 450)
# f(x) = --------------  + 0 
#           620 - 450

def intensity(x, w, a):
    result = 0
    
    sinofx = np.sin(x)
    num = np.pi * a * sinofx / w
    numerator = np.sin(num)
    fraction = numerator / num 
    result = fraction ** 2
    
    return result
    

# Set up data
x = np.linspace(-1, 1, 3000 )
y = np.cos(x)
source = ColumnDataSource(data=dict(x=x, y=y))


#other plot
brightness = y # change to have brighter/darker colors
crcolor, crRGBs = generate_color_range(1000,brightness, 1 )
cry = [ 5 for i in range(len(x)) ]
crsource = ColumnDataSource(data=dict(x=x, y=cry, crcolor=crcolor, RGBs=crRGBs))



p2 = figure( x_range=(0,10), 
            y_range=(x[0],x[-1]),
            plot_width=150, plot_height=400,
            title='Intensity Distribution', tools="reset,save")

color_range1 = p2.rect(x='y' , y='x', width=10, height=x[1] - x[0],
                       color='crcolor', source=crsource)
p2.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
p2.xaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
p2.xaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

p2.yaxis.axis_label = "Distance (m)"
# Set up plot
plot = figure(y_range=(x[0],x[-1]), plot_height=400, plot_width=200, title="Intensity Distribution",
              tools="crosshair,reset,save",
               x_range=[-0.5, 7.0])
plot.yaxis.axis_label = "Distance (m)"
plot.xaxis.axis_label = "Intensity (V^2/m^2)"
plot.xaxis.minor_tick_line_color = None  # turn off y-axis minor ticks


plot.line('y', 'x', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
electricfield = Slider(title="Initial electric field (V/m)", value=1.0, start=0.0, end=5.0, step=0.1)
wavelength = Slider(title="Wavelength (nm)", value=400, start=400, end=700, step=5.0)
distance = Slider(title="Distance Between Slits (nm)", value=500, start=500, end=5000, step=50)
length = Slider(title="Distance between slits and screen (m)", value=1.0, start=0.0, end=5.0, step=0.1)
slits = Slider(title="Number of Slits", value=2.0, start=2.0, end=10, step=1.0)
width = Slider(title="Width of slits (nm)", value=400, start=400, end=700, step=5)




def update_data(attrname, old, new):

    # Get the current slider values
    i = electricfield.value
    w = wavelength.value
    d = distance.value
    L = length.value
    s = slits.value
    a = width.value
    
    w = w * (10**-9)
    d = d * (10**-9)
    a = a * (10**-9)
    x = np.linspace(-1, 1, 3000)
 
    num = (s - 1)*d
    startingPoint = -1 * (num/2)
    slitArray = np.arange(s)
    sA = slitArray * d + startingPoint

    

    rsquared = L**2 + ( x[:,None] - sA[None,:] )**2
    r = rsquared ** 0.5
    k = np.pi * 2 / w

        
    sinofkr = np.sin(k*r)
    sinfield = i * np.sum(sinofkr, axis = 1)

    
    cosofkr = np.cos(k*r)
    cosfield = i * np.sum(cosofkr, axis = 1)
    result = cosfield ** 2 + sinfield ** 2
    
    theInt = intensity(x, w, a)
    
        
    y = (result / 2) * theInt

    source.data = dict(x=x, y=y)
    
    #------------------------------------------
    
    brightness = y # change to have brighter/darker colors
    crcolor, crRGBs = generate_color_range(1000,brightness, w / 10**-9) # produce spectrum

    crx = x 
    cry = [ 5 for i in range(len(crx)) ]
    
    crsource.data = dict(x=crx, y=cry, crcolor=crcolor, RGBs=crRGBs)


for i in [electricfield, wavelength, distance, length, slits, width]:
    i.on_change('value', update_data)

    

inputs = widgetbox( electricfield, wavelength, distance, length, slits, width)

curdoc().add_root(row(inputs, plot, p2, width=800))
curdoc().title = "Intensity Distribution"



