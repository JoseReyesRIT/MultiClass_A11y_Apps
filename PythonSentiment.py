import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import csv
import json

key = ""#Add Microsoft Azure service key
endpoint = ""#Add Microsoft Azure endpoit
documents_1 = []
documents_2 = []

input_file = ""#Input File location
output_sentiment = ""#Output path for sentiment analysis
output_key = ""#output path for key_phrase extraction

with open(input_file, encoding="utf8", mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            record = {"id" : row["Review_text"] + " , " + row["Category"], "language": "en", "text": row["Review_text"]}
            documents_1.append(record)
            line_count += 1
        else:
            record = {"id" : row["Review_text"] + " , " + row["Category"], "language": "en", "text": row["Review_text"]}
            #documents.append(f"'id': " + str(line_count) + f'", "en", "text": "{row["Review_text"]}"')

            if line_count < 601:
                documents_1.append(record)
            else:
                documents_2.append(record)
            line_count += 1

        #if line_count == 2:
        #    break;

    print(f'Processed {line_count} lines.')

def authenticateClient():
    credentials = CognitiveServicesCredentials(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client

def sentiment():
    
    client = authenticateClient()

    try:
        if len(documents_1) > 0:
            response_1 = client.sentiment(documents=documents_1)
        if len(documents_2) > 0:
            response_2 = client.sentiment(documents=documents_2)

        i = 1
        with open(output_sentiment, encoding="utf8", mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if len(documents_1) > 0:
                for document in response_1.documents:
                    print(i, "Sentiment Score: ", "{:.2f}".format(document.score))
                    i = i = 1

                    rec = document.id.split(",")
                    writer.writerow([rec[0], rec[1], "{:.2f}".format(document.score)])
            if len(documents_2) > 0:
                for document in response_2.documents:
                    print(i, "Sentiment Score: ", "{:.2f}".format(document.score))
                    i = i = 1

                    rec = document.id.split(",")
                    writer.writerow([rec[0], rec[1], "{:.2f}".format(document.score)])
                

    except Exception as err:
        print("Encountered exception. {}".format(err))

def keyphrases():
    client = authenticateClient()
    try:
        if len(documents_1) > 0:
            response_1 = client.key_phrases(documents=documents_1)
        if len(documents_2) > 0:
            response_2 = client.key_phrases(documents=documents_2)

        i = 1
        with open(output_key, encoding="utf8", mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            if len(documents_1) > 0:
                for document in response_1.documents:
                    print(i, "Key Phrases: ")
                    i = i + 1

                    key_phrases = ""
                    for phrase in document.key_phrases:
                        print("\t\t", phrase)
                        key_phrases = key_phrases + ", " + phrase

                    rec = document.id.split(",")
                    writer.writerow([rec[0], rec[1], key_phrases])
            if len(documents_2) > 0:
                for document in response_2.documents:
                    print(i, "Key Phrases: ")
                    i = i + 1

                    key_phrases = ""
                    for phrase in document.key_phrases:
                        print("\t\t", phrase)
                        key_phrases = key_phrases + ", " + phrase

                    rec = document.id.split(",")
                    writer.writerow([rec[0], rec[1], key_phrases])
                

    except Exception as err:
        print("Encountered exception. {}".format(err))

keyphrases()
#sentiment()