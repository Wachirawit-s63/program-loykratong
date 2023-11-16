import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
from itertools import count

#Init app and setting
app = tk.Tk()
app.state('zoomed') #Maximize the screen
app.title("โปรแกรมลอยกระทง") 

#Create Width and Height of screen
screenWidth= app.winfo_screenwidth() 
screenHeight= app.winfo_screenheight()

#Import the Background image
currentDirectory = os.getcwd()
iconPath = os.path.join(currentDirectory, "images", "icon.ico") #Get the icon path
app.iconbitmap(iconPath)

images_list = []
gif_duration = 0
x = 0

def extract_image_from_gif(path):
    global gif_duration
    image = Image.open(path)
    for r in count(1):
        try:
            images_list.append(image.copy())
            image.seek(r)
        except Exception:
            break
    gif_duration = int(image.info['duration'])
    
def play_gif():
    global x, cur_img
    try:
        x += 1
        resize_img = images_list[x].resize(
                    (screenWidth, int(screenHeight*96 /100)),
                    Image.LANCZOS
                    )
        cur_img = ImageTk.PhotoImage(resize_img)      
        canvas.itemconfig(bgGif, image=cur_img) 
        app.after(gif_duration, play_gif)
    except Exception:
        x = 0
        app.after(gif_duration, play_gif)
    
gifImagepath = os.path.join(currentDirectory, "images", "gifbackground.gif")
extract_image_from_gif(gifImagepath)
play_gif()

#Create a canvas to display the background image
canvas = tk.Canvas(app, width=screenWidth, height=screenHeight)
canvas.pack()
bgGif = canvas.create_image(0, 0, image="", anchor=tk.NW)

def addLogo():
    #Get the logo image path
    logoPath = filedialog.askopenfilename(title="Select a logo image", filetypes=[("Image files", "*.jpg *.png *.jpeg")]) 
    if logoPath:
        logoImage = Image.open(logoPath)
        logoImage.thumbnail((int(0.24*screenWidth), int(0.21*screenHeight)))
        logoPhoto = ImageTk.PhotoImage(logoImage)
        #Display the logo image 
        canvas.create_image(
            int(0.5*screenWidth),
            int(0.4*screenHeight),
            image=logoPhoto,
            anchor=tk.CENTER,
        ) 
        addLogo.picturePhoto = logoPhoto

def importPicture():
    #Get the image path
    filePathTuple = filedialog.askopenfilenames(title="Select an image", filetypes=[("Image files", "*.jpg *.png *.jpeg")]) 
    xAxis = [0.0485, 0.145, 0.25, 0.37, 0.485, 0.533, 0.629, 0.77, 0.8, 0.915]  # ค่า x ตามลำดับของรูปภาพ
    yAxis = [0.625, 0.65, 0.63, 0.66, 0.635, 0.87, 0.654, 0.63, 0.85, 0.63]   # ค่า y ตามลำดับของรูปภาพ
    images = []
    if filePathTuple:
        filePathArray = np.asarray(filePathTuple) #Convert the tuple to array
        for i, file in enumerate(filePathArray):
            if i > 9:
                continue
            picture = Image.open(file)
            picture.thumbnail((int(0.1*screenWidth), int(0.09*screenHeight)))
            picturePhoto = ImageTk.PhotoImage(picture)
            images.append(picturePhoto)
            #Display the picture image
            canvas.create_image(
                int(xAxis[i]*screenWidth),
                int(yAxis[i]*screenHeight),
                image=images[-1],
                anchor=tk.CENTER,
            )
        importPicture.picturePhoto = images

changeLogoButton = tk.Button(app, text="เพิ่ม/เปลี่ยน logo", command=addLogo,
                            fg="white", bg="#4B109E", 
                            width=int(0.01*screenWidth), height=int(0.002*screenHeight))
changeImageButton = tk.Button(app, text="เพิ่มภาพกระทง", command=importPicture,
                            fg="white", bg="#4B109E", 
                            width=int(0.01*screenWidth), height=int(0.002*screenHeight))

changeLogoButton.place(relx = 0.924, rely = 0.96, anchor = 'ne')
changeImageButton.place(relx = 0.999, rely = 0.96, anchor = 'ne')

# Run the application
app.mainloop()