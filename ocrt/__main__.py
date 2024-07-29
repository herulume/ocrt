import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
from collections.abc import Iterable   

def recursive_len(item):
    if isinstance(item, Iterable):
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1

def has_match(inp):
    return recursive_len(inp) > 0
        
def get_role(job:str):
    roles={
        'melee':['rpr','drg','vpr','nin','mnk'],
        'caster':['blm','rdm','blu','pct','smn'],
        'tank':['drk','gnb','pld','war'],
        'healer':['ast','sch','sge','whm'],
        'ranged':['dnc','brd','mch']
    }
    for role in roles:
        if job in roles[role]:
            return role
    
def detect_job(opener:str) -> str:
    img = cv.imread(f'openers/{opener}', cv.IMREAD_GRAYSCALE)
    assert img is not None, "file could not be read, check with os.path.exists()"
    img2 = img.copy()

    for class_icon in os.listdir('classes'):
        template = cv.imread(f'classes/{os.fsdecode(class_icon)}', cv.IMREAD_GRAYSCALE)
        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]


        img = img2.copy()
        method = getattr(cv, 'TM_CCOEFF_NORMED')

        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)        
        #plt.imshow(img, cmap="gray")
        #plt.show()
        
        if has_match(loc):
            return os.fsdecode(class_icon).split(".")[0]

def detect_skills(opener:str,job:str,role:str):
    job_path=f"skills/{role}/{job}"
    opener = cv.imread(f'openers/{opener}', cv.IMREAD_GRAYSCALE)
    assert opener is not None, "file could not be read, check with os.path.exists()"
    op = opener.copy()
    skill_list=os.listdir(job_path)
    
    for skill in skill_list:
        template = cv.imread(f'{job_path}/{skill}', cv.IMREAD_GRAYSCALE)
        assert template is not None, "file could not be read, check with os.path.exists()"
        w, h = template.shape[::-1]
        img = op.copy()
        method = getattr(cv, 'TM_CCOEFF_NORMED')
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)

        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2) 
        plt.imshow(img, cmap="gray")
        plt.show()

        

if __name__ == "__main__":
    #print(detect_job("rpr"))
    #print(get_role('mnk'))
    opener= "sge_standard.png"
    job = detect_job(opener)

    detect_skills(opener,job,get_role(job))