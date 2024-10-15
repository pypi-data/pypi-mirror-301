# pyscreenrec

*pyscreenrec* is a small and cross-platform python library for recording screen.


[![Downloads](https://pepy.tech/badge/pyscreenrec)](https://pepy.tech/project/pyscreenrec)

<br>

## Installation
Install on Windows: 
`pip install pyscreenrec`

Install on Linux/macOS: 
`pip3 install pyscreenrec`

<br>

## Example usage
``` python
>>> import pyscreenrec
>>> recorder = pyscreenrec.ScreenRecorder()

>>> # to start recording
>>> recorder.start_recording("recording.mp4", 10) 
>>> # 'recording.mp4' is the name of the output video file, may also contain full path like 'C:/Users/<user>/Videos/video.mp4'
>>> # the second parameter(10) is the FPS. You can specify the FPS for the screen recording using the second parameter.

>>> # to pause recording
>>> recorder.pause_recording()

>>> # to resume recording
>>> recorder.resume_recording()

>>> # to stop recording
>>> recorder.stop_recording()
```

Keep in mind that the `start_recording` method is non-blocking, it will start a thread in the background to capture the screenshots.

The `stop_recording` saves the video and deletes all screenshots used in the session. 
So calling the `stop_recording` method is necessary when `start_recording` is called.

If a screen recording session is already running, calling the `start_recording` and `resume_recording` methods raises a `ScreenRecodingInProgress` warning.

Similarly, if a screen recording session is not running, calling the `stop_recording` and `pause_recording` methods raises a `NoScreenRecodingInProgress` warning.

<br>

## Known limitations
*pyscreenrec* is not able to:
- capture the system sound during screen recording
- capture only a certain part of the screen

<br>

## Change Log
Changes made in the latest version (*v0.5*) are:
- Remove the `HighFPSWarning` and `InvalidFPS` exception classes.
- Raise frame count by almost 2 times.
- Calling start and resume recording methods on an already running recorder instance raises a warning instead of printing, and vice versa.
- Temporary screenshots are now stored in `~/.pyscreenrec_data` folder.
- Internal refactors.


View [CHANGELOG](https://github.com/shravanasati/pyscreenrec/blob/master/CHANGELOG) for more details.

<br>

## Contribution
Pull requests are welcome. If you want to make a major change, open an issue first to discuss about the change.

For further details, view [CONTRIBUTING.md](https://github.com/shravanasati/pyscreenrec/blob/master/CONTRIBUTING.md).