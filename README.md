# MS Clippy

MS Clippy is an OBS Studio script that records a timestamp to a file when a designated hotkey is pressed and saves a clip with the replay buffer. This is useful for keeping track of important moments during a live stream or recording session.

## Setup

1. Download the `MS_Clippy.py` file from the repository.
2. In OBS Studio, go to "Tools" -> "Scripts" -> "Python Scripts" and click the "+" button.
3. Select the `MS_Clippy.py` file and click "Open".
4. In the "Scripts" window, click the "MS Clippy" script to open the settings.
5. Choose a file for the timestamp log file. This is where the script will save the timestamps and clip names.
6. Choose a .wav file for feedback sounds. This will tell you that the clip was taken.
7. Assign a hotkey for the "MS Clippy" action. This will trigger the timestamp recording and clip saving.

## Usage

1. Start streaming or recording in OBS Studio.
2. Press the hotkey assigned to the "MS Clippy" action to record a timestamp and save a clip to the replay buffer.
3. The elapsed time since the start of the stream/recording session and the clip name (if replay is enabled) will be logged to the timestamp log file specified in the settings.

## Output
```
Recording started on 2023-03-02 at 23:32:48
 Time: 0:00:02 | Clip: Replay 2023-03-02 23-29-51.mkv
 Time: 0:00:37 | Clip: Replay 2023-03-02 23-32-58.mkv
 Time: 0:00:39 | Clip: Replay 2023-03-02 23-33-27.mkv

Recording started on 2023-03-02 at 23:33:30
 Time: 0:53:15
 ```

## Troubleshooting

- If the script is not working, make sure it is enabled in the "Scripts" window.
- If the script is enabled but still not working, try restarting OBS Studio.
- If the script is still not working, check the OBS Studio log for error messages.
- If you encounter any issues or have any suggestions for improvement, please create an issue on the GitHub repository.
