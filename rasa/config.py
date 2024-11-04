riva_config = {
    "RIVA_SPEECH_API_URL": "localhost:50051", # Replace the IP port with your hosted RIVA endpoint
    "WEATHERSTACK_ACCESS_KEY": "",  # Get your access key at - https://weatherstack.com/
    "VERBOSE": True  # print logs/details for diagnostics
}

tts_config = {
    "TTS_API_URL":"http://localhost:5010/synthesize",
    "VERBOSE": True, # Print logs/details for diagnostics
    "SAMPLE_RATE": 22050, # The speech is generated at this sampling rate. The only value currently supported is 22050
    "LANGUAGE_CODE": "en-US", # The language code as a BCP-47 language tag. The only value currently supported is "en-US"
    "VOICE_NAME": "English-US-Female-1", # Options are English-US-Female-1 and English-US-Male-1
}

object_finder_config = {
    "OF_API_URL":"http://localhost:5000/",
    "VERBOSE": True, # Print logs/details for diagnostics
}