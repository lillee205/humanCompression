from PIL import Image
import os 
import shutil
import cv2

def colorQuantizeImg(img, numColors):
    """ input: img is a string representing a filename to a portrait
               numColors is an int saying how many colors we want
        output: PIL img of newly color quantized portrait
    """
    pilImg = Image.open("./photos/" + img) 
    compImg = pilImg.quantize(colors=numColors, method = None, kmeans = 0,
    palette = None).convert('RGB')
    return compImg

def sampleImg(img):
    pass

def isHuman(img):
    pass 

def haar_cascade(img):
    ''' inputs:     img, the pathname of the img
        outputs:    a list containing the top-left and bottom-right coordinates of the face
    '''
    classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(img)
    faces = classifier.detectMultiScale(img) # result
    # to draw faces on image
    print(faces)
    if len(faces) > 0:
        result = faces[0]
        x, y, w, h = result
        x1, y1 = x + w, y + h
        # cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
        return [x, y, x1, y1] # top-left-x, top-left-y, bottom-right-x, bottom-right-y
    return [0, 0, 0, 0]

def main(portraits, option = "color_quantization"):
    # loop through each portrait
    for portrait in portraits:
        flag = False
        # make a copy of the file
        shutil.copyfile(portrait, "compressed_" + portrait)
        portrait = "compressed_" + portrait
        numColors = 255
        while flag and numColors > 25: 
            # check if portrait is identifiable as human
            if isHuman(portrait):
                if option == "color_quantization":
                    newImg = colorQuantizeImg(portrait, numColors - 25)
                    newImg.save("./photos/" + portrait)
                elif option == "sampling":
                    pass 
                else:
                    print("invalid option")
            else:
                print(f"not a human!!")
                break

if __name__ == "__main__":
    # get array of portrait file names 
    path = "./photos"
    portraits = os.listdir(path)
    print(portraits)
    main(portraits)
