import gi
gi.require_version('Gst', '1.0')
import socketio
import threading
from gi.repository import Gst, GLib
import requests
import signal
import json
# Initialize GStreamer
Gst.init(None)

# Setup Flask-SocketIO client
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print("Successfully connected to the server.")



@sio.on("connect_ack")
def connect_ack(data):
    print('The client gettng event from server', data)


# Connect to the Flask-SocketIO server
sio.connect("http://localhost:5555")




# Function to initialize the chatbot via HTTP POST
def init_chatbot(user_conversation_index):
    url = "http://localhost:5555/init"  # Endpoint for chatbot initialization
    response = requests.post(url, json={"user_conversation_index": user_conversation_index})
    print('ok')
    if response.ok:
        print(f"Chatbot initialized: {response.json()}")
    else:
        print(f"Failed to initialize chatbot: {response.status_code}, {response.text}")
        return 

    sio.emit("unpause_asr", {
        "user_conversation_index": 1,  # Set your user_conversation_index accordingly
        "on":"REQUEST_COMPLETE"
    }) 
   
    





# Function to send audio data to server over WebSocket
def send_audio_data(audio_data):
    if isinstance(audio_data, memoryview):
        audio_data = audio_data.tobytes()  # Convert memoryview to bytes
    sio.emit("audio_in", {
        "user_conversation_index": 1,  # Set your user_conversation_index accordingly
        "audio": audio_data  # Send bytes directly
    })

# Define the GStreamer pipeline
pipeline = None  # Define globally for access in shutdown

def start_gstreamer_pipeline():
    global pipeline
    # Define GStreamer pipeline
    pipeline = Gst.parse_launch(
        "autoaudiosrc ! audioconvert ! audioresample ! appsink name=sink"
    )
    pipeline.set_state(Gst.State.PLAYING)
    # Retrieve the appsink element
    appsink = pipeline.get_by_name("sink")
    appsink.set_property("emit-signals", True)
    appsink.set_property("max-buffers", 1)
    appsink.connect("new-sample", on_new_sample)

# Handle new audio samples
def on_new_sample(sink):
    sample = sink.emit("pull-sample")
    buf = sample.get_buffer()
    result, map_info = buf.map(Gst.MapFlags.READ)
    
    if result:
        audio_data = map_info.data
        send_audio_data(audio_data)
        buf.unmap(map_info)
    
    return Gst.FlowReturn.OK

# Gracefully shutdown all components
def shutdown_this():
    print("Stopping client...")
    # Stop GStreamer pipeline
    if pipeline:
        pipeline.set_state(Gst.State.NULL)
    # Disconnect Socket.IO
    sio.disconnect()
    # Quit the GLib main loop
    main_loop.quit()
    pipeline_thread.join()
    stream_thread.join()

# initiating the chatbot
init_chatbot(1)



# Function to handle transcript streaming
def handle_stream_transcripts(user_conversation_index):
    url = f"http://localhost:5555/stream/{user_conversation_index}"
    try:
        with requests.get(url, stream=True) as response:
            if response.status_code == 200:
                print("Connected to the transcript stream.")
                for line in response.iter_lines():
                    if line:
                        # Decode the received JSON line
                        transcript_data = json.loads(line.decode('utf-8'))
                        print("Transcription received:", transcript_data.get("text", "No text"))
            else:
                print(f"Stream connection failed with status: {response.status_code}")
    except requests.RequestException as e:
        print(f"Stream connection error: {e}")





# Start GStreamer pipeline in a separate thread
pipeline_thread = threading.Thread(target=start_gstreamer_pipeline, daemon=True)
pipeline_thread.start()
import time
time.sleep(1)
# Start the transcript stream in a separate thread
stream_thread = threading.Thread(target=handle_stream_transcripts, args=(1,), daemon=True)
stream_thread.start()

# Create a GLib main loop
main_loop = GLib.MainLoop()




# Keep the program running to maintain WebSocket and GStreamer pipeline
try:
    main_loop.run()  # Run the main loop
except KeyboardInterrupt:
    shutdown_this()
