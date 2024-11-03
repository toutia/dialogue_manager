from rasa.core.channels.rest import RestInput
from custom_output_channel import CustomOutputChannel  # Adjust as necessary

if __name__ == "__main__":
    # Start Rasa with your custom output channel
    rasa.run(
        input_channel=RestInput(),
        output_channel=CustomOutputChannel(),
        # Other parameters...
    )
