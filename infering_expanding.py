# @Author: Sushant Das
# @Date: 23-10-2024
# @Last Modified by: Sushant Das
# @Last Modified time: 23-10-2024
# @Title: Python program to perform Gen AI tasks infering and expanding using Gemini API

import google.generativeai as genai
import os
import csv
import pandas as pd

# Function to perform sentiment analysis on the reviews in the CSV
def sentiment_analysis(chat_session):
    # Open the CSV file containing sample reviews in read mode
    with open("sample_reviews.csv", mode='r') as file:
        csv_reader = csv.reader(file)  # Create a CSV reader object
        
        # Skip the header row of the CSV (Product, Review)
        next(csv_reader)
        
        # Iterate through each row in the CSV
        for row in csv_reader:
            # Prepare the prompt to categorize the sentiment of the review as Positive, Negative, or Neutral
            prompt = f"Categorize the sentiment in one word of this review in Postive/Negative/Neutral {row[1]}"
            # Send the prompt to the generative AI model for sentiment analysis
            sentiment = chat_session.send_message(prompt)
            
            # Prepare another prompt to generate a 40-word reply to the review based on the determined sentiment
            prompt = f"Add a 40 words reply to this review: {row[1]} as per sentiment {sentiment}"
            # Get the AI-generated reply for the review
            reply = chat_session.send_message(prompt)
            
            # Save the product, review, sentiment, and reply to a new CSV file
            save_to_csv(row[0], row[1], sentiment.text, reply.text)

# Function to save the processed data to a new CSV file
def save_to_csv(product, review, sentiment, reply):
    # Create a tuple (row) with the product, review, sentiment, and AI-generated reply
    row = (product, review, sentiment, reply)
    
    # Open the CSV file for appending, or create it if it doesn't exist
    with open("processed_reviews.csv", 'a', encoding='utf-8') as file:
        writer = csv.writer(file)  # Create a CSV writer object
        
        # Check if the file is empty to write the header row
        if file.tell() == 0:
            writer.writerow(['Product', 'Review', 'Sentiment', 'Reply'])  # Write the header row
        
        # Write the data (product, review, sentiment, reply) to the CSV file
        writer.writerow(row)

# Main function to configure the model and start the sentiment analysis process
def main():
    # Configure the Google generative AI model using the API key from environment variables
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
    # Instantiate the generative model (Gemini 1.5 flash version)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Start a new chat session with the model
    chat_session = model.start_chat(
        history=[]  # Initialize with an empty conversation history
    )
    
    # Call the sentiment analysis function to process the reviews
    sentiment_analysis(chat_session)

# Entry point of the script
if __name__=="__main__":
    main()