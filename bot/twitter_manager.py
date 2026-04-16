"""
$MONDAY Twitter Manager
Handles posting, scheduling, profile updates for @MondayOnSol
"""
import os, tweepy
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

def get_client():
    return tweepy.Client(
        consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
        consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
        access_token=os.environ["TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
    )

def get_api():
    """v1.1 API — needed for profile picture + banner updates"""
    auth = tweepy.OAuth1UserHandler(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_SECRET"],
    )
    return tweepy.API(auth)

def tweet(text: str) -> str:
    r = get_client().create_tweet(text=text)
    tweet_id = r.data["id"]
    print(f"✅ Tweeted: https://x.com/MondayOnSol/status/{tweet_id}")
    return tweet_id

def update_bio(bio: str):
    get_api().update_profile(description=bio)
    print(f"✅ Bio updated: {bio}")

def update_profile_pic(image_path: str):
    get_api().update_profile_image(filename=image_path)
    print(f"✅ Profile pic updated: {image_path}")

def update_banner(image_path: str):
    get_api().update_profile_banner(filename=image_path)
    print(f"✅ Banner updated: {image_path}")

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"

    if cmd == "status":
        me = get_client().get_me(user_fields=["description", "public_metrics"])
        d = me.data
        print(f"@{d.username}")
        print(f"Bio: {d.description}")
        print(f"Followers: {d.public_metrics['followers_count']}")

    elif cmd == "bio":
        update_bio(sys.argv[2])

    elif cmd == "pic":
        update_profile_pic(sys.argv[2])

    elif cmd == "banner":
        update_banner(sys.argv[2])

    elif cmd == "tweet":
        tweet(sys.argv[2])
