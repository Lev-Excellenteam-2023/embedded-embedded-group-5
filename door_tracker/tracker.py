from typing import List, Final
import cv2
import sys

PATH: Final[str] = r'..\closed_open_vid.mp4'
SQUARE_LENGTH: Final[int] = 90


class Tracker:
    tracker_type: str
    tracker1: cv2.TrackerMIL

    def track_doors(self, doors: List[int], vid_source=0) -> None:
        self.tracker_type = 'MIL'
        self.tracker1 = cv2.TrackerMIL_create()

        video = cv2.VideoCapture(vid_source)  # 0 instead of PATH for CAM

        if not video.isOpened():
            print("Could not open video")
            sys.exit()

        ok_frame, frame = video.read()
        if not ok_frame:
            print('Cannot read video file')
            sys.exit()

        initial_bbox1 = (doors[0] - SQUARE_LENGTH//2, doors[1] - SQUARE_LENGTH//2, SQUARE_LENGTH, SQUARE_LENGTH)
        initial_bbox2 = (doors[0] - SQUARE_LENGTH//2 + doors[2], doors[1] - SQUARE_LENGTH//2,
                         SQUARE_LENGTH, SQUARE_LENGTH)

        # Initialize tracker with first frame and bounding box
        self.tracker1.init(frame, initial_bbox1)

        while True:
            # Read a new frame
            ok_frame, frame = video.read()

            if not ok_frame:
                break

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok_tracker1, bbox1 = self.tracker1.update(frame)

            bboxes = [bbox1]

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Draw bounding box
            if ok_tracker1:
                # Tracking success
                for bbox in bboxes:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                    # print((int(bbox1[0]), int(bbox1[1])), (int(bbox1[2]), int(bbox1[3])))

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


def main():
    my_tracker = Tracker()
    my_tracker.track_doors([619, 236, 391])


if __name__ == '__main__':
    main()
