from PIL import Image
import os 
import shutil
import cv2
import csv

def colorQuantizeImg(img, numColors):
    """ input: img is a string representing a filename to a portrait
               numColors is an int saying how many colors we want
        output: PIL img of newly color quantized portrait
    """
    pilImg = Image.open(img) 
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
        if old_width == 0:
            print("not human orig")
            return
        scale_factor = width / old_width

        new_top_left_x = int(orig_coords[0]*scale_factor)
        new_top_left_y = int(orig_coords[1]*scale_factor)
        new_bot_right_x = int((orig_coords[0]*scale_factor) + width)
        new_bot_right_y = int((orig_coords[1]*scale_factor) + height)

        result = (new_top_left_x - width*0.1 <= new_coords[0] <= new_top_left_x + width*0.1) and (new_top_left_y - height*0.1 <= new_coords[1] <= new_top_left_y + height*0.1) and (new_bot_right_x - width*0.1 <= new_coords[2] <= new_bot_right_x + width*0.1) and (new_bot_right_y - height*0.1 <= new_coords[3] <= new_bot_right_y + height*0.1)

        return result

def haar_cascade(img):
    ''' inputs:     img, the pathname of the img
        outputs:    a 4-tuple containing the top-left and bottom-right coordinates of the face
    '''
    classifier = cv2.CascadeClassifier(cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml')

    img = cv2.imread(img)
    faces = classifier.detectMultiScale(img) # result

    # to draw faces on image
    if len(faces) > 0:
        result = faces[0]
        x, y, w, h = result
        x1, y1 = x + w, y + h

        # testing
        # cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
        # cv2.imshow('image', img)
  
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return (x, y, x1, y1) # top-left-x, top-left-y, bottom-right-x, bottom-right-y
    return (0, 0, 0, 0)

def main(portraits, option = "color_quantization"):
    
    # set up CSV for data collection
    header = ["filename"]
    
    if option == "color_quantization":
        header.append("at what # of colors is the human no longer recognizable?")
        
    elif option == "sampling":
        header.append("at what % compression is the human no longer recognizable?")
        
    data = []
    
    flag = False
    if option == "sampling":
        flag = True
    
    # loop through each portrait
    for portrait in portraits:
        data.append([portrait])
        print()
        print(f"Currently testing {portrait}")
        # run haar_cascade on orig file
        # make a copy of the file
        shutil.copyfile("./photos/" + portrait, "./compress_photos/" + portrait)
        portraitPil = Image.open("./photos/" + portrait)
        numColors = 255
        width, height = portraitPil.size
        percent = 1
        portraitPil.close()
        portrait = "./compress_photos/" + portrait

        orig_coordinates = haar_cascade(portrait)
        if orig_coordinates == (0,0,0,0):
            print("no human here")
            data[-1] = [portrait, "n.a"]
            continue
        while True: 
            # check if portrait is identifiable as human
            if isHuman(portrait, orig_coordinates, scale = flag):
                if option == "color_quantization":
                    if numColors <= 2:
                        break
                    if numColors >= 25:
                        numColors -= 15
                    else:
                        numColors -= 1
                    newImg = colorQuantizeImg(portrait, numColors)
                    newImg.save(portrait)
                    
                elif option == "sampling":
                    percent -= 0.1
                    newHeight = int(height * percent)
                    newWidth = int(width * percent)

                    if percent <= 0 or newHeight <= 0 or newWidth <= 0:
                        break
                    newImg = sampleImg(portrait, newWidth, newHeight)
                    newImg.save(portrait)
                    
                else:
                    print("Please pick either color_quantization or sampling.")
            else:
                if option == "color_quantization":
                    print(f"Color Quantization: Stopped being human at {numColors}")
                    data[-1]= [portrait, numColors]
                elif option == "sampling":   
                    print(f"Sampling: Stopped being human at {percent*100}% compression.")
                    data[-1] = [portrait, percent * 100]
                break
        
    with open(f'{option}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        
        # write the header
        writer.writerow(header)
            
        # write multiple rows
        writer.writerows(data)

if __name__ == "__main__":
    # get array of portrait file names 
    path = "./photos/"
    portraits = os.listdir(path)
    main(portraits, option="sampling")
