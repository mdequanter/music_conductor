import torch
import cv2
import time
import argparse
import json
import math
import posenet
import pyautogui
import random


def Press(key):
    print (key)
    #pyautogui.press(key)


def on_publish(client,userdata,result):             #create function for callback
  print("data published \n")
  pass

nose = 0
leftEye=1
rightEye=2
leftEar=3
rightEar=4
leftShoulder=5
rightShoulder=6
leftElbow=7
rightElbow=8
leftWrist=9
rightWrist=10
leftHip=11
rightHip=12
leftKnee=13
rightKnee=14
leftAnkle=15
rightAnkle=16
neck=17


tempTime = time.time()


toProcess = [rightWrist,leftWrist,leftShoulder,rightShoulder]

keystroke = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']

Xlist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Ylist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
vMovement = ['S','S','S','S','S','S','S','S','S','S','S','S','S','S','S','S','S','S']  # S: Static,  U: UP, D: Down
hMovement = ['S','S','S','S','S','S','S','S','S','S','S','S','S','S','S','S','S','S']  # S: Static,  L: Left, R: Right


leftWristX = 0
leftElbowX = 0
leftShoulderX=0
leftWristY = 0
leftElbowY = 0
leftShoulderY=0
rightWristX = 0
rightElbowX = 0
rightShoulderX=0
rightWristY = 0
rightElbowY = 0
rightShoulderY=0

tempo = 0.01


frameCounter = 0

def distance(keypoint2, keypoint1):
    global Xlist, Ylist
    p = [Xlist[keypoint2], Ylist[keypoint2]]
    q = [Xlist[keypoint1], Ylist[keypoint1]]
    distance = 0
    if (Ylist[keypoint1] > 0 and Ylist[keypoint2] > 0 and Xlist[keypoint1] > 0 and Xlist[keypoint2] > 0):
        distance = math.sqrt((Ylist[keypoint2] - Ylist[keypoint1]) * (Ylist[keypoint2] - Ylist[keypoint1]) + (
                    Xlist[keypoint2] - Xlist[keypoint1]) * (Xlist[keypoint2] - Xlist[keypoint1]))
    return distance


def updown(keypoint2, keypoint1):
    global Ylist
    Y = Ylist[keypoint2] - Ylist[keypoint1]
    if (Y > 20):
        return ('H')
    elif (Y < -20):
        return ('L')
    else:
        return ('M')


def direction(keypoint2, keypoint1):
    global Xlist, Ylist
    X = Xlist[keypoint2] - Xlist[keypoint1]
    Y = Ylist[keypoint2] - Ylist[keypoint1]
    direction = math.atan2(X, Y)
    return math.degrees(direction)


def speed(keypoint, x, y):
    global Xlist, Ylist
    p = [Xlist[keypoint], Ylist[keypoint]]
    q = [x, y]
    distance = 0
    if (Ylist[keypoint] > 0 and Ylist[keypoint] > 0 and x > 0 and y > 0):
        distance = math.sqrt(
            (Ylist[keypoint] - y) * (Ylist[keypoint] - y) + (Xlist[keypoint] - x) * (Xlist[keypoint] - x))
    if (distance < 1):
        return ('L')
    elif (distance < 5):
        return ('M')
    elif (distance > 8):
        return ('H')




def processKeypoints(keypoints):
    global Xlist, Ylist, vMovement, hMovement, tempo, toProcess,tempTime,keystroke


    for data in keypoints:
        for item in toProcess :
            content = data[item]
            if (content[0] > 0 and  content[1] > 0):
                Xlist[item] = content[0]
                Ylist[item] = content[1]

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=1280)
parser.add_argument('--cam_height', type=int, default=720)
parser.add_argument('--scale_factor', type=float, default=0.7125)
args = parser.parse_args()


def main():
    global tempTime,leftWrist,leftShoulder,rightWrist,rightShoulder,Xlist,Ylist
    model = posenet.load_model(args.model)
    model = model.cuda()
    output_stride = model.output_stride

    cap = cv2.VideoCapture(args.cam_id)
    cap.set(3, args.cam_width)
    cap.set(4, args.cam_height)

    start = time.time()
    frame_count = 0
    while True:
        input_image, display_image, output_scale = posenet.read_cap(
            cap, scale_factor=args.scale_factor, output_stride=output_stride)

        with torch.no_grad():
            input_image = torch.Tensor(input_image).cuda()

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = model(input_image)

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
                heatmaps_result.squeeze(0),
                offsets_result.squeeze(0),
                displacement_fwd_result.squeeze(0),
                displacement_bwd_result.squeeze(0),
                output_stride=output_stride,
                max_pose_detections=18,
                min_pose_score=0.15)

        counter = 0

        processKeypoints(keypoint_coords)


        '''
        for pose in keypoint_coords :
            counter += 1
            if (counter == 1) :
                print (pose[9][0])
                
        '''
        timePassed = time.time() - tempTime
        if (timePassed > tempo):
            leftDirection = Xlist[leftShoulder] - Xlist[leftWrist]
            if (leftDirection >-300 and leftDirection < -250) :
                Press(keystroke[0])
            if (leftDirection >-250 and leftDirection < -200) :
                Press(keystroke[1])
            if (leftDirection >-200 and leftDirection < -150) :
                Press(keystroke[2])
            if (leftDirection >-100 and leftDirection < -50) :
                Press(keystroke[3])
            if (leftDirection > -50 and leftDirection < 0) :
                Press(keystroke[4])
            if (leftDirection >0 and leftDirection < 50) :
                Press(keystroke[5])
            if (leftDirection >50 and leftDirection < 100) :
                Press(keystroke[6])
            if (leftDirection >100 and leftDirection < 150) :
                Press(keystroke[7])
            rightDirection = Xlist[rightShoulder] - Xlist[rightWrist]
            if (rightDirection >-300 and rightDirection < -250) :
                Press(keystroke[0])
            if (rightDirection >-250 and rightDirection < -200) :
                Press(keystroke[1])
            if (rightDirection >-200 and rightDirection < -150) :
                Press(keystroke[2])
            if (rightDirection >-100 and rightDirection < -50) :
                Press(keystroke[3])
            if (rightDirection > -50 and rightDirection < 0) :
                Press(keystroke[4])
            if (rightDirection >0 and rightDirection < 50) :
                Press(keystroke[5])
            if (rightDirection >50 and rightDirection < 100) :
                Press(keystroke[6])
            if (rightDirection >100 and rightDirection < 150) :
                Press(keystroke[7])



            #print("play")
            #Press(keystroke[random.randint(0, 7)])
            tempTime = time.time()

            if (time.time()-start >= 1 ) :
                print('Average FPS: ', frame_count)
                start = time.time()
                frame_count = 0






        #print (distance (leftWrist,rightWrist))


        keypoint_coords *= output_scale

        # TODO this isn't particularly fast, use GL for drawing and display someday...

        overlay_image = posenet.draw_skel_and_kp(
            display_image, pose_scores, keypoint_scores, keypoint_coords,
            min_pose_score=0.15, min_part_score=0.1)

        cv2.imshow('posenet', overlay_image)
        frame_count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print('Average FPS: ', frame_count / (time.time() - start))


if __name__ == "__main__":
    main()