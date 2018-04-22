import random
from tkinter import *
from tkinter import ttk

from PIL import ImageFont, ImageDraw, Image

darkRed = (204,0,0)
red = (255,0,0)
pastelRed = (255,102,102)
darkOrange = (255,128,0)
orange = (255,153,51)
pastelOrange = (255,178,102)
darkYellow = (255,255,0)
yellow = (255,255,51)
pastelYellow = (255,255,152)
darkPink = (255,0,127)
darkBlue = (0,0,255)
lightBlue = (0,128,255)

fullColourList = [darkRed,red,pastelRed,darkOrange,orange,pastelOrange,darkYellow,yellow,pastelYellow,darkPink,darkBlue,lightBlue]
topTierColours = [red,darkOrange,darkYellow,yellow]
avantGardeColours = [red,orange,yellow,darkPink]
shittyColours = [darkBlue,darkPink,darkRed,pastelOrange]
pastelColours = [pastelRed,pastelOrange,pastelYellow]

class questionSun():
    #def __init__(self):

    def question(self):
        return("Please create your interpretation of Sol, our sun")

    def markeeAnswer(self):
        return([random.randint(0,10),random.randint(0,15)])
    #Shouldnt come up
    def answerMark(self,markeeAnswer):
        if self.answer == markeeAnswer:
            return(0)
        else:
            return(0)
    def display(self):
        questionWindow = Tk()
        w = Label(questionWindow,text=self.question()).pack()
        #questionWindow.mainloop()

    def createImage(self,artifact):

        complexity = artifact.answer[0]
        onTopic = artifact.answer[1]
        #print(artifact.answer)

        if onTopic > 10:
            backgroundColour = topTierColours[random.randint(0,len(topTierColours)-1)]
        elif onTopic == 10:
            backgroundColour = pastelColours[random.randint(0,len(pastelColours)-1)]
        elif onTopic == 9:
            backgroundColour = avantGardeColours[random.randint(0,len(avantGardeColours)-1)]
        elif onTopic > 5:
            backgroundColour = yellow
        else:
            backgroundColour = shittyColours[random.randint(0,len(shittyColours)-1)]

        image = Image.new("RGB", (512, 512), backgroundColour)

        x = (random.randint(0,10)/5)*complexity

        self.draw = ImageDraw.Draw(image)

        for i in range(int(x)):

            # On topic will have a maximum of 15
            # ,it shall determine how 'circular', the thigns are
            circleCords = [0,0,1,(random.randint(1,5)*onTopic/20)]

            enlargeFactor = random.randint(80,300)
            movementFactor = random.randint(0,600)

            self.draw.ellipse(((enlargeFactor*circleCords[0])+movementFactor,(enlargeFactor*circleCords[1])+movementFactor,(enlargeFactor*circleCords[2])+movementFactor,(enlargeFactor*circleCords[3])+movementFactor),fill=fullColourList[random.randint(0,len(fullColourList)-1)])

        image.save("./data/answers/"+str(artifact.answer)+".gif")

# Dan Gorringe January 2018
