import time
from typing import List, Final
import cv2
import sys
from notification.notification import NotificationManager
import threading

SQUARE_LENGTH: Final[int] = 90


class Tracker:
    tracker_type: str
    tracker: cv2.TrackerMIL
    status: str

    def track_doors(self, doors: List[int], notify: NotificationManager, vid_source=0) -> None:
        self.tracker_type = 'MIL'
        self.tracker = cv2.TrackerMIL_create()
        self.status = 'closed'

        video = cv2.VideoCapture(vid_source)  # 0 instead of PATH for CAM

        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        ok_frame, frame = video.read()
        if not ok_frame:
            print('Cannot read video file')
            sys.exit()

        initial_bbox = (doors[0] - SQUARE_LENGTH//2, doors[1] - SQUARE_LENGTH//2, SQUARE_LENGTH, SQUARE_LENGTH)

        # Initialize tracker with first frame and bounding box
        self.tracker.init(frame, initial_bbox)

        while True:
            # Read a new frame
            ok_frame, frame = video.read()
            time.sleep(0.02)
            if not ok_frame:
                break

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok_tracker1, bbox = self.tracker.update(frame)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Draw bounding box
            if ok_tracker1:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

                if abs(initial_bbox[0] - bbox[0]) > 10 or abs(initial_bbox[1] - bbox[1]) > 10:
                    cv2.putText(frame, "Door is open", (100, 80), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 0, 255), 2)

                    if self.status == 'closed':
                        # Notify user asynchronously
                        notify_thread = threading.Thread(target=notify.notify_user,
                                                         args=("Door is open", frame))
                        notify_thread.start()

                        self.status = 'open'
                else:
                    cv2.putText(frame, "Door is closed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 0, 255), 2)

                    if self.status == 'open':
                        # Notify user asynchronously
                        notify_thread = threading.Thread(target=notify.notify_user,
                                                         args=("Door is closed", frame))
                        notify_thread.start()

                        self.status = 'closed'
            else:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 255), 2)

            # Display tracker type on frame
            cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (50, 170, 50), 2)

            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (50, 170, 50), 2)

            # Display result
            cv2.imshow("Tracking", frame)

            # if press SPACE bar
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

