# Text Analysis of Online Articles using Python (newspaper3k module)
This project involves extracting text data from online articles and analysing the sentiment and readibility of the content by calculating various metrics such as positive score, negative score, subjectivity score, FOG index etc.

# Methodology Adopted

1. Sentiment Analysis:<br />
Sentiment analysis is the process of determining whether a piece of writing is positive, negative, or neutral. The below Algorithm is designed for use in Financial Texts. It consists of steps:<br />
1.1	Cleaning using Stop Words Lists<br />
The Stop Words Lists (found in the folder StopWords) are used to clean the text so that Sentiment Analysis can be performed by excluding the words found in Stop Words List. <br />
1.2	Creating a dictionary of Positive and Negative words<br />
The Master Dictionary (found in the folder MasterDictionary) is used for creating a dictionary of Positive and Negative words. We add only those words in the dictionary if they are not found in the Stop Words Lists. <br />
1.3	Extracting Derived variables<br />
We convert the text into a list of tokens using the nltk tokenize module and use these tokens to calculate the 4 variables described below:<br />
Positive Score: This score is calculated by assigning the value of +1 for each word if found in the Positive Dictionary and then adding up all the values.<br />
Negative Score: This score is calculated by assigning the value of -1 for each word if found in the Negative Dictionary and then adding up all the values. We multiply the score with -1 so that the score is a positive number.<br />
Polarity Score: This is the score that determines if a given text is positive or negative in nature. It is calculated by using the formula: <br />
Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001) (ranges from -1 to 1) <br />
Subjectivity Score: This is the score that determines if a given text is objective or subjective. It is calculated by using the formula:<br /> 
Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001) (ranges from 0 to 1) <br />

2. Analysis of Readability:<br />
Analysis of Readability is calculated using the Gunning Fox index formula described below.<br />
Average Sentence Length = the total number of characters / the total number of sentences<br />
Percentage of Complex words = the total number of complex words / the total number of words <br />
Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)<br />

   (Complex wordsare words in the text that contain more than two syllables.)<br />
   (We count the total cleaned words present in the text by:
      1.	removing the stop words (using stopwords class of nltk package).<br />
      2.	removing any punctuations like ? ! , . from the word before counting.)<br />

3. Other Variables:<br />
   A. Average Number of Words Per Sentence = the total number of words / the total number of sentences<br />
   B. Average Word Length = Sum of the total number of characters in each word/Total number of words<br />
   C. Total Personal Pronouns: Used regex to find the counts of the words such as “I,” “we,” “my,” “ours,” and “us”. Special care is taken so that the country name US is not included in the list.<br />
   D. Syllable Count Per Word: Used nltk's cmudict dictionary.<br />

# How the code works:<br />
The code takes in an excel file with a column of urls as input.<br />
First comes the extraction part,<br />
•	I started by first extracting all the articles into text files using Article() class of newspaper module. This would ensure smooth analysis in the code ahead.<br />
•	For this purpose, I made a function to extract article title and article content from a particular URL and return a single string file.<br />
•	Further, ran all URLs provided in a loop and created a separate text file for each article.<br />
Now, onto the analysis part,<br />
•	In a separate .py file named “analysis”, imported everything from the “extraction.py” file.<br />
•	Started with creating a master dictionary, which would have “positive” and “negative” keys and the positive and negative words as their respective values.<br />
•	Proceeded to create a function to count syllables in a word since it would be required later on.<br />
•	This will be covered using two functions,<br />
     o	First: A function which uses nltk’s cmu.dict(), which is an extensive dictionary containing a large number of English words and their respective pronunciations.<br />
     o	Second: If there comes a word with no respective key in the dictionary, we will calculate the number of syllables it has by using a custom-made function, which loosely generalizes the method of syllable recognition in a word.<br />
•	Further, defined a function named “analyse_text” taking on “filename” as a variable, which would just be the name of the text file we want to analyze. This will return a row containing URL ID, URL, and all the relevant variables with which we can assess and analyze the article. Later, a loop will be created to analyze all files at once by feeding their file names into this function which will be inside the loop.<br />
•	 This function takes the file name, reads the text inside it and cleans it by removing stop words, then proceeds to create lists of words and sentences. Now, we have everything in place to calculate the required metrics.<br />
•	Now, before starting the loop, an empty list is initialized, which we will use to store all the URLs with their respective metrics, in a multi-dimensional array.<br />
•	This array is now converted into a Pandas DataFrame and exported as an excel file using Pandas’ “to_csv()”. <br />

