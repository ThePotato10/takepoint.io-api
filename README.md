# Takepoint.io JSON API
A JSON api for stats from the browser-based io game takepoint.io

Takepoint.io is a browser-based top-down shooter game focused on capturing points. Wonderfully, the game collects players's stats on the subdomain (stats.takepoint.io)[https://stats.takepoint.io]. Less wonderfully, there's on way to programmatically read these stats

That's where this comes in

I hacked together a webscraper that reads the stats and creates a JSON object out of them

## Installation
1. run the command `git clone https://github.com/ThePotato10/takepoint.io-api.git`
2. `cd takepoint.io-api`
3. `pip install -r requirements.txt`
4. `python3 server.py`

This starts a server on `localhost:5500` with an ad hoc web interface. Raw JSON data is available at `http://localhost:5500/stats/<user>`
