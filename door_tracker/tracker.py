import cv2
import sys
import time

PATH = r'..\closed_open_vid.mp4'

if __name__ == '__main__':

    tracker_type = 'KCF'
    tracker1, tracker2 = (cv2.TrackerKCF_create(), cv2.TrackerKCF_create())

    video = cv2.VideoCapture(PATH)  # 0 instead of PATH for CAM

    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    ok_frame, frame = video.read()
    if not ok_frame:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box (x, y, w, h)
    length = 90
    x = 619
    y = 236
    initial_bbox1 = (x + 430 - length, y - length//2, length, length)
    initial_bbox2 = (x - length//2, y - length//2, length, length)

    # Initialize tracker with first frame and bounding box
    tracker1.init(frame, initial_bbox1)
    tracker2.init(frame, initial_bbox2)

    while True:
        # Read a new frame
        ok_frame, frame = video.read()

        if not ok_frame:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok_tracker1, bbox1 = tracker1.update(frame)
        ok_tracker2, bbox2 = tracker2.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok_tracker1 or ok_tracker2:
            # Tracking success
            p1 = (int(bbox1[0]), int(bbox1[1]))
            p2 = (int(bbox1[0] + bbox1[2]), int(bbox1[1] + bbox1[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            # print((int(bbox1[0]), int(bbox1[1])), (int(bbox1[2]), int(bbox1[3])))
            p3 = (int(bbox2[0]), int(bbox2[1]))
            p4 = (int(bbox2[0] + bbox2[2]), int(bbox2[1] + bbox2[3]))
            cv2.rectangle(frame, p3, p4, (255, 0, 0), 2, 1)
            # print((int(bbox2[0]), int(bbox2[1])), (int(bbox2[2]), int(bbox2[3])))

            if abs(initial_bbox1[0] - bbox1[0]) > 2 or abs(initial_bbox1[1] - bbox1[1]) > 2 \
                    or abs(initial_bbox2[0] - bbox2[0]) > 2 or abs(initial_bbox2[1] - bbox2[1]) > 2:
                cv2.putText(frame, "Door is open", (100, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 255), 2)
                print("changed")
            else:
                cv2.putText(frame, "Door is closed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 255), 2)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (50, 170, 50), 2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (50, 170, 50), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # if press SPACE bar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time.sleep(0.1)

    video.release()
    cv2.destroyAllWindows()
