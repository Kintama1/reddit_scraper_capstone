# How to use the script:
- pip install praw in your terminal (the python wrapper for the reddit scraper)-> if this is confusing or not working, you can look up how to install these via the terminals or you can reach out to me: ykhayati@bowdoin.edu
## Creating a reddit client
- You have to log in to this website and make a client (something that reddit will give permission to scrape their website from) https://www.reddit.com/prefs/apps
- Follow the instructions: choose the local host to be: http://localhost:8000  (default for most computers )for the redirect uri (which is your machine by default) if you just want to scrape and store what you scrape on your local machine
## Filling the details of reddit = praw.Reddit
- Once you have a client for your application copy the following information:
    - the client id which will be under the title of your client (the sequence of random characters)
    - the client secret which is titled secret
    - user agent can be anything as long as u write a string that helps you identify your script

### Once you fill the details:
- You can run the code and it will write the reddit posts for you