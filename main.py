from detector.detection_image import DoorDetector
from door_tracker.tracker import Tracker
from notification.notification import NotificationManager


def main():
    vid_path: str = input("Enter the video path")
    tel_num: str = input("Enter your phone number")

    detector = DoorDetector(vid_path)
    tracker = Tracker()
    notify = NotificationManager(tel_num)

    doors = detector.detect_all_doors()
    tracker.track_doors(doors[0], notify, vid_path)


if __name__ == "__main__":
    main()
