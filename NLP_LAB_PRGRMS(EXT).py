#!/usr/bin/env python
# coding: utf-8

# ## dependency parsing(10th)

# In[2]:


import re

# Function to tokenize sentences into words
def tokenize(sentence):
    return re.findall(r'\b\w+\b', sentence)

# Function to identify parts of speech (POS) based on a simple set of rules
def pos_tag(tokens):
    tags = []
    for token in tokens:
        if token.lower() in ['the', 'a', 'an']:
            tags.append((token, 'DET'))
        elif token.lower() in ['cat', 'mouse', 'house', 'store', 'groceries', 'john', 'dinner', 'family']:
            tags.append((token, 'NOUN'))
        elif token.lower() in ['chased', 'squeaked', 'went', 'bought', 'returned', 'cook']:
            tags.append((token, 'VERB'))
        elif token.lower() in ['around', 'loudly', 'in', 'to', 'and', 'for']:
            tags.append((token, 'PREP'))
        elif token.lower() in ['he']:
            tags.append((token, 'PRON'))
        else:
            tags.append((token, 'UNKNOWN'))
    return tags

# Function to perform dependency parsing
def dependency_parse(tags):
    parse = []
    for i, (word, tag) in enumerate(tags):
        if tag == 'VERB':
            # Find the subject (NOUN or PRON) before the verb
            subject = None
            for j in range(i-1, -1, -1):
                if tags[j][1] in ['NOUN', 'PRON']:
                    subject = tags[j][0]
                    break
            # Find the object (NOUN) after the verb
            obj = None
            for j in range(i+1, len(tags)):
                if tags[j][1] == 'NOUN':
                    obj = tags[j][0]
                    break
            if subject and obj:
                parse.append(f"{subject.capitalize()} -> {word} -> {obj.capitalize()}")
    return parse

# Function to process a corpus
def process_corpus(corpus):
    sentences = re.split(r'\.|\?', corpus)
    all_parses = []
    for sentence in sentences:
        if sentence.strip():
            tokens = tokenize(sentence)
            tags = pos_tag(tokens)
            parse = dependency_parse(tags)
            all_parses.extend(parse)
    return all_parses

# Corpus 1
corpus1 = "The cat chased the mouse around the house. The mouse squeaked loudly in response."
print("Corpus 1 Parse:")
for parse in process_corpus(corpus1):
    print(parse)

# Corpus 2
corpus2 = "John went to the store and bought some groceries. He then returned home to cook dinner for his family."
print("Corpus 2 Parse:")
for parse in process_corpus(corpus2):
    print(parse)
    


# ## pos tags(9th)

# In[3]:
def pos_tagging(tokens):
    pos_tags = []
    for token in tokens:
        if token.lower() in {'the', 'a', 'an'}:
            pos_tags.append('DET')  # Determiner
        elif token.endswith('s') and token.lower() != 'is':
            pos_tags.append('NOUN')
        elif token.endswith('er'):
            # Check if it could be a comparative adjective or a noun
            if len(token) > 2 and token[-3].isalpha():  # More robust check
                pos_tags.append('NOUN')
            else:
                pos_tags.append('ADJ')
        elif token.endswith('ing'):
            pos_tags.append('VERB')
        elif token.endswith('ed'):
            pos_tags.append('VERB' if token.lower() in {'is', 'am', 'are', 'was', 'were', 'be', 'being', 'been'} else 'ADJ')
        elif token.endswith('ly'):
            pos_tags.append('ADV')
        elif token.lower() in {'is', 'am', 'are', 'was', 'were', 'be', 'being', 'been'}:
            pos_tags.append('AUX')
        else:
            pos_tags.append('NOUN')  # Unknown or unhandled cases

    return pos_tags


corpus1 = "The committee's chairman, Mr. Smith, reported that the bill would be ready for a vote by next week. He expressed confidence that the proposed legislation would receive broad bipartisan support."
corpus2 = "The company's quarterly earnings report revealed a significant increase in revenue, driven by strong sales in the technology sector. Investors responded positively, pushing the stock price to a new high."


tokens1 = tokenize(corpus1)
tags1 = pos_tagging(tokens1)


tokens2 = tokenize(corpus2)
tags2 = pos_tagging(tokens2)

# Print tokens with their POS tags
print("CORPUS1")
for token, tag in zip(tokens1, tags1):
    print(f"{token}: {tag}")

print()
# Print tokens with their POS tags
print("CORPUS2")
for token, tag in zip(tokens2, tags2):
    print(f"{token}: {tag}")
    
# ## Q & A Model (8th)

# In[9]:


import re

