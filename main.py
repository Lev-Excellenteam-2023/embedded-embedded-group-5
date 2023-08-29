from detector.detection_image import DoorDetector
from door_tracker.tracker import Tracker


def main():
    detector = DoorDetector()
    tracker = Tracker()
    doors = detector.detect_all_doors()
    tracker.track_doors(doors[0])


if __name__ == "__main__":
    main()
