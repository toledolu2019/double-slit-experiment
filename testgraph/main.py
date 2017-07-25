import numpy as np
from bokeh.io import curdoc, show
from bokeh.models.widgets import Slider, TextInput
import colorsys
import yaml
from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, Slider
from bokeh.plotting import figure, output_notebook, show, curdoc
from bokeh.themes import Theme
from graphSlits import graphSlits




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
slitData = np.linspace(-.00005, .00005, 10000 )



#other plot

#----------------------------------------------------------------------------------
		






#----------------------------------------------------------------------------------
		

slitBright = np.ones(10000)
slcolor, slRGBs = generate_color_range(1000,slitBright, 1)	
slsource = ColumnDataSource(data=dict(x=np.zeros(10000), y=slitData, slcolor=slcolor, RGBs=slRGBs))



p3 = figure( x_range=(-.0005, .0005), 
            y_range=(slitData[0],slitData[-1]),
            plot_width=100, plot_height=400,  tools="reset,save")

colorSlits = p3.rect(x='x' , y='y', width=.002, height=slitData[1] - slitData[0],
                       color='slcolor', source=slsource)
                       
                       
brightness = y # change to have brighter/darker colors
crcolor, crRGBs = generate_color_range(1000,brightness, 1)
cry = [ 5 for i in range(len(x)) ]
crsource = ColumnDataSource(data=dict(x=x, y=cry, crcolor=crcolor, RGBs=crRGBs))

p2 = figure( x_range=(x[0],x[-1]), 
            y_range=(0,10),
            plot_width=400, plot_height=150,
            title='Intensity Distribution', tools="reset,save")

color_range1 = p2.rect(x='x' , y='y', width=x[1] - x[0], height=10,
                       color='crcolor', source=crsource)
p2.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p2.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
p2.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels

p2.xaxis.axis_label = "Distance (m)"
# Set up plot
plot = figure(x_range=(x[0],x[-1]), plot_height=200, plot_width=400, title="Intensity Distribution",
              tools="crosshair,reset,save",
               y_range=[-0.5, 7.0])
plot.xaxis.axis_label = "Distance (m)"
plot.yaxis.axis_label = "Intensity (V^2/m^2)"
p2.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks


plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


#set up last plot

p = figure(plot_width=400, plot_height=400)

p.line(x=slitData, y=slitBright,line_width=2, line_alpha=0.6)

p3.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
p3.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
p3.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
p3.ygrid.visible = False
p3.yaxis.visible = False

p3.xaxis.major_tick_line_color = None  # turn off y-axis major ticks
p3.xaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
p3.xaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
p3.xgrid.visible = False
p3.xaxis.visible = False


plot.background_fill_color = '#2F2F2F'
plot.border_fill_color = '#2F2F2F'

# Set up widgets
electricfield = Slider(title="Initial electric field", value=1.0, start=0.0, end=5.0, step=0.1)
wavelength = Slider(title="Wavelength (nm)", value=400, start=400, end=700, step=5.0)
distance = Slider(title="Distance Between Slits (nm)", value=500, start=500, end=5000, step=50)
length = Slider(title="Distance between slits and screen", value=1.0, start=0.0, end=5.0, step=0.1)
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
    slitData = np.linspace(-.00005, .00005, 10000 )
    
  
 
    num = (s - 1)*d
    startingPoint = -1 * (num/2)
    slitArray = np.arange(s)
    sA = slitArray * d + startingPoint
    
    
    slitBright[:] = 0
    

    for j in np.arange(len(sA)):
        i1 = int((sA[j]- a/2 - startingPoint) *1e8)
        i2 = int((sA[j] + a/2 - startingPoint) *1e8)
        slitBright[i1:i2] = 1


   	         
            
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
    
    slcolor, slRGBs = generate_color_range(1000,slitBright, 1)	
    crsource.data = dict(x=crx, y=cry, crcolor=crcolor, RGBs=crRGBs)
    slsource.data = dict(x=np.zeros(10000), y=slitData, slcolor=slcolor, RGBs=slRGBs)
    
    


for i in [electricfield, wavelength, distance, length, slits, width]:
    i.on_change('value', update_data)

    

inputs = widgetbox( electricfield, wavelength, distance, length, slits, width)

curdoc().add_root(row(inputs,p3, column(plot, p2), width=800))
curdoc().title = "Intensity Distribution"