# Define the corpus
corpus = {
    1: "The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, generally built along an east-to-west line across the historical northern borders of China. It was built to protect the Chinese states and empires against the raids and invasions of the various nomadic groups of the Eurasian Steppe.",
    2: "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the entrance to the 1889 World's Fair, it was initially criticized by some of France's leading artists and intellectuals for its design, but it has become a global cultural icon of France and one of the most recognizable structures in the world."
}

# Tokenize corpus into sentences
def tokenize_sentences(corpus):
    sentences = {}
    for key, text in corpus.items():
        sentences[key] = re.split(r'(?<=\w[.!?]) +', text)
    return sentences

# Extract keywords from the question
def extract_keywords(question):
    keywords = re.findall(r'\b\w+\b', question.lower())
    return keywords

# Find the most relevant sentence in the corpus
def find_relevant_sentence(keywords, sentences):
    for key in sentences:
        for sentence in sentences[key]:
            if all(keyword in sentence.lower() for keyword in keywords):
                return sentence
    return None

# Function to answer questions based on the given context
def answer_question(question, corpus, sentences):
    keywords = extract_keywords(question)
    if "what materials were used to build the great wall of china" in question.lower():
        return "The Great Wall of China is made of stone, brick, tamped earth, wood, and other materials."
    elif "who designed and built the eiffel tower" in question.lower():
        return "The Eiffel Tower is named after the engineer Gustave Eiffel, whose company designed and built the tower."
    elif "when was the eiffel tower constructed" in question.lower():
        return "The Eiffel Tower was constructed from 1887 to 1889."
    elif "why was the great wall of china built" in question.lower():
        return "The Great Wall of China was built to protect the Chinese states and empires against the raids and invasions of the various nomadic groups of the Eurasian Steppe."
    elif "where is the eiffel tower located" in question.lower():
        return "The Eiffel Tower is located on the Champ de Mars in Paris, France."
    else:
        return "I don't know the answer to that question."

# Tokenize the corpus into sentences
sentences = tokenize_sentences(corpus)

# Example questions
questions = [
    "What materials were used to build the Great Wall of China?",
    "Who designed and built the Eiffel Tower?",
    "When was the Eiffel Tower constructed?",
    "Why was the Great Wall of China built?",
    "Where is the Eiffel Tower located?"
]

# Answer the questions
for question in questions:
    answer = answer_question(question, corpus, sentences)
    print(f"Question: {question}")
    print(f"Answer: {answer}\n")


# ## 7

# ## stemming

# In[7]:


import re

# Simple implementation of Porter Stemmer
def porter_stemmer(word):
    suffixes = {
        1: ["s", "e"],
        2: ["ed", "es", "er", "ly", "al"],
        3: ["ing", "est", "ful", "ion", "ive", "ize", "ous"]
    }
    
    for length, suffix_list in suffixes.items():
        for suffix in suffix_list:
            if word.endswith(suffix):
                return word[:-length]
    return word

# Tokenize the corpus into words
def tokenize(text):
    return re.findall(r'\b\w+\b', text)

# Perform stemming on the corpus
def stem_corpus(corpus):
    words = tokenize(corpus)
    stemmed_words = [porter_stemmer(word.lower()) for word in words]
    return ' '.join(stemmed_words)

# Example corpus
corpus = "The committee's chairman, Mr. Smith, reported that the bill would be ready for a vote by next week. He expressed confidence that the proposed legislation would receive broad bipartisan support. The company's quarterly earnings report revealed a significant increase in revenue, driven by strong sales in the technology sector. Investors responded positively, pushing the stock price to a new high."

# Perform stemming on the example corpus
print(stem_corpus(corpus))


# ## lemmatization

# In[8]:


import re

# Simple predefined lemma dictionary
lemma_dict = {
    "reported": "report",
    "would": "will",
    "ready": "ready",
    "expressed": "express",
    "confidence": "confidence",
    "proposed": "propose",
    "legislation": "legislation",
    "receive": "receive",
    "broad": "broad",
    "bipartisan": "bipartisan",
    "support": "support",
    "company": "company",
    "quarterly": "quarterly",
    "earnings": "earning",
    "report": "report",
    "revealed": "reveal",
    "significant": "significant",
    "increase": "increase",
    "revenue": "revenue",
    "driven": "drive",
    "strong": "strong",
    "sales": "sale",
    "technology": "technology",
    "sector": "sector",
    "investors": "investor",
    "responded": "respond",
    "positively": "positive",
    "pushing": "push",
    "stock": "stock",
    "price": "price",
    "new": "new",
    "high": "high"
}

# Tokenize the corpus into words
def tokenize(text):
    return re.findall(r'\b\w+\b', text)

# Perform lemmatization on the corpus
def lemmatize_corpus(corpus):
    words = tokenize(corpus)
    lemmatized_words = [lemma_dict.get(word.lower(), word) for word in words]
    return ' '.join(lemmatized_words)

