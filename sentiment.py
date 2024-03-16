from textblob import TextBlob
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import download
from nltk.corpus import cmudict
import pandas as pd
# Download NLTK resources (if not already downloaded)
download('punkt')
download('stopwords')
download('averaged_perceptron_tagger')
download('words')
download('cmudict')
# Load the CMU Pronouncing Dictionary
pronouncing_dict = cmudict.dict()
# Initialize the Sentiment Intensity Analyzer
sid = SentimentIntensityAnalyzer()
# Load your Excel file into a pandas DataFrame
file_path = 'D:/PROJECTS/BlackCoffer_Assignment/Output Data Structure.xlsx'
df = pd.read_excel(file_path)
# Specify the batch size for processing
batch_size = 100
# Function to calculate text-related scores
def calculate_text_scores(text, stop_words):
    blob = TextBlob(text)
    
    # Sentiment analysis scores using TextBlob's default implementation
    sentiment_scores = sid.polarity_scores(text)
    positive_score = sentiment_scores['pos']
    negative_score = -positive_score
    polarity_score = sentiment_scores['compound']
    
    subjectivity_score = blob.sentiment.subjectivity
    
    # Other text-related scores
    sentences = sent_tokenize(text)
    
    avg_sentence_length = len(word_tokenize(text)) / len(sentences)
    
    complex_words = [word for word in word_tokenize(text) if word.lower() not in stop_words]
    
    percentage_of_complex_words = (len(complex_words) / len(word_tokenize(text))) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)
    avg_words_per_sentence = len(word_tokenize(text)) / len(sentences)
    complex_word_count = len(complex_words)
    word_count = len(word_tokenize(text))
    
    def count_syllables(word, syllable_dict):
        return max([len(list(y for y in x if y[-1].isdigit())) for x in syllable_dict.get(word.lower(), [[]])])

    syllable_per_word = sum([count_syllables(w, pronouncing_dict) for w in word_tokenize(text)]) / word_count
    
    # Count personal pronouns
    personal_pronouns = ['I', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours']
    personal_pronoun_count = sum(text.lower().count(pronoun) for pronoun in personal_pronouns)

    # Calculate average word length
    avg_word_length = sum(len(word) for word in word_tokenize(text)) / len(word_tokenize(text))
    
    return positive_score, negative_score, polarity_score, subjectivity_score, \
           avg_sentence_length, percentage_of_complex_words, fog_index, \
           avg_words_per_sentence, complex_word_count, word_count, \
           syllable_per_word, personal_pronoun_count, avg_word_length


# Function to batch process rows
def batch_process_rows(df, start_index, end_index):
    stop_words = set(stopwords.words('english'))
    
    for index in range(start_index, end_index):
        id_value = df.at[index, 'URL_ID']
        file_path =f'text_files/{id_value}.txt'

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text_data = file.read()
                text_scores = calculate_text_scores(text_data, stop_words)

                # Update the DataFrame with the calculated scores
                df.loc[index, ['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
                               'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
                               'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
                               'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']] = text_scores

# Iterate over the DataFrame rows in batches and fill the empty columns with text-related scores
for i in range(0, len(df), batch_size):
    batch_process_rows(df, i, min(i + batch_size, len(df)))

# Save the updated DataFrame back to the Excel file
output_excel_path = 'D:/PROJECTS/BlackCoffer_Assignment/Output Data StructureFinal.xlsx'
df.to_excel(output_excel_path, index=False)