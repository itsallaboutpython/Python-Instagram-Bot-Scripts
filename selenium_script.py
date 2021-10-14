# Importing modules
import os, time, random
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Global variables
credentials = []
cred_filename = "creds.txt"
driver = None
actions = None
ec_wait = None
URL = "https://www.instagram.com"
IMPLICIT_WAIT_TIME = 10
WAIT_TIME = 5
USERNAME_TEXTBOX = "//input[@name = 'username']"
PASSWORD_TEXTBOX = "//input[@name = 'password']"
NOT_NOW_BUTTON = "//button[@type='button']"
LOGIN_BUTTON = "//button[@type='submit']"
SEARCH_BY_TAG = URL + "/explore/tags/"
POSTS_SEARCH = "//a[@tabindex='0']"
LIKE_BUTTON = "//span[@class = 'fr66n']/button"
CROSS_BUTTON = "//div[contains(@class, ' Igw0E     IwRSH      eGOV_         _4EzTm  ')]/button"
COMMENT_BOX = "//textarea[contains(@aria-label, 'Add a comment')]"
COMMENT_BUTTON = "//span[@class = '_15y0l']/button"
FOLLOW_LINK = "//a[@class = 'sqdOP yWX7d     _8A5w5   ZIAjV ']"
FOLLOW_BUTTON = "//button[contains(text(),  'Follow')]"

# Function to check internet connection and 
# Login to instagram with user credentials
def login():

    # check for internet connection
    print()
    print("[INFO] Checking for Internet Connectivity")
    if requests.get("https://www.google.com").status_code != 200:
        print("[ERROR] No internet connection detected...please try again")
        exit(0) 

    # Opening 'www.instagram.com' on browser
    print("[INFO] Opening {0}".format(URL))
    driver.get(URL)
    driver.implicitly_wait(IMPLICIT_WAIT_TIME)
    page_title = ec_wait.until(EC.title_contains("Instagram"))

    try:
        print("[INFO] Logging into instagram")

        # Entering username
        driver.find_element_by_xpath(USERNAME_TEXTBOX).send_keys(credentials[0])
        time.sleep(WAIT_TIME)

        # Entering password
        driver.find_element_by_xpath(PASSWORD_TEXTBOX).send_keys(credentials[1])
        time.sleep(WAIT_TIME)

        # Clicking on login button
        driver.find_element_by_xpath(LOGIN_BUTTON).click()
        time.sleep(WAIT_TIME)

        # Wait for not now button to appear
        waiter = ec_wait.until(EC.presence_of_element_located((By.XPATH, NOT_NOW_BUTTON)))

    except Exception as ex:
        print(ex)