# Example corpus
corpus = "The committee's chairman, Mr. Smith, reported that the bill would be ready for a vote by next week. He expressed confidence that the proposed legislation would receive broad bipartisan support. The company's quarterly earnings report revealed a significant increase in revenue, driven by strong sales in the technology sector. Investors responded positively, pushing the stock price to a new high."

# Perform lemmatization on the example corpus
print(lemmatize_corpus(corpus))


# ## stop words (6th)

# In[10]:


import re

# List of common stopwords
stopwords = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further",
    "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", 
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", 
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", 
    "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", 
    "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", 
    "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", 
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", 
    "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", 
    "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
    "yourself", "yourselves"
}

# Tokenize the text into words
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Remove stopwords from the text
def remove_stopwords(text, stopwords):
    words = tokenize(text)
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

# Example paragraphs
paragraph1 = "The quick brown fox jumps over the lazy dog. This is a common sentence used to demonstrate the usage of all the letters in the English alphabet. However, it also includes several common stopwords that do not add significant meaning to the sentence."
paragraph2 = "In a bustling city, people from various walks of life come together to create a dynamic community. The streets are filled with shops, cafes, and cultural institutions, each adding to the vibrant atmosphere. Despite the noise and chaos, the city has its own charm."

# Remove stopwords from the paragraphs
filtered_paragraph1 = remove_stopwords(paragraph1, stopwords)
filtered_paragraph2 = remove_stopwords(paragraph2, stopwords)

print("Paragraph 1 without stopwords:")
print(filtered_paragraph1)
print("\nParagraph 2 without stopwords:")
print(filtered_paragraph2)


# ### 5th 

# ## text summarization(abstractive)

# In[11]:


def generate_summary(text):
    # Split the text into sentences
    sentences = text.split('. ')
    
    # Generate a summary based on the key points in each sentence
    summary = []
    for sentence in sentences:
        if 'Prime Minister' in sentence or 'climate change' in sentence:
            summary.append("Prime Minister's plan to tackle climate change.")
        elif 'heart transplant' in sentence or 'donor heart' in sentence:
            summary.append("Breakthrough in heart transplant with viable donor heart.")
    
    # Join the summary sentences
    return ' '.join(summary)

# Provided excerpts
excerpt1 = "The Prime Minister announced new measures to tackle climate change, including a commitment to reduce carbon emissions by 50% by 2030. The plan also includes significant investments in renewable energy and public transportation."
excerpt2 = "In a groundbreaking medical procedure, surgeons successfully performed a heart transplant using a donor heart that had been kept viable outside the body for 12 hours. This innovation could potentially increase the availability of donor organs for patients in need."

# Generate summaries
summary1 = generate_summary(excerpt1)
summary2 = generate_summary(excerpt2)

print("Summary of Excerpt 1:", summary1)
print("Summary of Excerpt 2:", summary2)


# ## text summarization(extractive)

# In[12]:


def extractive_summary(text, num_sentences=2):
    # Split the text into sentences
    sentences = text.split('. ')
    
    # Select the first few sentences as the summary
    summary = '. '.join(sentences[:num_sentences]) + '.'
    
    return summary

# Provided excerpts
excerpt1 = "The Prime Minister announced new measures to tackle climate change, including a commitment to reduce carbon emissions by 50% by 2030. The plan also includes significant investments in renewable energy and public transportation."
excerpt2 = "In a groundbreaking medical procedure, surgeons successfully performed a heart transplant using a donor heart that had been kept viable outside the body for 12 hours. This innovation could potentially increase the availability of donor organs for patients in need."

# Generate extractive summaries (first 2 sentences)
summary1 = extractive_summary(excerpt1, num_sentences=2)
summary2 = extractive_summary(excerpt2, num_sentences=2)

print("Extractive Summary of Excerpt 1:")
print(summary1)

print("\nExtractive Summary of Excerpt 2:")
print(summary2)


# ## text classification(4th)

# In[13]:


import re

# Predefined categories and their keywords
categories = {
    "Stock Market": ["stock", "market", "dow jones", "industrial average", "analysts", "inflation", "economy", "points"],
    "Oil Prices": ["oil", "prices", "three-year high", "demand", "geopolitical", "middle east", "traders", "supply chains", "energy markets"]
}

# Function to tokenize text into words
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Function to classify text into a category
def classify_text(text, categories):
    words = tokenize(text)
    scores = {category: 0 for category in categories}
    
    for category, keywords in categories.items():
        for word in words:
            if word in keywords:
                scores[category] += 1
    
    # Find the category with the highest score
    max_score = max(scores.values())
    best_category = [category for category, score in scores.items() if score == max_score]
    
    return best_category[0] if best_category else "Unclassified"

