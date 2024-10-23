# @Author: Sushant Das
# @Date: 23-10-2024
# @Last Modified by: Sushant Das
# @Last Modified time: 23-10-2024
# @Title: Python program to perform Gen AI tasks transformation and summarization using Gemini API

import google.generativeai as genai
import os
import csv

# Function to summarize and process an email
def email_summarization(content, chat_session):
    # Prepare the prompt to summarize the email in two lines
    prompt = f"Summarize the email below in two lines {content}"
    # Send the prompt to the generative AI model to get a summary
    response = chat_session.send_message(prompt)
    
    # Extract the sender and receiver information from the email content
    mail_info = extract_email_info(content)
    sender = mail_info[0]
    receiver = mail_info[1]
    
    # Get the summary text from the model's response
    summary = response.text

    # Perform a language transformation (e.g., translate the summary to German)
    transformed_mail = email_transformation(summary, chat_session)

    # Save the sender, receiver, summary, and transformed email to a CSV file
    save_to_csv(sender, receiver, summary, transformed_mail)

# Function to transform (translate) the email summary into German
def email_transformation(summary, chat_session):
    # Prepare the prompt to translate the summary into German
    prompt = f"Translate the following text to German {summary}"
    # Send the translation request to the generative AI model
    response = chat_session.send_message(prompt)
    # Return the translated text
    transformed_mail = response.text
    return transformed_mail

# Function to extract sender and receiver information from the email content
def extract_email_info(email):
    # Split the email into lines
    lines = email.split("\n")
    # Initialize sender and receiver variables
    sender = receiver = None
    # Iterate over the lines to find sender and receiver information
    for line in lines:
        if line.startswith("From:"):
            # Extract the sender email address
            sender = line.split(":")[1].strip()
        elif line.startswith("To:"):
            # Extract the receiver email address
            receiver = line.split(":")[1].strip()
    # Return the sender and receiver as a tuple
    return sender, receiver

# Function to save the processed email information to a CSV file
def save_to_csv(sender, receiver, summary, transformed_mail):
    # Create a row with the sender, receiver, summary, and translated mail
    row = (sender, receiver, summary, transformed_mail)
    
    # Open (or create) the CSV file in append mode
    with open("email_summary.csv", 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Check if the file is empty, and write the header row if it is
        if file.tell() == 0:
            writer.writerow(['Sender', 'Receiver', 'Summary', 'Translation'])  # Write the header
        # Write the email information row to the CSV file
        writer.writerow(row)

# Main function to configure the generative AI model and process multiple emails
def main():
    # Configure the generative AI model using the API key from environment variables
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Instantiate the generative model (Gemini 1.5 flash version)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Start a new chat session with the model
    chat_session = model.start_chat(
        history=[]  # Initialize with an empty conversation history
    )

    # Define the folder containing the sample emails
    folder_path = "sample_mails/"
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        # Construct the full path of the file
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file (and not a directory)
        if os.path.isfile(file_path):
            # Open and read the email content from the file
            with open(file_path, 'r') as file:
                content = file.read()
                # Process the email by summarizing and translating it
                email_summarization(content, chat_session)

# Run the main function if this script is executed
if __name__=="__main__":
    main()