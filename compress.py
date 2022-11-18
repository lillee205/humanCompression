from PIL import Image
import os 
import shutil

def colorQuantizeImg(img, numColors):
    """ input: img is a string representing a filename to a portrait
               numColors is an int saying how many colors we want
        output: PIL img of newly color quantized portrait
    """
    pilImg = Image.quantize(colors=numColors, method = None, kmeans = 0,
    palette = None)
    return pilImg

def sampleImg(img):
    pass

def isHuman(img):
    pass 

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
                    newImg.save(portrait)
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
