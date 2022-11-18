from PIL import Image
import os 

def colorQuantizeImg(img):
    pass 

def sampleImg(img):
    pass

def isHuman(img):
    pass 

def main(portraits, option = "color_quantization"):
    # loop through each portrait
    for portrait in portraits:
        flag = False
        while flag: 
            # check if portrait is identifiable as human
            if isHuman(portrait):
                if option == "color_quantization":
                    pass 
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
