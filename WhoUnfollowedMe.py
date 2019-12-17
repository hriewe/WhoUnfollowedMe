# Hayden Riewe
# Who Unfollowed Me?
# github.com/hriewe
# haydenriewe.com

from InstagramAPI import InstagramAPI
from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

# https://github.com/LevPasha/Instagram-API-python/blob/master/examples/user_followers.py
def getTotalFollowers(api, user_id):
    """
    Returns the list of followers of the user.
    It should be equivalent of calling api.getTotalFollowers from InstagramAPI
    """

    followers = []
    next_max_id = True
    while next_max_id:
        # first iteration hack
        if next_max_id is True:
            next_max_id = ''

        _ = api.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return followers

@app.route('/')
def WhoUnfollowed():
    api = InstagramAPI("username", "password")
    api.login()

    # user_id = '1461295173'.
    user_id = api.username_id

    # List of all followers.
    followers = getTotalFollowers(api, user_id)

    # Declare sets for comparison.
    current = set()
    previous = set()

    # Add all folowers from most recent run to current set.
    for follower in followers:
      current.add(follower['username'])
    
    # Add all folowers from previous run to previous set.
    try:
      with open('db/followers.txt', 'r') as f:
        next(f)
        for follower in f:
          previous.add(follower.strip('\n'))
    except IOError:
      print("Previous followers could not be loaded. If this is your first run, this is normal")

    # Overwrite the previous followers with the most recent ones for next run.
    with open('db/followers.txt', 'w') as f:
      f.write('Number of followers: ' + str(len(followers)) + '\n')
      for follower in followers:
        f.write(follower['username'] + '\n')

    # Determine difference of sets. This will reveal who has unfollowed.
    unfollowed = previous.difference(current)
    if len(unfollowed) == 0:
      return render_template('noresult.html')
    else:
      return render_template('result.html', result = unfollowed)
    
    return render_template('result.html', result = unfollowed)

if __name__ == "__main__":
  app.run()