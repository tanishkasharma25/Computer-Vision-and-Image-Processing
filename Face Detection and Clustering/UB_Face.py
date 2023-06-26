'''
Notes:
1. All of your implementation should be in this file. This is the ONLY .py file you need to edit & submit. 
2. Please Read the instructions and do not modify the input and output formats of function detect_faces() and cluster_faces().
3. If you want to show an image for debugging, please use show_image() function in helper.py.
4. Please do NOT save any intermediate files in your final submission.
'''


import cv2
import numpy as np
import os
import sys
import math

import face_recognition

from typing import Dict, List
from utils import show_image

'''
Please do NOT add any imports. The allowed libraries are already imported for you.
'''

def detect_faces(img: np.ndarray) -> List[List[float]]:
    """
    Args:
        img : input image is an np.ndarray represent an input image of shape H x W x 3.
            H is the height of the image, W is the width of the image. 3 is the [R, G, B] channel (NOT [B, G, R]!).

    Returns:
        detection_results: a python nested list. 
            Each element is the detected bounding boxes of the faces (may be more than one faces in one image).
            The format of detected bounding boxes a python list of float with length of 4. It should be formed as 
            [topleft-x, topleft-y, box-width, box-height] in pixels.
    """
    detection_results: List[List[float]] = [] # Please make sure your output follows this data format.

    # Add your code here. Do not modify the return and input arguments.

    coordinates = face_recognition.face_locations(img)
    final_list = []
    for pixels in coordinates:
        detection_results = []
        detection_results.append(float(pixels[3]))
        detection_results.append(float(pixels[0]))
        detection_results.append(float(pixels[1]-pixels[3]))
        detection_results.append(float(pixels[2]-pixels[0]))
        final_list.append(detection_results)
    return final_list


def cluster_faces(imgs: Dict[str, np.ndarray], K: int) -> List[List[str]]:
    """
    Args:
        imgs : input images. It is a python dictionary
            The keys of the dictionary are image names (without path).
            Each value of the dictionary is an np.ndarray represent an input image of shape H x W x 3.
            H is the height of the image, W is the width of the image. 3 is the [R, G, B] channel (NOT [B, G, R]!).
        K: Number of clusters.
    Returns:
        cluster_results: a python list where each elemnts is a python list.
            Each element of the list a still a python list that represents a cluster.
            The elements of cluster list are python strings, which are image filenames (without path).
            Note that, the final filename should be from the input "imgs". Please do not change the filenames.
    """
    cluster_results: List[List[str]] = [[]] * K # Please make sure your output follows this data format.

    np.random.seed(20)

    codes =[]
    final_cluster =[]
    code_name_map ={}
    for k in imgs.keys():
        codes.append(face_recognition.face_encodings(imgs[k])[-1])
    
    rand_list = np.random.choice(range(len(codes)),size = K)
    cluster_centers = [codes[i] for i in rand_list]

    img_len = range(len(imgs.keys()))

    for i in range(999):
        group = []

        for  j in img_len:
            min_diff = 99999
            min_index = 0
            for k in range(K):
                current_diff = math.dist(cluster_centers[k],codes[j])
                if current_diff < min_diff:
                    min_diff = current_diff
                    min_index= k
            group.append(min_index)
    
        group_imgs =[[],[],[],[],[]]

        for l in range(len(codes)):
            c = group[l]
            group_imgs[c].append(codes[l])

        new_centers =[]
        for grp in group_imgs:
            new_centers.append(np.mean(np.asarray(grp), axis = 0))
        
        store = cluster_centers
        cluster_centers = new_centers
    
        if i !=0:
            if np.array_equal(np.array(store), np.array(cluster_centers)):
                final_cluster = group_imgs
                break
        i+=1

    return image_name_mapping(final_cluster,codes, imgs)
    


'''
If your implementation requires multiple functions. Please implement all the functions you design under here.
But remember the above 2 functions are the only functions that will be called by task1.py and task2.py.
'''

# Your functions. (if needed)

def image_name_mapping(final_cluster,codes, imgs):
    image_names = [i for i in imgs]

    name_result = [[],[],[],[],[]]
    for c in range(len(final_cluster)):
        for p in range(len(final_cluster[c])):
            arr = np.asarray(codes)

            for row, i in zip(arr, range(len(codes))):
                if np.array_equal(row, final_cluster[c][p]):

                    name_result[c].append(image_names[i])
    return name_result
