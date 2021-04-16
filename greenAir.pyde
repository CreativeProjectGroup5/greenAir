# SENSORS:

CO2_PIN = 0
DUST_PIN = 1
HUMIDITY_PIN = 2
TEMP_PIN = 3


# --------

# any element on the screen
class Field(object):
    
    def __init__(self, pin, x, y, d1, d2 = 0):
        
        self.pin = pin
        self.x, self.y, self.d1, self.d2 = pos(x, y, d1, d2)
        
        # if d2 is 0 the shape is circle and d1 is diameter, otherwise d1 = rectangle width, d2 = rectangle height
        # also collision detection adequate to the shape
        if d2:
            self.circ = False
            self.show = lambda: rect(self.x, self.y, self.d1, self.d2)
            self.collide = lambda x, y: x >= self.x - self.d1 and x <= self.x + self.d1 and y >= self.y - self.d2 and y <= self.y + self.d2
        else:            
            self.circ = True
            self.show = lambda: circle(self.x, self.y, self.d1)
            self.collide = lambda x, y : dist(self.x, self.y, x, y) <= self.d1/2
        
        
    # read the sensor data and calculate proper colour
    def read(self):
        
        self.data = read(self.pin)
        self.colour = colour(self.data)
    
    
    # display the element
    def display(self):
        
        fill(self.colour)
        self.show()
        fill(0)
        text(self.data, self.x, self.y)     
        
        
    # write info in the info section when clicked
    def click(self, mes1, mes2):
        
        if self.collide(mouseX, mouseY):
            displayInfo(self.colour, mes1 + str(self.data) + mes2)
        
                
# --------

def read(pin):
    
    # this should be replaced with actual reading of the pin state
    return int(random(4))


def colour(reading):
    
    # this should be replaced with calculating displayed colour based on a sensor reading
    colours = [color(100, 150, 250), color(150, 200, 50), color(250, 200, 50), color(200, 50, 50)]
    return colours[reading]


# --------

# get actual position from screen proportions
def pos(x, y, w, h):
    
    return width * x, height * y, width * w, height * h
    
    
# display info in the info section
def displayInfo(colour, message):
    
    x, y, w, h = pos(.5, .7, .8, .45)
    fill(colour)
    rect(x, y, w, h)
    fill(0)
    text(message, x, y, w, h)


# update sensor data
def update():
    co2.read()
    dust.read()
    humidity.read()
    temp.read()


# check if any of below is clicked and display the information
def click():
    co2.click("Carbon dioxide: ", " %")
    dust.click("Pollen levels: ", " pm")
    humidity.click("Humidity: ", " %")
    temp.click("Temperature: ", " C")
    
    map_icon.click("", " display here")
    
    
# MAIN:

def setup():
    
    size(600, 700)
    
    rectMode(CENTER)
    textAlign(CENTER, CENTER)
    textSize(height/15)
    
    # create elements of the display
    global co2, dust, humidity, temp, map_icon
    
    co2 = Field(CO2_PIN, .2, .3, .25)
    dust = Field(DUST_PIN, .5, .3, .25)
    humidity = Field(HUMIDITY_PIN, .8, .3, .25)
    temp = Field(TEMP_PIN, .2, .1, .2, .1)
    
    # create map icon and assign it proper text and colour
    map_icon = Field(None, 0.8, 0.1, 0.2, 0.1)
    map_icon.data = "Map"
    map_icon.colour = color(150, 150, 150)
    
    update()
    
    
def draw():
    
    # display the data
    co2.display()
    dust.display()
    humidity.display()
    temp.display()
    
    map_icon.display()
    
    
def mouseClicked():
    update()
    click()
