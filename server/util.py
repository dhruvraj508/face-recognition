import cv2
import json
import joblib
import base64
import numpy as np
from wavelet import transform_image

__class_name_to_number = {}
__class_number_to_name = {}
__model = None

def classify_image(image_base64_data, file_path=None):
    """Classifies the image and returns the class name.

    Args:
        image_base64_data (str): base64 encoded image data
        file_path (str, optional): path to the image. Defaults to None.

    Returns:
        str: class name
    """
    image_list = get_cropped_image_if_two_eyes(file_path, image_base64_data)
    result = []
    if len(image_list) == 0:
        return "No face detected"

    else:
        for image in image_list:
            # scalling the image into 32x32 before giving it to the model
            scalled_img = cv2.resize(image, (32, 32))
            # getting the transformed image from the function we wrote
            har_img = transform_image(image, 'db1', 5)
            # scalling the transformed image into 32x32
            scalled_har_img = cv2.resize(har_img, (32, 32))
            # now stacking on top using np.vstack
            combined_img = np.vstack((scalled_img.reshape(32*32*3,1), scalled_har_img.reshape(32*32,1)))
            len_img = 32*32*3 + 32*32
            # reshaping the combined image
            final_img = combined_img.reshape(1, len_img).astype(float)

            result.append({
            'class': class_number_to_name(__model.predict(final_img)[0]),
            'class_probability': np.around(__model.predict_proba(final_img)*100,2).tolist()[0],
            'class_dictionary': __class_name_to_number
            })
        return result    

# loading the model and the class dictionary
def load_artifacts():
    """
    Loads the model and the class dictionary from the artifacts folder.
    """
    global __class_name_to_number
    global __class_number_to_name
    global __model
    
    with open("./artifacts/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v:k for k,v in __class_name_to_number.items()}

    if __model is None:
        with open('./artifacts/saved_model.pkl', 'rb') as f:
            __model = joblib.load(f)

def class_number_to_name(class_num):
    """Converts the class number to the class name.

    Args:
        class_num (int): class number

    Returns:
        str: class name
    """
    return __class_number_to_name[class_num]


# Function to get the cropped image if there are two eyes
# Coppied from the model as used in jupyter notebook
def get_cropped_image_if_two_eyes(img_path, img_64_base_data):
    """Gets the cropped image if two eyes and face are detected in the image.

    Args:
        img_path (str): path to the image
        img_64_base_data (str): base64 encoded image data

    Returns:
        img_list (array): list of cropped images
    """
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

    if img_path != None:
        img = cv2.imread(img_path)
    else:
        img = get_cv2_image_from_base64_string(img_64_base_data)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    
    img_list = []

    for (x,y,w,h) in faces:
        roi_gray = gray_img[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            img_list.append(roi_color)
    
    return img_list


def get_cv2_image_from_base64_string(b64str):
    '''
    credit: https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    '''
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

if __name__ == "__main__":
    
    load_artifacts()
    print(classify_image(img1, None))