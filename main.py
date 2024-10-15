import praw
import os

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

#recusive function to include all comments recursively
def write_comment(comment, file, level = 0):
    """Writes the comment and all its replies to the 
    represents the nested level of the comment by the level of indentation

    Args:
        comment (reddit.comment): The comment to retrieved from the reddit API
        file (.txt): The file the comment will be written to
        level (int, optional): level of nestedness for the replies: Defaults to 0.
    """
    indent = '  ' * level # to represent level of nesting of the comment
    file.write(f"{indent} Comment by {comment.author}: {comment.body} \n")
    for reply in comment.replies:
        write_comment(reply, file, level + 1)
    
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
                f.write(f"Title: {submission.title} \n ")
                f.write(f"URL: {submission.url} \n")
                f.write(f"OP entry: \n {submission.selftext} \n")
                
                #getting comments
                submission.comments.replace_more(limit = None)
                top_comments = submission.comments[:COMMENTS_PER_QUERY]
                f.write("Top 3 comments and their replies: \n \n")
                for comment in top_comments:
                    write_comment(comment, f)
    print("Finished query")



if __name__ == "__main__":
   scraper(SUBREDDIT,QUERIES,DISC_DIR)