import cv2
import mediapipe as mp
import pyautogui

cap =cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_width, screen_height = pyautogui.size()
index_y = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    faceOutput = face_mesh.process(rgb_frame)
    landmark_points = faceOutput.multi_face_landmarks
    # print(landmark_points)
    hands = output.multi_hand_landmarks
    if (hands and landmark_points) or hands:
        print("Hand")
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                   x = int(landmark.x*frame_width)
                   y = int(landmark.y*frame_height)
                   if id == 4:
                       cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                       index_x = screen_width/frame_width*x
                       index_y = screen_height/frame_height*y
                       pyautogui.moveTo(index_x, index_y)
                   if id == 8:
                       cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                       thumb_x = screen_width / frame_width * x
                       thumb_y = screen_height / frame_height * y
                       print('outside', abs(index_y - thumb_y))
                       if abs(index_y - thumb_y) < 20:
                           pyautogui.click()
                           pyautogui.sleep(1)
    elif landmark_points:
        print("Eye")
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_width / frame_width * x
                screen_y = screen_height / frame_height * y
                pyautogui.moveTo(screen_x,  screen_y)
                left = [landmarks[145], landmarks[158]]
                for landmark in left:
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
                if (left[0].y - left[1].y) < 0.004:
                    pyautogui.click()
                    pyautogui.sleep(0)


    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)