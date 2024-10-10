"""Example usage of the BerryIMU library."""

import argparse
import logging

from berryimu import IMU, KalmanFilter

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--bus", type=int, default=1)
    args = parser.parse_args()

    imu = IMU(args.bus)
    filter = KalmanFilter(imu)

    while True:
        angles = filter.step()
        logger.info("Angles: %s", angles)


if __name__ == "__main__":
    # python -m berryimu.cli
    main()
