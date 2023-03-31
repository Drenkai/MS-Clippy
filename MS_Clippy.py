import obspython as obs  # Import the required OBS Python module
import datetime  # Import the datetime module to work with dates and times
import os  # Import the os module to work with files and directories
import winsound

def on_event(event):
    # If streaming or recording starts, reset the elapsed time to 0 and log the start time to a file
    if event in (obs.OBS_FRONTEND_EVENT_STREAMING_STARTED, obs.OBS_FRONTEND_EVENT_RECORDING_STARTED):
        update.current_time = 0
        now_str = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")  # Get the current time and format it as a string
        create_log_directory()
        with open(file_path, "a") as f:  # Open the log file for appending
            f.write(f"Recording started on {now_str}\n")  # Write the start time to the log file
    # Add a space when streaming or recording stops
    elif event in (obs.OBS_FRONTEND_EVENT_STREAMING_STOPPING, obs.OBS_FRONTEND_EVENT_RECORDING_STOPPING):
        create_log_directory()
        with open(file_path, "a") as f:  # Open the log file for appending
            f.write(f"\n")  # Add a space between recording outputs

def update():
    update.current_time += 1  # Increment the elapsed time by 1 second

def key_pressed(pressed):
    if pressed:
        recording_time = datetime.timedelta(seconds=update.current_time)  # Convert the elapsed time (in seconds) to a timedelta object
        hours, remainder = divmod(recording_time.seconds, 3600)  # Convert the total seconds to hours and the remainder
        minutes, seconds = divmod(remainder, 60)  # Convert the remaining seconds to minutes and seconds
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"  # Format the elapsed time as a string (HH:MM:SS)
        obs.script_log(obs.LOG_INFO, f"Recording timecode: {time_str}")  # Log the elapsed time to the OBS log
        if obs.obs_frontend_replay_buffer_active():  # If the replay buffer is active, save a clip
            obs.obs_frontend_replay_buffer_save() # Save the clip
            clip_name = get_last_replay_filename() # Get the clip name
            recording_time = f"{recording_time} | Clip: {clip_name}"
        # Record the file name and recording time to the text file
        create_log_directory()
        with open(file_path, "a") as f:  # Open the log file for appending
            f.write(f" Time: {recording_time}\n")  # Write the elapsed time (as a timedelta object) to the log file
        winsound.PlaySound(sound_path, winsound.SND_FILENAME) # Play sound for feedback

def create_log_directory():
    if not os.path.exists(os.path.dirname(file_path)):  # If the directory for the log file doesn't exist, create it
        os.makedirs(os.path.dirname(file_path))

def get_last_replay_filename():
    path = get_last_replay() # Get the replay path
    filename = os.path.basename(path) # Get just the file name
    return filename

def get_last_replay():
    replay_buffer = obs.obs_frontend_get_replay_buffer_output() # Get the buffer and return the path
    cd = obs.calldata_create()
    ph = obs.obs_output_get_proc_handler(replay_buffer)
    obs.proc_handler_call(ph, "get_last_replay", cd)
    path = obs.calldata_string(cd, "path")
    obs.calldata_destroy(cd)
    obs.obs_output_release(replay_buffer)
    return path

def script_update(settings):
    global file_path, sound_path
    file_path = obs.obs_data_get_string(settings, "file_path")  # Get the file path from the settings
    sound_path = obs.obs_data_get_string(settings, "sound_path")  # Get the feedback sound path from the settings
    update.current_time = 0  # Reset the elapsed time when the settings are updated

def script_properties():
    props = obs.obs_properties_create()  # Create a properties object for the script settings
    obs.obs_properties_add_path(props, "file_path", "Timestamp File", obs.OBS_PATH_FILE, "", "")  # Add a file path property to the settings
    obs.obs_properties_add_path(props, "sound_path", "Feedback Sound", obs.OBS_PATH_FILE, "", "")  # Add a feedback sound path property to the settings
    return props  # Return the properties object

def script_description():
    return "Manage Stream Clippy:\nRecords a timestamp to a file when the designated hotkey is pressed and saves a clip with replay buffer."  # Return a description of the script

def script_load(settings):
    obs.obs_hotkey_register_frontend("key_pressed", "MS Clippy", key_pressed) # Register the hotkey to trigger the timestamp recording
    obs.obs_frontend_add_event_callback(on_event) # Create an event listener
    obs.timer_add(update, 1000) # Start the timer for recording time

def script_unload():
    obs.obs_hotkey_unregister("key_pressed") # Unregister the hotkey to trigger the timestamp recording
    