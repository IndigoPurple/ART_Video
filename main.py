import numpy as np
import cv2
import os


input_path = './video/'
video_num = 4
for i in range(1, video_num+1):
    # decompose videos into frames

    # Read the video from specified path
    cam = cv2.VideoCapture("%svideo%d.mp4"%(input_path,i))
    folder_name = './temp/img%d/'%i
    try:
        # creating a folder named data
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0

    while (True):

        # reading from frame
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = './%sframe' % folder_name + str(currentframe) + '.png'
            print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    ### compress video frames into measurements

    output_path = './video/meas%d.mp4' %i
    img_num = len(os.listdir(folder_name))
    cr = 8 # compression rate
    meas_num = img_num // cr
    img = cv2.imread('%sframe1.png' % folder_name)
    height, width, c = img.shape
    meas = np.zeros((height, width, 3, meas_num))
    mask = np.random.randint(2, size=(height, width, 3, cr))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # *'mp4v'
    video = cv2.VideoWriter(output_path, fourcc, 120, (width, height))

    # imgs = []
    print(meas_num)
    for i in range(meas_num):  # meas_num
        print(i)
        # meas = np.zeros((height,width,3,cr))
        meas_temp = np.zeros((height, width, 3))
        for k in range(cr):
            img = cv2.imread('%sframe%d.png' % (folder_name, i * cr + k))
            # imgs.append(img)
            for j in range(c):
                meas_temp[:, :, j] += np.multiply(mask[:, :, j, k], img[:, :, j])
        # meas[:, :, :,i] = meas_temp
        img = np.uint8(meas_temp / cr)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
        video.write(img)

    cv2.destroyAllWindows()
    video.release()
