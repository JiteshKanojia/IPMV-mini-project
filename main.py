

# Author :		[Jitesh Kanojia]
# Filename:			main.py
# Functions:		process_video
#  Global variables:	frame_details


####################### IMPORT MODULES #######################
##############################################################
import cv2
import numpy as np
import os
##############################################################

# Global variable for details of frames seleced in the video will be put in this dictionary, returned from process_video function
frame_details = {}

##############################################################


def process_video(vid_file_path, frame_list):
    """
    Purpose:
    ---
    this function takes file path of a video and list of frame numbers ase argumnts
    and returns dictionary containing details of red color circle co-ordinates in the frame

    Input Arguments:
    ---
    `vid_file_path` :		[ str ]
                    file path of video
    `frame_list` :			[ list ]
                    list of frame numbers

    Returns:
    ---
    `frame_details` :		[ dictionary ]
                    co-ordinate details of red colored circle present in selected frame(s) of video
                    { frame_number : [cX, cY] }

    Example call:
    ---
    frame_details = process_video(vid_file_path, frame_list)
    """

    global frame_details

    ##############	ADD YOUR CODE HERE	##############

    cap = cv2.VideoCapture(vid_file_path)

    for frameValue in frame_list:
        lower = np.array([200, 20, 9])
        upper = np.array([225, 45, 13])

        flagg = cap.set(cv2.CAP_PROP_POS_FRAMES, frameValue)
        _, frame = cap.read()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        filtered_img = cv2.medianBlur(rgb_frame, 3)

        mask = cv2.inRange(filtered_img, lower, upper)
        ret, thresh = cv2.threshold(mask, 127, 255, 1)
        contours, hierachy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            M = cv2.moments(contour)
            if(M['m00'] == 0):
                continue

            else:
                cx = int(M['m10']/M['m00'])

                cy = int(M['m01']/M['m00'])
                # print(cx)
                # print(cy)
                frame_details[frameValue] = [cx, cy]
    # print(M)

    ##################################################

    return frame_details


# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes input for selecting one of two videos available in Videos folder
#                   and a input list of frame numbers for which the details are to be calculated. It runs process_video
#                   function on these two inputs as argument.
if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in ' + curr_dir_path)

    # path directory of videos in 'Videos' folder
    vid_dir_path = curr_dir_path + '/Videos/'

    try:
        file_count = len(os.listdir(vid_dir_path))

    except Exception:
        print('\n[ERROR] "Videos" folder is not found in current directory.')
        exit()

    print('\n============================================')
    print('\nSelect the video to process from the options given below:')
    print('\nFor processing ballmotion.m4v from Videos folder, enter \t=> 1')
    print('\nFor processing ballmotionwhite.m4v from Videos folder, enter \t=> 2')

    choice = input('\n==> "1" or "2": ')

    if choice == '1':
        vid_name = 'ballmotion.m4v'
        vid_file_path = vid_dir_path + vid_name
        print('\n\tSelected video is: ballmotion.m4v')

    elif choice == '2':
        vid_name = 'ballmotionwhite.m4v'
        vid_file_path = vid_dir_path + vid_name
        print('\n\tSelected video is: ballmotionwhite.m4v')

    else:
        print('\n[ERROR] You did not select from available options!')
        exit()

    print('\n============================================')

    if os.path.exists(vid_file_path):
        print('\nFound ' + vid_name)

    else:
        print('\n[ERROR] ' + vid_name +
              ' file is not found. Make sure "Videos" folders has the selected file.')
        exit()

    print('\n============================================')

    print('\nEnter list of frame(s) you want to process, (between 1 and 404) (without space & separated by comma) (for example: 33,44,95)')

    frame_list = input('\nEnter list ==> ')
    frame_list = list(frame_list.split(','))

    try:
        for i in range(len(frame_list)):
            frame_list[i] = int(frame_list[i])
        print('\n\tSelected frame(s) is/are: ', frame_list)

    except Exception:
        print('\n[ERROR] Enter list of frame(s) correctly')
        exit()

    print('\n============================================')

    try:
        print('\nRunning process_video function on', vid_name,
              'for frame following frame(s):', frame_list)
        frame_details = process_video(vid_file_path, frame_list)

        if type(frame_details) is dict:
            print(frame_details)
            print('\nOutput generated. Please verify')

        else:
            print('\n[ERROR] process_video function returned a ' +
                  str(type(frame_details)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print(
            '\n[ERROR] process_video function is throwing an error. Please debug process_video function')
        exit()

    print('\n============================================')