# Function to like, comment and follow posts based
# On certain parameters like
# tagname: name of the tag
# amount: amount of posts to check for that tag
# comment_list: lsit of comments to choose from
# followprecentage: chances to follow a user in percentage
def like_post_by_tag(tagname, amount, comment_list = [], followpercentage=0):
    try:
        # Check follow percentage value
        # as it should be between 0 to 100
        try:
            if 0 <= followpercentage <= 100:
                pass
            else:
                print("[ERROR] Invalid value for 'followpercentage' = '{0}'".format(followpercentage))
                exit(0)
        except:
            pass
        
        # Check amount value
        # as it should be between 0 to 10
        try:
            if 0 <= followpercentage <= 10:
                pass
            else:
                print("[ERROR] Invalid value for 'amount' = '{0}'".format(followpercentage))
                exit(0)
        except:
            pass

        # Start function
        print()
        print("[INFO] Finding post by the tag {0}".format(tagname))
        tag_url = SEARCH_BY_TAG + tagname.replace(' ', '')
        
        # Get to URL
        driver.get(tag_url)
        page_title = ec_wait.until(EC.title_contains("Instagram"))
        time.sleep(WAIT_TIME)

        # Search posts
        while len(driver.find_elements_by_xpath(POSTS_SEARCH)) < 10:
            continue
        posts_list = list(driver.find_elements_by_xpath(POSTS_SEARCH))[:10]
        choices = random.sample(posts_list, amount)
        number = len(driver.find_elements_by_xpath(LIKE_BUTTON))

        # Iterate through posts
        for choice in choices:

            # Click and open post
            actions.move_to_element(choice).click()
            choice.click()
            time.sleep(WAIT_TIME)


            print()
            print("[INFO] Count Number: {0}".format(choices.index(choice) + 1))
            print("[INFO] Found post {0}".format(driver.current_url))
            try:
                # Like the post
                elmnt = ec_wait.until(EC.presence_of_element_located((By.XPATH, LIKE_BUTTON)))
                like_button = driver.find_element_by_xpath(LIKE_BUTTON)
                like_button.click()
                print("[INFO] Liked post {0}".format(driver.current_url))
                time.sleep(WAIT_TIME)

                # If you have to add comment
                if comment_list != ['']:
                    # Choose random comment
                    comment_choice = random.choice(comment_list)

                    # Click on comment button
                    driver.find_element_by_xpath(COMMENT_BUTTON).click()
                    time.sleep(WAIT_TIME)

                    # Enter comment in comment box
                    driver.find_element_by_xpath(COMMENT_BOX).send_keys(comment_choice + Keys.ENTER)
                    print("[INFO] Commented '{0}' on {1}".format(comment_choice, driver.current_url))
                    time.sleep(WAIT_TIME)
                    
                    
                    # Calculate whether to follow or not
                    if followpercentage != 0:
                        follow_sample = [True, False]
                        weight = [followpercentage/10, (10 - followpercentage/10)]
                        follow_choice = random.choices(follow_sample, k=1, weights=weight)

                        # Code to follow user
                        try:
                            # If yes, follow the user
                            if follow_choice:
                                link = driver.find_element_by_xpath(FOLLOW_LINK).get_attribute("href")
                                time.sleep(WAIT_TIME)
                                try:
                                    # Open new tab and go to user profile page
                                    driver.execute_script("window.open('', '_blank');")
                                    driver.switch_to.window(driver.window_handles[1])
                                    driver.get(link)
                                    page_title = ec_wait.until(EC.title_contains("Instagram"))
                                    time.sleep(WAIT_TIME)

                                    # Click on follow button
                                    follow = ec_wait.until(EC.presence_of_element_located((By.XPATH, FOLLOW_BUTTON)))
                                    driver.find_element_by_xpath(FOLLOW_BUTTON).click()

                                    # Follow the user
                                    print("[INFO] Following {0}".format(driver.current_url))
                                    time.sleep(WAIT_TIME)

                                    # Close the tab and switch back to the first tab
                                    driver.close()
                                    driver.switch_to.window(driver.window_handles[0])
                                    time.sleep(WAIT_TIME)

                                except Exception as ex:
                                    try:
                                        print("Exception:", traceback.print_exc())
                                        # Don't follow the user if already following the user
                                        print("[INFO] Already following {0}".format(driver.current_url))
                                        driver.close()
                                        driver.switch_to(driver.window_handles[0])
                                        time.sleep(WAIT_TIME)
                                    except Exception as ex:
                                        print("Exception:", traceback.print_exc())

                        except Exception as ex:
                            # Exception printing
                            print(ex)
                            traceback.print_exc()

                    # Click on close button
                    elment = ec_wait.until(EC.presence_of_element_located((By.XPATH, CROSS_BUTTON)))
                    driver.find_element_by_xpath(CROSS_BUTTON).click()
                    time.sleep(WAIT_TIME)

                else:
                    # Click on close button
                    elment = ec_wait.until(EC.presence_of_element_located((By.XPATH, CROSS_BUTTON)))
                    driver.find_element_by_xpath(CROSS_BUTTON).click()
                    time.sleep(WAIT_TIME)

            except Exception as ex:
                # Exception printing
                print(ex)
                traceback.print_exc()

                # Click on close button
                print("[INFO] Already liked post {0}".format(driver.current_url))
                elment = ec_wait.until(EC.presence_of_element_located((By.XPATH, CROSS_BUTTON)))
                driver.find_element_by_xpath(CROSS_BUTTON).click()
                time.sleep(WAIT_TIME)

    except Exception as ex:
        # Exception printing
        print(ex)
        traceback.print_exc()

# Function to call like_post_by_tag function with a list of tags
def like_post_by_multiple_tags(tag_list, amount, comment_list = [], followpercentage=0):
    
    # Iterate through tags and call the function
    print("[INFO] Finding posts by the tags {0}".format(tag_list))
    for tag in tag_list:
        like_post_by_tag(tag, amount, comment_list, followpercentage)

# Main Function
def main():

    # Global variables
    global driver, ec_wait, actions, credentials
    try:

        # Check whether 'creds.txt' exists in the project folder or not
        if not os.path.exists(cred_filename):
            print("[ERROR] Invalid path...please try again")
            exit(0)

        # Open 'creds.txt' and read credentials
        with open(cred_filename, "r") as file:
            credentials = file.read().split(" ")

        tags, comment_list = [], []

        while 1:
            # Take user input
            tags = input("Enter tag/tags you want to search (required) (separated by commas) (like 'python python3' etc): ").split(",")
            amount = int(input("Enter amount of posts you want to check per tag (required) (not more than 10): "))
            followpercentage = int(input("Enter follow precentage (type '0' for no follows): "))
            comment_list = input("Enter list of comments you want to enter (separated by commans) (type nothing for no comments): ").split(",")

            # Confirm user input from user
            print('\n[INFO] Here is your bot configurations')
            print("[INFO] Tags: {0}".format(tags))
            print("[INFO] Amount:", amount)
            print("[INFO] Comments List:", comment_list)
            print("[INFO] Follow precentage:", followpercentage)
            agree = input("Do you agree with the configurations (y/n): ")

            # If user confirms, break the loop
            # Or else, ask for input again
            if agree.lower() == 'y':
                break
            else:
                print("")
                continue

        # Initiate, driver, actions and waiter
        driver = webdriver.Chrome("chromedriver.exe")
        actions = ActionChains(driver)
        ec_wait = WebDriverWait(driver, 20)

        # Call login() function
        login()

        # Call like_post_by_multiple_tags() function
        like_post_by_multiple_tags(tags, amount, comment_list, followpercentage)
        
        # Close the driver
        driver.close()

    except KeyboardInterrupt:
        print("[INFO] User stopped the program...exiting")
        exit(0)
    except TypeError:
        print("[ERROR] Some input was entered wrong...please try again")
        exit(0)
    except Exception:
        print("[ERROR] Something went wrong...please try again\n")
        traceback.print_exc()
        exit(0)

# Main function to be called when program runs
if __name__ == '__main__':
    main()