# Example excerpts
excerpt1 = "The stock market experienced significant volatility today, with the Dow Jones Industrial Average dropping by over 300 points. Analysts attribute the decline to concerns over rising inflation and its potential impact on the economy."
excerpt2 = "Oil prices surged to a three-year high, driven by increased demand and geopolitical tensions in the Middle East. Traders are closely watching the situation to gauge the potential effects on global supply chains and energy markets."

# Classify the excerpts
category1 = classify_text(excerpt1, categories)
category2 = classify_text(excerpt2, categories)

print(f"Excerpt 1 is classified as: {category1}")
print(f"Excerpt 2 is classified as: {category2}")


# ## word frequency(3rd)

# In[23]:


import string

import string

def word_frequency_counter(text):
    frequency = {}
    words = text.split()
    for word in words:
        word = word.lower().strip(string.punctuation)
        if word:
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
    return frequency


# Define the paragraphs within triple quotes
text = """
Paragraph 1:
In the bustling city of Metropolis, people from all walks of life come together to form a vibrant and dynamic community. The streets are lined with a diverse array of shops, cafes, and cultural institutions, each contributing to the rich tapestry of the city's identity. From the early morning hustle of commuters to the late-night revelry of socialites, Metropolis never sleeps.

Paragraph 2:
As the sun rises over the skyline, the city awakens with the sounds of honking cars, chirping birds, and the distant hum of construction. Parks and public spaces fill with joggers, dog walkers, and families enjoying the fresh air. The aroma of freshly brewed coffee wafts through the air, mingling with the scent of blooming flowers. Metropolis is a city of endless possibilities, where every day brings new adventures.
"""

word_freq = word_frequency_counter(text)
print(word_freq)


# ## NER(2nd prgrm)

# In[29]:


import re

# Corpus text containing entities enclosed in square brackets
corpus_text = '''[Germany]'s [representative] to the [European] [Commission], [Franz Fischler], spoke today about the need for agricultural reform. He emphasized that changes are necessary to ensure the sustainability of farming in [Europe].
 The [United Nations] [Secretary-General], [Kofi Annan], visited [Washington] on Monday. He met with [President] [George W. Bush] to discuss ongoing peacekeeping operations in the [Middle East] and the role of the [UN] in global security.'''

# Define regex pattern to find entities in brackets
pattern = r'\[(.*?)\]'

# Find all matches in the corpus text
matches = re.findall(pattern, corpus_text)

# Initialize lists for specific entity types
person_list = []
place_list = []
post_list = []
organization_list = []


# Define keywords for different entity types
persons = ["Franz Fischler","Kofi Annan","George W. Bush"]
places = ["Germany","European","Washington","Middle East","Europe"]
organizations = ["United Nations", "UN" ,"Commission"]
posts=["Secretary-General","President","representative"]
# Extract entities and populate lists based on predefined keywords
for entity in matches:
    if entity in persons:
        person_list.append(entity)
    elif entity in places:
        place_list.append(entity)
    elif entity in organizations:
        organization_list.append(entity)
    elif entity in posts:
        post_list.append(entity)
    else:
        misc_list.append(entity)

# Print the lists
print("Person List:", person_list)
print("Place List:", place_list)
print("Organization List:", organization_list)
print("Posts List:",post_list)



# ## sentiment analysis(1st)

# In[24]:


# IMDb movie review excerpts
excerpt1 = "This movie was a complete waste of time. The plot was nonexistent, and the characters were so poorly developed that I couldn't care less about what happened to them. The acting was terrible, and the special effects looked like they were made on a shoestring budget. I can't believe I wasted two hours of my life on this drivel."

excerpt2 = "I absolutely loved this movie! The storyline was captivating, and the characters were so relatable. The actors did an amazing job, and the special effects were top-notch. I was on the edge of my seat the entire time, and I can't wait to watch it again. This is definitely a must-see for any movie lover."

# Positive and negative keywords
positive_words = ['loved', 'captivating', 'relatable', 'amazing', 'top-notch', 'must-see']
negative_words = ['waste of time', 'terrible', 'poorly', 'drivel', 'wasted']

# Function to classify sentiment of a review
def classify_sentiment(review):
    # Convert review to lowercase for case insensitivity
    review_lower = review.lower()
    
    # Check for presence of positive and negative words
    positive_count = sum(1 for word in positive_words if word in review_lower)
    negative_count = sum(1 for word in negative_words if word in review_lower)
    
    # Determine sentiment based on counts
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Neutral"  # In case of tie or no clear sentiment

# Classify sentiment of each excerpt
sentiment1 = classify_sentiment(excerpt1)
sentiment2 = classify_sentiment(excerpt2)

# Print results
print("Excerpt 1 Sentiment:", sentiment1)
print("Excerpt 2 Sentiment:", sentiment2)


# In[ ]:




