import numpy as np

from bokeh.io import curdoc, show
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, output_notebook

# Set up data
x = np.linspace(-1, 1, 3000 )
y = np.cos(x)
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="Intensity Distribution",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[-1, 1], y_range=[-0.5, 7.0])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='Intensity Distribution')
electricfield = Slider(title="Initial electric field", value=1.0, start=0.0, end=5.0, step=0.1)
wavelength = Slider(title="Wavelength (nm)", value=100, start=100, end=1000, step=50)
distance = Slider(title="Distance Between Slits (nm)", value=500, start=500, end=5000, step=50)
length = Slider(title="Distance between slits and screen", value=1.0, start=0.0, end=5.0, step=0.1)
slits = Slider(title="Number of Slits", value=2.0, start=2.0, end=10, step=1.0)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    i = electricfield.value
    w = wavelength.value
    d = distance.value
    L = length.value
    s = slits.value
    
    w = w * (10**-9)
    d = d * (10**-9)
    x = np.linspace(-1, 1, 3000)
        
    num = (s - 1)*d
    startingPoint = -1 * (num/2)
    slitArray = np.arange(s)
    sA = slitArray * d - startingPoint
    
    

    rsquared = L**2 + ( x[:,None] - sA[None,:] )**2
    r = rsquared ** 0.5
    k = np.pi * 2 / w

        
    sinofkr = np.sin(k*r)
    sinfield = i * np.sum(sinofkr, axis = 1)

    
    cosofkr = np.cos(k*r)
    cosfield = i * np.sum(cosofkr, axis = 1)
    result = cosfield ** 2 + sinfield ** 2
        
    y = result / 2

    source.data = dict(x=x, y=y)

for w in [electricfield, wavelength, distance, length, slits]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, electricfield, wavelength, distance, length, slits)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"


