import praw
import os
import textwrap

#HYPER_PARAMETERS
POSTS_NUMBERS_PER_QUERY = 17
COMMENTS_PER_QUERY = 3

#DETAILS FOR r/getdisciplined
SUBREDDIT = '' #fill it with the title of your subreddit (drop the r/ just the title for example. productivity and not r/productivity)
# a list of search queries you want to use 
# (for example if you want all posts from R/slash addiction about social media, your que)
QUERIES = ['']
# Choose a name for the directory that your files will be saved to 
DISC_DIR = ''

#EXAMPLE 
# SUBREDDIT_PROD = 'productivity'
# PROD_QUERIES = ['social media addiction', 'delete social media', 'quit social media', '"social media addiction" AND help']
# PROD_DIR = "producitvity_subreddit"


reddit = praw.Reddit(
    client_id = "",#FILL IT WITH YOUR CLIENT ID
    client_secret ="", #FILL IT WITH YOUR CLIENT SECRET
    user_agent ="" ,#FILL IT WITH YOUR USER_agent
    # Password and username are not required for a read oly reddit instance
    # username
    #password  
)
def wrap_text(text, width=80, initial_indent='', subsequent_indent=''):
    """Has the text wrapping for better readability

    Args:
        text (string): text file to wrap
        width (int, optional): Length of line in characters. Defaults to 80.
        initial_indent (str, optional): initial indent for text. Defaults to ''.
        subsequent_indent (str, optional): subsequent indent for text (used for nested comments). Defaults to ''.

    Returns:
        _type_: _description_
    """
    wrapper = textwrap.TextWrapper(width=width, initial_indent=initial_indent, subsequent_indent=subsequent_indent)
    return wrapper.fill(text)

#recusive function to include all comments recursively
def write_comment(comment, f, width = 110,indent = "    "):
    """Writes the comment and all its replies to the 
    represents the nested level of the comment by the level of indentation

    Args:
        comment (reddit.comment): The comment to retrieved from the reddit API
        f (.txt): The file the comment will be written to
        width (int, optional): the length of line in characters
        indent(string, optional): the inital indent for nested comments
    """
    f.write(f"comment by {comment.author}: \n")
    f.write(f"{wrap_text(comment.body)} \n \n")
    for reply in comment.replies:
        f.write(f"{indent} Reply by {reply.author}: \n")
        f.write(wrap_text(reply.body, width= width,initial_indent = indent, subsequent_indent = indent) + "\n\n")
    
def scraper(subreddit_name, search_queries, base_dir):
    """Scrapes the subreddit chosen based on the search queries provided and writes the posts and the top 3 comments as a file 
    inside a directory that is inside the base_dir

    Args:
        subreddit_name (string): Name of subreddit to include
        search_queries (list): List of search queries
        base_dir (string): name of directory to write all searches to
    """
    subreddit = reddit.subreddit(subreddit_name)
    os.makedirs(base_dir,exist_ok= True)
    for query in search_queries:
        #SO This is making the path to the current directory we have here
        query_dir = os.path.join(base_dir,query.replace(" ", "_"))
        os.makedirs(query_dir,exist_ok= True)
        
        #statement to check
        print(f"Writing results for search query: '{query}' to ' {query_dir}'")
        for i, submission in enumerate(subreddit.search(query, limit = POSTS_NUMBERS_PER_QUERY)):
            filename = os.path.join(query_dir,f"post_{i+1}.txt")
            with open(filename, 'w', encoding='UTF-8') as f:
                f.write(f"Title: {submission.title} \n \n")
                f.write(f"URL: {submission.url} \n \n")
                f.write(f"OP entry: \n {wrap_text(submission.selftext)} \n\n")
                
                #getting comments
                submission.comments.replace_more(limit = None)
                top_comments = submission.comments[:COMMENTS_PER_QUERY]
                f.write("Top 3 comments and their replies: \n \n")
                for comment in top_comments:
                    write_comment(comment, f)
    print("Finished query")



if __name__ == "__main__":
   scraper(SUBREDDIT,QUERIES,DISC_DIR)


   

#recusive function to include all comments recursively

    

