# berryimu

This is a Python package with bindings for interacting with the BerryIMU.

## Wiring

The BerryIMU is a 9-axis motion tracking device that can be connected to a Raspberry Pi via I2C. The following wiring is required:

- BerryIMU VCC to 3.3V
- BerryIMU GND to GND
- BerryIMU SCL to SCL
- BerryIMU SDA to SDA

See the example wiring diagrams [here](https://ozzmaker.com/product/berryimu-accelerometer-gyroscope-magnetometer-barometricaltitude-sensor/).

## Installation

Install the package from PyPI:

```bash
pip install berryimu
```

To verify the installation, run:

```bash
berryimu
```

You should see the BerryIMU data printed to the console.
