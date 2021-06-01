# Importing modules
from instapy import InstaPy
from instapy import smart_run

# Variable
creds = []

# Reading credentials from creds.txt
with open("creds.txt", 'r') as file:
    creds = file.read().split(" ")

# Creating main function
def main():

    # Starting InstaPy session 
    # You can add argument headless=True
    # To run the script without browser
    session = InstaPy(username=creds[0], password = creds[1])
    
    # Logging into instagram
    session.login()

    # Starting smart run loop
    while smart_run(session):

        # Liking 3 posts by tags 'pythonprogramming' and 'pythontutorial'
        session.like_by_tags(['pythonprogramming', 'pythontutorial'], amount=3)
        
        # Use set_do_like to set like precentage
        session.set_do_like(True, percentage=50)

        # Use sd to specify which tags to not like
        session.set_dont_like(["nsfw"])

        # Use set_do_comment to set comment percentage
        session.set_do_comment(True, percentage=30)

        # Set possible comments to choose from
        session.set_comments(["Nice post", 'Great Work bro'])
        
        # Set supervisor to evade from instagram detecting bot
        session.set_quota_supervisor( 
            enabled=True, # To enable supervisor
            peak_comments_daily=5, # Daily comment limit
            peak_comments_hourly=5, # Hourly comment limit
            peak_likes_daily = 5, # Daily likes limit
            peak_likes_hourly = 5 # Hourly likes limit
        )
    
    # Ending the session
    session.end()

if __name__ == '__main__':
    # Calling the main function
    main()