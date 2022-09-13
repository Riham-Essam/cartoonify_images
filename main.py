import cv2  # for image processing
import easygui  # to open the fileBox
import matplotlib.pyplot as plt
import os
from tkinter import *
import tkinter as tk
import sys

#HINT: Uncomment these importing libraries then Uncomment the used command below
#import numpy as np  # to store image
#import imageio  # to read image stored at particular path
#from tkinter import filedialog
#from PIL import ImageTk, Image


#For creating the fileBox
frame = Tk()
frame.geometry('400x300')
frame.title('Cartoonify the image')
frame.configure(background='white')

#8D918D is Gunmetal gray color
label = Label(frame, background='#8D918D', font=('Arial', 20, 'bold'))

#Get Img
def uploadImg():
    #To choose the img from the device and stores the path as a string
    imgPath = easygui.fileopenbox()
    cartoonify(imgPath)

def cartoonify(imgPath):
    # read the image
    chosenImg = cv2.imread(imgPath)  # imread is used to store img as numbers
    # HINT: we can also use numpy to convert img to numpy array

    chosenImg = cv2.cvtColor(chosenImg, cv2.COLOR_BGR2RGB)
    #print(chosenImg)  # image is stored in form of numbers

    # To confirm that the image is chosen
    if chosenImg is None:
        print("Can't find any image, please try again")
        sys.exit()

    # Width = 960 , Height = 540
    ReSized1 = cv2.resize(chosenImg, (960, 540))
    # plt.imshow(ReSized1, cmap='gray')

    # converting an image to grayscale(used in flag parameter)
    grayScaleImage = cv2.cvtColor(chosenImg, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')

    # applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    # plt.imshow(ReSized3, cmap='gray')

    # retrieving the edges for cartoon effect
    # by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    # plt.imshow(ReSized4, cmap='gray')

    # We use bilateralFilter which removes the noise
    # and keep edge sharp as required
    colorImage = cv2.bilateralFilter(chosenImg, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    # plt.imshow(ReSized5, cmap='gray')

    # masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    # plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    figNames = ['Original photo','GrayScaled Photo','Blurred Photo','Cartoon Photo','BilateralFiltered Photo','Beautified Photo']

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.3, wspace=0.1))   #rows = 3 , cols = 2

    for itr, img in enumerate(axes.flat):
        img.set_title(figNames[itr])
        img.imshow(images[itr], cmap='gray')

    save1 = Button(frame, text="Save cartoon image", command=lambda: save(ReSized6, imgPath), padx=30, pady=5)
    # E2DFD2 is pearl color & 34282C is charcoal color
    save1.configure(background='#34282C', foreground='#E2DFD2', font=('Arial', 10, 'bold'))
    save1.pack(side=TOP, pady=50)

    plt.show()


def save(ReSized6, imagePath):
    # saving an image using imwrite()
    cartoonifiedImage = "cartoonified_image"
    oldPath = os.path.dirname(imagePath)
    extension = os.path.splitext(imagePath)[1]   # To extract the extension of the file from the path
    newPath = os.path.join(oldPath, cartoonifiedImage + extension)
    cv2.imwrite(newPath, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    msg = "Image is saved by name " + cartoonifiedImage + " at " + newPath
    tk.messagebox.showinfo(title=None, message=msg)

#Upload Img
upload_img = Button(frame, text="Cartoonify An Image", command=uploadImg, padx=10, pady=5)
upload_img.configure(background='#34282C', foreground='#E2DFD2', font=('Arial', 10, 'bold'))
upload_img.pack(side=TOP, pady=50)

#Main
frame.mainloop()
