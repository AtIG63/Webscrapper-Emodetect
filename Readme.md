Steps to run the project
1. Download all the files from the drive.
2. Delete all the contents of the text_files folder after viewing as it already contain files from my execution of the code
3. Delte the Output Data StructureFINAL file after viewing as it contains all the result from my execution.
4. Run 'pip install -r requirements.txt' in terminal
5. Now you have the change the file location in the code.

Inside extract.py

Line no. 50 replace 
# Load the URLs from an Excel file
df = pd.read_excel('D:/PROJECTS/BlackCoffer_Assignment/Input.xlsx') with your file path.

Line no.53
# Specify the directory where text files will be saved
save_path = 'D:/PROJECTS/BlackCoffer_Assignment/text_files' with your file path.

Inside sentiment.py

Line no.20 replace
# Load your Excel file into a pandas DataFrame
file_path = 'D:/PROJECTS/BlackCoffer_Assignment/Output Data Structure.xlsx' with your file path for reference.

Line no.74 replace
file_path =f'text_files/{id_value}.txt' with your folder path which contains the extracted texts.

Line no.91 replace this
# Save the updated DataFrame back to the Excel file
output_excel_path = 'D:/PROJECTS/BlackCoffer_Assignment/Output Data StructureFinal.xlsx' with your file path and the name you want your final excel file should be.

Then simply save the changes and then run

'python runthis.py'

After few seconds(approx. 30s) the files will get extracted and the outfut excel file will be generated.

What is happening in the code?

In extract.py-
Firstly,

Setting Up: It starts by loading necessary tools for web scraping, handling data, and analyzing sentiments. It uses specific libraries to request web pages (requests), parse HTML content (BeautifulSoup), manage data (pandas), and perform sentiment analysis (NLTK).

Preparing for Sentiment Analysis: Before anything else, it ensures that the necessary parts of NLTK, particularly the VADER lexicon used for sentiment analysis, are ready to use.

Handling Web Requests Efficiently: To make web requests more efficient, it sets up a session. This is like keeping a browser window open instead of opening and closing it for each web page you visit, saving time and resources.

Scraping Web Pages: The script defines a function to visit a given web page, collect all the text found there, and return this text along with an identifier for the web page. It's designed to handle potential issues, like web pages not loading properly, by reporting any problems encountered.

Analyzing the Mood of Text: Another part of the script is dedicated to figuring out the sentiment of the collected text, determining whether it's positive, negative, or neutral. This is done using a tool that's trained to understand the emotional tone behind words.

Main Task – Fetch, Analyze, Save: The core of the script works by taking a list of web pages from an Excel file and processing them one by one. For each page, it fetches the text, analyzes its sentiment, and saves the results into a file. This process is sped up by doing several tasks at the same time, thanks to parallel processing.

Organization and Output: Before it starts, the script prepares a folder to store the results. Then, it reads the web page addresses (URLs) from an Excel sheet and begins its work. Once it's done processing all the pages, it saves the fetched text and its sentiment analysis into separate files for each URL.

Efficiency and Reporting: Finally, the script keeps track of how long it takes to finish all tasks, providing a simple report at the end.

In sentiment.py - 

Setting Up the Environment: The script starts by preparing the tools it needs. It loads linguistic resources from the NLTK library, such as tokenizers, stop words (common words that are usually ignored), and the CMU Pronouncing Dictionary for phonetic analysis. It ensures all necessary components are downloaded and ready for use.

Loading Data: It reads an Excel file into a pandas DataFrame. This file contains data that will be analyzed, including identifiers for text sources (referred to as URL_ID in the script).

Defining Analysis Functions:

1. Text Analysis: A key function (calculate_text_scores) is defined to compute various scores from the text. This includes sentiment scores (positive, negative, and compound) using both TextBlob and the NLTK's Sentiment Intensity Analyzer. It also calculates linguistic features such as average sentence length, percentage of complex words, the Fog index (which estimates the readability of English writing), syllables per word, counts of personal pronouns, and average word length.

2. Batch Processing: Another function (batch_process_rows) is designed to process a batch of rows from the DataFrame. For each row, it reads the text content from a file, calculates the text scores using the previously defined function, and then updates the DataFrame with these scores.

Processing the Data: The script processes the DataFrame in batches. It iterates through the DataFrame, applies the batch processing function to each batch of rows, and calculates the scores for the text associated with each row. This approach helps manage memory usage and improves efficiency, especially with large datasets.

Saving the Results: After all rows have been processed and the DataFrame has been updated with the calculated scores, the script saves the modified DataFrame to a new Excel file. This file contains the original data along with the newly calculated text scores.