import re
import json
import requests
from bs4 import BeautifulSoup

# The above lines import a bunch of libraries that we use for the code below
# re is a string management library
# json is a json text library that is used to create tweet object with this structure
# tweet = {
#   likes: "123 likes",
#   answers: "123 svar",
#   retweets: "123 retweets",
# }
#
# very simple and readable structure
#
# the request library is what makes us able to get the content of a webpage
# and is only used once in the very first line
#
# bs4 stands for BeautifulSoup4
# thats a library to look through the website text we just got with the request library


# TO the code!
# you should be able to run the whole thing but for understanding
# I would recommend making a new file
# copy from the top until a print()
# remove the "#" in front of the print() line
# run the code to see what is printed out
# then you can sort of get an idea of what every line does
# then you can copy the next bit until the next print and so forth ;)


# first we get the website text we want to get some data from
url = "https://twitter.com/elonmusk?lang=da"
page = requests.get(url)
print("Twitterpage: ", url)

# then we make a soup from the website text
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup)

# then we put in at spoon to try and nitpick in the soup only the elemnets which are a "span" element
# and also we are looking for elements with the class "ProfileTweet-actionCount"
# this info can be found by looking at the website code
# That is a small other guide that I'll skip for now
counts = soup.find_all("span", {"class": "ProfileTweet-actionCount"})
# print(counts)

# now we have all the elements from the website which contain counters
# some of there elements are empty though ... and we done want those
# so lets remove those empty ones

counts_clean = []
for count_element in counts: # for every count_element in the list counts do the following
    text = count_element.get_text().strip() # get the text from the element and remove white space at front and back
    if text: # if not empty text
        counts_clean.append(text) # add the text to the counts_clean list
        # print(text)

# print(len(counts_clean))
# print(counts_clean)

# now we have all the info now lets put it into tweet objects

tweets = []
tweet = {}
for i in range(0, len(counts_clean)):
    text = counts_clean[i]
    # print(text)

    if i % 3 == 0: # if the index in the list divided by 3 has a rest of 0
        tweet['answers'] = text # put the text in the object tweet at ['answers']
    if i % 3 == 1:
        tweet['retweets'] = text
    if i % 3 == 2:
        tweet['likes'] = text
        tweets.append(tweet)


# print(tweets)
print("Number of tweets on page: ", len(tweets))

# now we have all the tweets organized and seems like there are 20 on the first page
# lets do something with it
# lets count the total number of likes from these 20 tweets

total_likes = 0
for t in tweets:
    like_number = int(re.sub("\D", "", t['likes'])) # removes anything not a digit from string and convert it to integer type
    total_likes = total_likes + like_number

print("Total number of likes: ", total_likes)


# very nice