# Pygame UI Designer

Pygame UI Designer (pgUId) is a free library for the development of user interfaces in [Pygame](https://pypi.org/project/Pygame/). Creating UI in Pygame can be time-consuming and difficult, so with this library, you will be able to create a UI in under a minute, with little to no difficulty.

### Installation

Before installing, make sure that you have [Python](https://www.python.org/downloads/) installed on your computer. To check, run this command in a terminal:
```
python --version
```
After you have verified that Python is installed, you need to ensure that pip is installed. You can check that by running the following command:
```
pip --version
```
After you have verified that you have Python and pip installed, check if you have the [Pygame](https://pypi.org/project/Pygame/) and [Requests](https://pypi.org/project/requests/) libraries installed by running these commands:
```
python -m pygame
python -m requests
```
Now that you have every dependency installed, you can install Pygame UI Designer by running this command:
```
pip install pguid
```

### Dependencies

Currently, there are only two dependencies for pgUId, one being Pygame (obviously), and the other being requests (for copying the docs). I don't plan on needing any other libraries, but that is not a promise.

| Name   | Version   |
| ------ | --------- |
| pygame | >=1.9.1  |
| requests | >=2.0.0 |