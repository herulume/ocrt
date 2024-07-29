import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os


def detect_class(opener:str) -> str:
    img = cv.imread(f'openers/{opener}.png', cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img2 = img.copy()
         
    # All the 6 methods for comparison in a list
    methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR',
                  'TM_CCORR_NORMED', 'TM_SQDIFF', 'TM_SQDIFF_NORMED']
    
    for class_icon in os.listdir('classes'):
        print(os.fsdecode(class_icon))
        template = cv.imread(f'classes/{os.fsdecode(class_icon)}', cv.IMREAD_GRAYSCALE)
        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]


        # Storing the height and the width of the template image
        height_1, width_1 = img.shape
        height_2, width_2 = template.shape
        img = img2.copy()
        method = getattr(cv, 'TM_CCOEFF_NORMED')

        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)        
        plt.imshow(img, cmap="gray")
        plt.show()
        print(res)


    
if __name__ == "__main__":
    detect_class("rpr")