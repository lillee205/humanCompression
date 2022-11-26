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
    pilImg = Image.open(img)
    finalImg = pilImg.resize((width, height),Image.Resampling.LANCZOS)
    pilImg.close()
    return finalImg

def isHuman(img, orig_coords, scale = False):
    ''' inputs:     img, pathname of file
                    orig_coordinates, a 4-tuple of the top-left and bottom-right coords of the face
                    scale,  a bool indicating whether we are scaling the image (i.e., reducing the 
                            number of pixels in the image)
        outputs:    True, if the new coordinates are close to orig_coordinates
                    False otherwise
    '''
    new_coords = haar_cascade(img)
    width, height = abs(new_coords[2] - new_coords[0]), abs(new_coords[1] - new_coords[3])
    if not scale:
        return (orig_coords[0] - width*0.1 <= new_coords[0] <= orig_coords[0] + width*0.1) and (orig_coords[1] - height*0.1 <= new_coords[1] <= orig_coords[1] + height*0.1) and (orig_coords[2] - width*0.1 <= new_coords[2] <= orig_coords[2] + width*0.1) and (orig_coords[3] - height*0.1 <= new_coords[3] <= orig_coords[3] + height*0.1)
    else:
        old_width = abs(orig_coords[2] - orig_coords[0])
        scale_factor = width / old_width
        new_top_left_x = int(orig_coords[0]*scale_factor)
        new_top_left_y = int(orig_coords[1]*scale_factor)
        new_bot_right_x = int((orig_coords[0]*scale_factor) + width)
        new_bot_right_y = int((orig_coords[1]*scale_factor) + height)
        return (new_top_left_x - width*0.1 <= new_coords[0] <= new_top_left_x + width*0.1) and (new_top_left_y - height*0.1 <= new_coords[1] <= new_top_left_y + height*0.1) and (new_bot_right_x - width*0.1 <= new_coords[2] <= new_bot_right_x + width*0.1) and (new_bot_right_y - height*0.1 <= new_coords[3] <- new_bot_right_y + height*0.1)

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
    flag = False
    if option == "sampling":
        flag = True
    # loop through each portrait
    for portrait in portraits:
        print(f"Currently testing {portrait}")
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
            
            if isHuman(portrait, orig_coordinates, scale = flag):
                if option == "color_quantization":
                    if numColors > 25:
                        break
                    numColors -= 25
                    newImg = colorQuantizeImg(portrait, numColors)
                    newImg.save(portrait)
                elif option == "sampling":
                    newHeight = int(height * percent)
                    newWidth = int(width * percent)
                    if percent <= 0 or newHeight <= 0 or newWidth <= 0:
                        break
                    newImg = sampleImg(portrait, newWidth, newHeight)
                    newImg.save(portrait)
                    percent -= 0.1
                else:
                    print("Please pick either color_quantization or sampling.")
                    
            else:
                if option == "color_quantization":
                    print(f"Color Quantization: Stopped being human at {numColors}")
                elif option == "sampling":   
                    print(f"Sampling: Stopped being human at {percent*100}% reduction.")
                break
            print()

if __name__ == "__main__":
    # get array of portrait file names 
    path = "./photos/"
    portraits = os.listdir(path)
    print(portraits)
    main(portraits, "sampling")
