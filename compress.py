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
    pilImg.close()
    return compImg

def sampleImg(img, width, height):
    """ input: img is a string representing a filename to a portrait
               width, height are ints that represent new img size
        output: PIL img of newly sampled portrait
    """
    pilImg = Image.open("./photos/" + img)
    finalImg = piImg.resize((width, height),Image.ANTIALIAS)
    pilImg.close()
    return finalImg

def isHuman(img, orig_coords):
    ''' inputs:     img, pathname of file
                    orig_coordinates, a 4-tuple of the top-left and bottom-right coords of the face
        outputs:    True, if the new coordinates are close to orig_coordinates
                    False otherwise
    '''
    new_coords = haar_cascade(img)
    width, height = abs(new_coords[2] - new_coords[0]), abs(new_coords[1] - new_coords[3])
    return (orig_coords[0] - width*0.1 <= new_coords[0] <= orig_coords[0] + width*0.1) and (orig_coords[1] - height*0.1 <= new_coords[1] <= orig_coords[1] + height*0.1) and (orig_coords[2] - width*0.1 <= new_coords[2] <= orig_coords[2] + width*0.1) and (orig_coords[3] - height*0.1 <= new_coords[3] <= orig_coords[3] + height*0.1)

def haar_cascade(img):
    ''' inputs:     img, the pathname of the img
        outputs:    a 4-tuple containing the top-left and bottom-right coordinates of the face
    '''
    classifier = cv2.CascadeClassifier(cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml')

    img = cv2.imread(img)
    faces = classifier.detectMultiScale(img) # result
    # to draw faces on image
    print(faces)
    if len(faces) > 0:
        result = faces[0]
        x, y, w, h = result
        x1, y1 = x + w, y + h

        # testing
        # cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
        # cv2.imshow('image', img)
  
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
        return (x, y, x1, y1) # top-left-x, top-left-y, bottom-right-x, bottom-right-y
    return (0, 0, 0, 0)

def main(portraits, option = "color_quantization"):
    # loop through each portrait
    for portrait in portraits:        
        # run haar_cascade on orig file

        # make a copy of the file
        shutil.copyfile("./photos/" + portrait, "./compress_photos/" + portrait)
        numColors = 255
        portraitPil = Image.open("./photos/" + portrait)
        width, height = portraitPil.size
        percent = 1
        portraitPil.close()
        portrait = "./compress_photos/" + portrait

        orig_coordinates = haar_cascade(portrait)
        
        while True: 
            # check if portrait is identifiable as human

            if isHuman(portrait, orig_coordinates):
                print(portrait)
                if option == "color_quantization":
                    if numColors > 25:
                        break
                    numColors -= 25
                    newImg = colorQuantizeImg(portrait, numColors)
                    newImg.save("./compress_photos/" + portrait)
                elif option == "sampling":
                    if percent <= 0:
                        break
                    newImg = sampleImg(portrait, width * percent, height *
        percent)
                    newImg.save("./compress_photos/" + portrait)
                    percent -= 0.1
                else:
                    print("invalid option")
            else:
                print(f"not a human!!")
                break

if __name__ == "__main__":
    # get array of portrait file names 
    path = "./photos/"
    portraits = os.listdir(path)
    print(portraits)
    main(portraits)
