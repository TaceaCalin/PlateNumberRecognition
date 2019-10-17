import cv2
import numpy as np
import PlateNumberNeuralNetwork as NN
import math
import keyboard
import time
import scipy.io as sio
from pyzbar.pyzbar import decode
import mysql.connector

config = {
  'host': 'localhost',
  'user': 'CalinTacea',
  'password': 'babolat',
  'database': 'intelligentparking',
}


def ConnectToDataBase():
    mydb = mysql.connector.connect(**config)
    return mydb


def ValidatePlateNumber(platenumber):
    print(platenumber)
    mydb = ConnectToDataBase()
    mycursor = mydb.cursor()
    try:
        mycursor.execute("SELECT * FROM Parking WHERE PlateNumber = '%s'" % platenumber)
        results = mycursor.fetchall()
        if not results:
            print("Nu se afla in baza de date")
        else:
            print(results)
    except:
        print("Error: unable to fecth data")
    mydb.close()


def barcodeReader(image, bgr):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)

    for decodedObject in barcodes:
        points = decodedObject.polygon

        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

    for bc in barcodes:
        cv2.putText(frame, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    bgr, 2)

        return bc.data.decode("utf-8")

def __draw_label(im, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.2
    color = (0, 255, 0)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(im, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(im, text, pos, font_face, scale, color, 1, cv2.LINE_AA)


net = NN.NeuralNetwork()
tf_number = net.importONNXModel(r"C:\Users\calin.tacea\Documents\MATLAB\WorkDigitsPlease")
tf_letter = net.importONNXModel(r"C:\Users\calin.tacea\Documents\MATLAB\LetterNeuralNetwork")
cap = cv2.VideoCapture(0)
bgr = bgr = (8, 70, 208)
SCALAR_WHITE = (255.0, 255.0, 255.0)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
area_flag = 0
s = ''
numarator = 0
# ADAPTIVE_THRESH_WEIGHT = 9
# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    detection = 0
    ret, frame = cap.read()
    frame1 = np.asarray(frame, dtype=np.uint8)
    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,9)
    _, contours, hp = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    largest_rectangle = [0,0]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.025*cv2.arcLength(cnt, True), True)
        if len(approx)==4: #polygons with 4 points is what I need.
            area = cv2.contourArea(cnt)
            if 700 < area < 50000:
                start_time = time.time()
                #find the polygon which has the largest size.
                largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
                area_flag = 1
    if(area_flag == 1):
        x,y,w,h = cv2.boundingRect(largest_rectangle[1])
        if(w/h > 4 and w/h < 6):
            imgThreshCopy = cv2.rectangle(imgThresh, (x, y), (x + w, y + h), (255,255,0), 3)
            detection = 1
        if detection == 1 and keyboard.is_pressed('p'):
            numarator = 0
            s = ''
            neww = w
            newx = x
            newimage = imgThreshCopy[y-2:y + h + 2, newx - 2:newx + neww +2]
            sio.savemat('image2.mat', {'image2': newimage})
            newh = h
            _, parse, h = cv2.findContours(newimage, 1, 2)
            image_list = []
            # np.zeros(shape=(26, 26, 1, 60000))
            i = 0
            order = np.empty((1, 10000))
            for cnt in parse:
                x, y, w, h = cv2.boundingRect(cnt)
                if (35 * w > neww and w < neww / 3) and (1.7 * h > newh):
                    image = np.zeros([h, w])
                    image = newimage[y:y + h, x:x + w]
                    order[0, numarator] = x
                    image_list.append(image)
                    numarator = numarator + 1
            scaled_images = []
            if(len(image_list)==7):

                for aranjarej in range(0, len(image_list), 1):
                    for aranjare in range(0, len(image_list) - 1, 1):
                        if (order[0, aranjare] > order[0, aranjare + 1]):
                            aux = image_list[aranjare]
                            auxn = order[0,aranjare]
                            image_list[aranjare] = image_list[aranjare + 1]
                            order[0,aranjare] = order[0,aranjare+1]
                            image_list[aranjare + 1] = aux
                            order[0,aranjare + 1] =auxn
                for printeaza in range(7):
                    print(order[0, printeaza])
                for cnt in range(len(image_list)):
                    final_test_image = np.zeros([28, 28])
                    picture_rec = image_list[cnt]
                    line_diff = picture_rec.shape[0]
                    column_diff = picture_rec.shape[1]
                    if (line_diff >= column_diff):
                        ratio = line_diff / 20
                        col = math.floor(column_diff / ratio)
                        scaled_image = cv2.resize(picture_rec, (col, 20))
                        if (col % 2 == 0):
                            col = int(col / 2)
                            final_test_image[4:24, 14 - col:14 + col] = scaled_image
                        else:
                            col = int(col / 2)
                            final_test_image[4:24, 14 - col - 1:14 + col] = scaled_image

                    else:
                        ratio = column_diff / 20
                        line = math.floor(line_diff / ratio)
                        scaled_image = cv2.resize(picture_rec, (20, line))
                        if (line % 2 == 0):
                            line = int(line / 2)
                            final_test_image[14 - line:14 + line, 4:24] = scaled_image
                        else:
                            line = int(line / 2)
                            final_test_image[14 - line - 1:14 + line, 4:24] = scaled_image
                    for i in range(final_test_image.shape[0]):
                        for j in range(final_test_image.shape[1]):
                            if final_test_image[i, j] > 10:
                                final_test_image[i, j] = 255
                            else:
                                final_test_image[i, j] = 0
                    scaled_images.append(final_test_image)

                for i in range(2):
                    img = np.reshape(scaled_images[i], (1, 1, 28, 28))
                    prediction = tf_letter.run(img)
                    number = np.argmax(prediction)
                    if(np.max(prediction)> 0.5):
                        s += str(chr(65+number))
                    else:
                        s += "-"
                for i in range(2, 4):
                    img = np.reshape(scaled_images[i], (1, 1, 28, 28))
                    prediction = tf_number.run(img)
                    number = np.argmax(prediction)
                    if (np.max(prediction) > 0.5):
                        s += str(number)
                        print(prediction)
                    else:
                        s += "-"
                for i in range(4, 7):
                    img = np.reshape(scaled_images[i], (1, 1, 28, 28))
                    prediction = tf_letter.run(img)
                    number = np.argmax(prediction)
                    if (np.max(prediction) > 0.5):
                        s += str(chr(65 + number))
                    else:
                        s += "-"
                    end_time = time.time()
                    print(end_time - start_time)
                print(s)
                sio.savemat('test.mat', {'test': scaled_images[2]})
            else:
                print("not detecting the 7 chars")
        else:
            print("not found")
    if(keyboard.is_pressed('a')):
        f = open(r"C:\Users\calin.tacea\Desktop\PlateNumber.txt", "a+")
        f.write("\nPlate number that has been here today: "+s)
        f.close()
    if(keyboard.is_pressed('q')):
        s = barcodeReader(frame, bgr)
        if not isinstance(s, str):
            s = ""
        print(s)
    if(keyboard.is_pressed('v')):
        ValidatePlateNumber(s)
    __draw_label(imgThresh, 'Plate number: ' + s, (100, 100), (255, 0, 0))
    cv2.imshow('Input', imgThresh)
    area_flag = 0
    c = cv2.waitKey(1)
    if c == 27:
        del frame
        break

cap.release()
cv2.destroyAllWindows()