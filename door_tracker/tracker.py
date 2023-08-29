import cv2
import sys
import time

PATH = r'..\closed_open_vid.mp4'

if __name__ == '__main__':

    tracker_type = 'KCF'

    match tracker_type:
        case 'BOOSTING': tracker = cv2.TrackerBoosting_create()
        case 'MIL': tracker = cv2.TrackerMIL_create()
        case 'KCF': tracker = cv2.TrackerKCF_create()
        case 'TLD': tracker = cv2.TrackerTLD_create()
        case 'MEDIANFLOW': tracker = cv2.TrackerMedianFlow_create()
        case 'GOTURN': tracker = cv2.TrackerGOTURN_create()
        case 'MOSSE': tracker = cv2.TrackerMOSSE_create()
        case 'CSRT': tracker = cv2.TrackerCSRT_create()
        case _: sys.exit()

    video = cv2.VideoCapture(PATH)  # 0 instead of PATH for CAM

    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Define an initial bounding box (x, y, w, h)
    length = 90
    x = 619
    y = 236
    initial_bbox = (x + 430 - length, y - length//2, length, length)
    initial_bbox2 = (x - length//2, y - length//2, length, length)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, initial_bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()

        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            print((int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            if abs(initial_bbox[0] - bbox[0]) > 2 or abs(initial_bbox[1] - bbox[1]) > 2:
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

        # Exit if ESC pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):  # if press SPACE bar
            break

        # time.sleep(0.1)

    video.release()
    cv2.destroyAllWindows()
