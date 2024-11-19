from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


url = "https://x.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJteCI6IjIifQ%3D%3D%22%7D"
driver = webdriver.Firefox()
driver.get(url)


def loginAsUser(username, password):
    print(f"Logging in as {username}...")
    
    sleep(5)
    try:
        # Find the username and password fields and fill them in
        usernameField= driver.find_element(By.CSS_SELECTOR, 'input[autocapitalize="sentences"][autocomplete="username"][autocorrect="on"][name="text"][spellcheck="true"][type="text"]')
        usernameField.send_keys(username)
        # driver.find_element_by_name("text").send_keys(username)
        # Click the Next button
        nextButton= driver.find_element(By.CSS_SELECTOR, 'button[role="button"].css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l')
        nextButton.click()

        # driver.find_element_by_name("password").send_keys(password)
        sleep(1)
        password_element = driver.find_element(By.XPATH, '//input[@autocapitalize="sentences" and @autocomplete="current-password" and @autocorrect="on" and @name="password" and @spellcheck="true" and @type="password"]')
        password_element.send_keys(password)
        login_button = driver.find_element(By.XPATH, '//button[@role="button" and @data-testid="LoginForm_Login_Button" and @type="button" and contains(@class, "css-175oi2r") and contains(@class, "r-sdzlij") and contains(@class, "r-1phboty") and contains(@class, "r-rs99b7") and contains(@class, "r-lrvibr") and contains(@class, "r-19yznuf") and contains(@class, "r-64el8z") and contains(@class, "r-1fkl15p") and contains(@class, "r-1loqt21") and contains(@class, "r-o7ynqc") and contains(@class, "r-6416eg") and contains(@class, "r-1ny4l3l")]')
        login_button.click()
        sleep(3)
        print("Login successful!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    


def get_latest_tweets(username, tweet_count):
    print(f"Getting {tweet_count} latest tweets from {username}...")
    url = f"https://x.com/{username}"
    driver.get(url)
    sleep(3)
    collected_tweets = []
    
    try:
        while len(collected_tweets) < tweet_count:
            response = driver.page_source
            # Parse the HTML response
            soup = BeautifulSoup(response, features="html.parser")
            
            # Find all tweet texts
            tweetContainer = soup.find_all("div", {"data-testid": "cellInnerDiv"})
            
            for tweet in tweetContainer[:tweet_count]:
                tweet_text_element = tweet.find("div", {"data-testid": "tweetText"})
                specific_image = tweet.find("img", {"alt": "🚨", "src": "https://abs-0.twimg.com/emoji/v2/svg/1f6a8.svg"})
                tweet_text = tweet_text_element.get_text()
                
                time_tag = tweet.find("time")
                tweet_time = time_tag['datetime'] if time_tag else "No time tag found"
                
                
                collected_tweets.append({"text": tweet_text, "time": tweet_time, "siren": True if specific_image else False})
                # Scroll down to load more tweets
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                sleep(1)
            
        
        # for i, tweet in enumerate(collected_tweets[:tweet_count]):
        #     print(f"Tweet {i + 1}: {tweet['text']}")
        #     print(f"Time: {tweet['time']}")
        #     print(f"Contains alert: {tweet['siren']}\n")
        
        return collected_tweets
        # print(f"Found {len(collected_tweets)} tweets\n")
        # for i, tweet in enumerate(collected_tweets[:tweet_count]):
        #     tweet_text = tweet.text
            
        #     # Check if the tweet contains "#alert"
        #     contains_alert = "#alert" in tweet_text
            
        #     # Check for the specific image tag within the tweet
        #     specific_image = tweet.find("img", {"alt": "🚨", "src": "https://abs-0.twimg.com/emoji/v2/svg/1f6a8.svg"})
        #     contains_specific_image = specific_image is not None
            
        #     if contains_alert or contains_specific_image:
        #         print(f"Tweet {i + 1}: {tweet_text}\n")
    
    except Exception as e:
        print(f"An error occurred: {e}")



def process_buy_tweets(tweets):
    print("Processing buy tweets...")
    sell_keywords = ["manage risk", "reduced", "loss", "losses", "took loss"]
    for tweet in tweets:
        tweet_text = tweet["text"]
        tweet_time = tweet["time"]
        siren=tweet["siren"]
        
        # Check if the tweet does not contain a word in the sell_keywords list
        if not any(keyword in tweet_text.lower() for keyword in sell_keywords) and siren:
            print(f"Buy tweet found at {tweet_time}: {tweet_text}")
            
    print("\n")
# Example usage
logged_in = loginAsUser("rahulanwar", "Nevermind420")


# dict(tweetText, timeStamp);

if logged_in:
    tweet_dict=get_latest_tweets("rachels_premium", 20)
    process_buy_tweets(tweet_dict)
    driver.quit()
