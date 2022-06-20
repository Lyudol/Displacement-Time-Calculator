from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
import math

g = 9.81
rampLength = 1
rampAngle = 22.33
onTop = False

def constantUpdate(gEntry, rlengthEntry, rangleEntry, info, infoLabel):
    global g
    global rampLength
    global rampAngle
    global onTop

    try:
        if float(gEntry.get()) <= 0:
            infoLabel.config(text="g can only be positive")
        elif float(rlengthEntry.get()) <= 0:
            infoLabel.config(text="Ramp length can only be positive")
        elif float(rangleEntry.get()) < 0:
            infoLabel.config(text="Ramp angle must be at least 0")
        else:
            g = float(gEntry.get())
            rampLength = float(rlengthEntry.get())
            rampAngle = float(rangleEntry.get())
            info.destroy()
            onTop =False 
    except ValueError:
        if gEntry.get() == "" or rlengthEntry.get() == "" or rangleEntry.get() == "":
            infoLabel.config(text="Please fill in all fields")
        else:
            errorLabel.config(text="Please only enter numbers")

def options():
    global onTop

    if not onTop:
        onTop = True

        def closing():
            global onTop
            onTop = False
            info.destroy()

        info = Tk()
        info.title("Options")
        info.geometry("210x215")
        info.resizable(False, False)

        devLabel = Label(info, text="Developed by Alek Petseski").pack()
        version = Label(info, text="v1.0.0").pack()

        gLabel = Label(info, text=("Value of g (N/m\u00b2):"))
        gLabel.pack()
        gEntry = Entry(info, width=10, justify=CENTER)
        gEntry.insert(0, g)
        gEntry.pack()

        rlengthLabel = Label(info, text=("Ramp length (m):"))
        rlengthLabel.pack()
        rlengthEntry = Entry(info, width=10, justify=CENTER)
        rlengthEntry.insert(0, rampLength)
        rlengthEntry.pack()

        rangleLabel = Label(info, text=("Ramp angle (°):"))
        rangleLabel.pack()
        rangleEntry = Entry(info, width=10, justify=CENTER)
        rangleEntry.insert(0, rampAngle)
        rangleEntry.pack()

        infoLabel = Label(info, text="", fg="red")
        infoLabel.pack()

        enter = Button(info, text="Submit", command=lambda : constantUpdate(gEntry, rlengthEntry, rangleEntry, info, infoLabel))
        enter.pack(pady=5)

        info.protocol("WM_DELETE_WINDOW", closing)
        info.mainloop
    onTop = True

def getFunction():
    global canvas
    try:
        rampTime = float(rampTimeEntry.get())
        rampHeight = float(rampHeightEntry.get())
        decimalPlace = int(decimalPlaceEntry.get())

        errorLabel.config(text="")

        canvas.destroy()

        initVelocity = rampLength/rampTime

        initVelocityY = initVelocity * (math.sin(math.radians(rampAngle)))
        time = (math.sqrt((2*g*rampHeight)+initVelocityY**2)-initVelocityY)/(g)
        finalVelocityY = initVelocityY + g*time

        initVelocityX = math.sqrt(initVelocity**2 - initVelocityY**2)
        finalVelocity = math.sqrt(finalVelocityY**2 + initVelocityX**2)

        a = round((finalVelocity-initVelocity)/(2*time), decimalPlace)
        ay = round((finalVelocityY-initVelocityY)/(2*time), decimalPlace)

        fX = [a, "x**2", "+", round(initVelocity, decimalPlace), "x"]

        fig = plt.figure(facecolor="#f0f0f0")
        x = np.linspace(0,time,100)
        y1 = (fX[0]*x**2)+(fX[3]*x)
        y2 = ((2*fX[0]*x)+(fX[3]))
        y3 = (a*x**2)+(round(initVelocityY, decimalPlace)*x)
        ax1 = fig.add_subplot()
        ax1.set_ylabel("s (m)")
        ax1.set_xlabel("t (s)")
        plt.plot(x,y1, "r", label="s = f(t)")
        plt.plot(x,y2, "b", label="s = f'(t)")
        plt.plot(x, y2, "g")
        plt.title("Displacement/Time graph after ball leaves the ramp", fontsize=11)
        plt.legend()
        plt.grid()

        figCanvas = FigureCanvasTkAgg(fig, master=parent)
        figCanvas.draw()
        canvas = figCanvas.get_tk_widget()
        canvas.config(width=440, height=440)
        canvas.pack(pady=5)

        function = "f(t) = "+ str(a) +"t\u00b2+"+ str(round(initVelocity, decimalPlace)) +"t"
        derivative = "f'(t) = "+ str(2*a) +"t+"+ str(round(initVelocity, decimalPlace))

        functionLabel.config(text=function)
        derviativeLabel.config(text=derivative)

    except ValueError:
        if rampTimeEntry.get() == "" or rampHeightEntry.get() == "" or decimalPlaceEntry.get() == "":
            errorLabel.config(text="Please fill in all fields")
        else:
            errorLabel.config(text="Please only enter numbers")

parent = Tk()
parent.title("Theoretical Displacement/Time Calculator")
parent.geometry("480x755")
parent.resizable(False, False)

rampTimeLabel = Label(parent, text="Enter time taken for ball to travel across ramp (s):").pack(pady=5)
rampTimeEntry = Entry(parent, width=10, justify=CENTER)
rampTimeEntry.pack()
rampHeightLabel = Label(parent, text="Enter height of end of ramp off the ground (m):").pack()
rampHeightEntry = Entry(parent, width=10, justify=CENTER)
rampHeightEntry.pack()
decimalPlaceLabel = Label(parent, text="Enter decimal place:").pack()
decimalPlaceEntry = Entry(parent, width=10, justify=CENTER)
decimalPlaceEntry.pack()
errorLabel = Label(parent, fg="red")
errorLabel.pack()

submit = Button(parent, text="Submit", width=10, command=lambda : getFunction())
submit.pack()

advanced = Button(parent, text="Options", width=10, command=lambda : options())
advanced.pack()


functionLabel = Label(parent, text="f(t) =", font=("Arial, 18"))
functionLabel.pack(pady=5)
derviativeLabel = Label(parent, text="f'(t) =", font=("Arial", 18))
derviativeLabel.pack(pady=5)

canvas = Canvas(parent, width=440, height=440, bg="#f0f0f0")
rect = canvas.create_rectangle(2,2, 441, 441, outline='black')
canvas.pack(pady=5)

parent.mainloop()
