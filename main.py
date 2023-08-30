from typing import Union

from detector.detection_image import DoorDetector
from door_tracker.tracker import Tracker
from notification.notification import NotificationManager


def main():
    vid_path = input("Enter '0' to use the camera, or enter the video path otherwise: ")
    tel_num: str = input("Enter your phone number: ")
    mail_address: str = input("Enter your email address: ")
    service: str = input("[sms] or [email] or [all]: ")
    if vid_path == '0':
        vid_path = int(vid_path)

    if vid_path == '0':
        vid_path = int(vid_path)

    detector = DoorDetector(vid_path)
    tracker = Tracker()
    notify = NotificationManager(tel_num, mail_address, service)

    doors = detector.detect_all_doors()
    tracker.track_doors(doors[0], notify, vid_path)


if __name__ == "__main__":
    main()
