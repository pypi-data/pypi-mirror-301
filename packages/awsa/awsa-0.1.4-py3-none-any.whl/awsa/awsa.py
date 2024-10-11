import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
import requests
from bs4 import BeautifulSoup
import asyncio
import edge_tts
import nest_asyncio
from IPython.display import Audio

# Initialize the TTS system
async def generate_speech(text: str, voice: str) -> bytes:
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = b''  # Initialize an empty bytes object
    async for audio_chunk in communicate.stream():
        audio_bytes += audio_chunk  # Append the chunk to the bytes object
    return audio_bytes

    
# Load the Qwen2VL model and processor
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "aisak-ai/O", torch_dtype="auto", device_map="auto"
)
processor = AutoProcessor.from_pretrained("aisak-ai/O")

# The TTS voice settings
VOICE = "en-GB-ThomasNeural"

# Function to scrape text from a website
def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        scraped_text = ' '.join(element.get_text() for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'li', 'span']))
        cleaned_text = scraped_text.replace('\n', ' ').replace('\\', '').strip()
        return cleaned_text
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return None

# Main loop for scraping and summarizing websites
while True:
    url = input("URL (or 'exit' to quit): ")
    if url.lower() == 'exit':
        break

    scraped_text = scrape_website(url)
    if not scraped_text:
        continue

    # Define the conversation template with system instruction
    conversation = [
        {
            "role": "system",
            "content": (
                "Your name is AISAK-O, which stands for 'Artificially Intelligent Swiss Army Knife OPTIMUM'. "
                "You are built by the AISAK team, led by Mandela Logan. You are the implementation of a multi-purpose, multimodal, AI clerk. "
                "Read the following text and extract relevant information."
                "Focus on identifying key topics, highlighting important details, and summarizing the content concisely."
                "Organize the extracted information into categories for clarity."
                "When users are curious about the information you've provided, then give in depth explanations."
            ),
        },
        {
            "role": "user",
            "content": "Give me a complete summary: " + scraped_text,
        }
    ]

    # Preprocess the inputs
    text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
    inputs = processor(text=[text_prompt], padding=True, return_tensors="pt").to("cuda")

    # Inference: Generate the output
    output_ids = model.generate(**inputs, max_new_tokens=5000)
    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(inputs.input_ids, output_ids)
    ]

    # Decode the generated output
    output_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
    )

    # Clean up the generated output before displaying to the user
    cleaned_output = output_text[0].replace('[', '').replace(']', '').replace('\\n', ' ').replace('**', '').strip()

    # Print the summary
    print("Summary: ", cleaned_output)

    # Use TTS to convert the summary to speech and play it
    nest_asyncio.apply()
    audio_bytes = asyncio.run(generate_speech(cleaned_output, VOICE))

    # Play the audio
    Audio(audio_bytes)

    # Allow for follow-up questions
    while True:
        follow_up = input("You (type 'back' for new URL): ")
        if follow_up.lower() == 'back':
            break

        # Add the follow-up question to the conversation
        conversation.append({"role": "user", "content": follow_up})

        # Preprocess and generate a response to the follow-up question
        text_prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = processor(text=[text_prompt], padding=True, return_tensors="pt").to("cuda")

        # Inference: Generate the output
        output_ids = model.generate(**inputs, max_new_tokens=5000, min_length=100)
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(inputs.input_ids, output_ids)
        ]

        # Decode the generated output
        output_text = processor.batch_decode(
            generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )

        # Clean up the generated output before displaying to the user
        cleaned_output = output_text[0].replace('[', '').replace(']', '').replace('\\n', ' ').replace('**', '').strip()

        # Display the response to the follow-up question
        print("AISAK: ", cleaned_output)

        # Optionally convert the follow-up response to speech and play it
        nest_asyncio.apply()
        audio_bytes = asyncio.run(generate_speech(cleaned_output, VOICE))
        Audio(audio_bytes)
