import os
import sys
import time
from easygui import multpasswordbox
from instabot import Bot, utils


def app_settings():
    try:
        with open(setting_file, 'r'):
            pass
    except BaseException:
        with open(setting_file, 'w'):
            pass
        print("""
        Welcome to Asibot - Instagram Genius!
        First, let's setup parameters.
        """)
        setting_input()
        time.sleep(1)
        os.system('cls')


def setting_input():
    inputs = [("How many follows do you want to do in a day? ", 350),
              ("How about unfollow? ", 350),
              (("Maximal followers of account you want to follow?\n"
                "Asibot will skip users that have greater followers than this value "), 2000),
              (("Minimum followers a account should have before we follow?\n"
                "Asibot will skip users that have lesser followers than this value "), 10),
              (("Maximum following of account you want to follow?\n"
                "Asibot will skip users that have a greater following than this value "), 7500),
              (("Minimum following of account you want to follow?\n"
                "Asibot will skip users that have lesser following from this value "), 10),
              (("Minimal media the account you will follow have.\n"
                "Asibot will skip users that have lesser media from this value "), 3)]

    with open(setting_file, "w") as f:
        while True:
            for msg, n in inputs:
                msg += " (Press enter if you want to use default number: {})".format(n)
                print(msg)
                entered = sys.stdin.readline().strip() or str(n)
                f.write(str(entered) + "\n")
            break
        print("Done with all settings!")


def add_whitelist():
    f = utils.file(whitelist_file)
    following = bot.get_user_following(username)
    f.save_list(following)


def menu():
    print("""
    1. Follow
    2. Unfollow
    3. Setting parameters
    4. Add my following to Whitelist
    """)
    ans = input("What do you like to do?\n").strip()
    if ans == "1":
        menu_follow()
    elif ans == "2":
        menu_unfollow()
    elif ans == "3":
        setting_input()
    elif ans == "4":
        add_whitelist()
    else:
        print("\n Not a valida choice. Try again.")


def menu_follow():
    print("""
    1. Follow from hashtag
    2. Follow a user followers
    3. Main menu
    """)
    ans = input("How do you want to follow?\n").strip()
    if ans == "1":
        print("""
    1.Manually insert hashtag
    2.Use hashtag database (from file hashtagdb.txt)
        """)
        if "1" in sys.stdin.readline():
            hashtags = input("Insert hashtags separated by spaces \nExample: food restaurant milano\nwhat hashtags?\n").strip().split(' ')
        else:
            hashtags = bot.read_list_from_file(hashtag_file)
        for hashtag in hashtags:
            print("Begin following: " + hashtag)
            users = bot.get_hashtag_users(hashtag)
            bot.follow_users(users)
        menu_follow()
    elif ans == "2":
        user_id = input("who?\n").strip()
        bot.follow_followers(user_id)
        menu_follow()
    elif ans == "3":
        menu()
    else:
        print("This number is not in the list.")
        menu_follow()


def menu_unfollow():
    print("""
    1. Unfollow non followers
    2. Unfollow everyone exept user in Whitelist
    3. Main menu
    """)
    ans = input("What do you like to do?\n").strip()
    if ans == "1":
        bot.unfollow_non_followers()
        menu_unfollow()
    elif ans == "2":
        bot.unfollow_everyone()
        menu_unfollow()
    elif ans == "3":
        menu()
    else:
        print("This number is not in the list.")
        menu_unfollow()


setting_file = "setting.txt"
whitelist_file = "whitelist.txt"
hashtag_file = "hashtagsdb.txt"


# Let's Go!
app_settings()
if os.stat(setting_file).st_size == 0:
    print("Looks like setting are broken")
    print("Let's make new one")
    setting_input()

lines = open(setting_file).readlines()
setting_max_follows = int(lines[0].strip())
setting_max_unfollows = int(lines[1].strip())
setting__max_followers = int(lines[2].strip())
setting_min_followers = int(lines[3].strip())
setting__max_following = int(lines[4].strip())
setting_min_following = int(lines[5].strip())
setting_min_media = int(lines[6].strip())

bot = Bot(
    max_follows_per_day=setting_max_follows,
    max_unfollows_per_day=setting_max_unfollows,
    max_followers_to_follow=setting__max_followers,
    min_followers_to_follow=setting_min_followers,
    max_following_to_follow=setting__max_following,
    min_following_to_follow=setting_min_following,
    min_media_count_to_follow=setting_min_media,
    whitelist_file=whitelist_file)
time.sleep(1)

print("Let's add your Instagram account.")
print("Don't worry, only you have access to your account.")

msg = "Login with your Instagram account"
title = "Login"
loginParameters = ["Username", "Password"]
loginValues = multpasswordbox(msg, title, loginParameters)

username = loginValues[0]
password = loginValues[1]
while 0:
  loginValues = multpasswordbox(title, loginParameters, loginValues)

bot.login(username=username, password=password)
time.sleep(1)
menu()
