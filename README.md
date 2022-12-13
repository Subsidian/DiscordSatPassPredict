# DiscordSatPassPredict
## Welcome!
This is a discord bot that can take multiple TLE's as input from a text file
and predict passes based on longitude and latitude, then sorts the output in ascending order. 
This code was developed with help from OpenAI's chatbot! Really helpful bot that diagnosed a few faults as I'm fairly new to Python

## Pre-requisites 
The first step is to create a discord application, and then a discord bot. (https://discord.com/developers/applications)
The variables in this such as name, PFP etc can be whatever you would like.
Please enable ALL Privileged Gateway Intents (there are 3 at time of writing) found under "Bot" tab.

I would reccomend installing GIT as this is the easiest way to install libraries. Otherwise these can be installed in any other means that suit.
If you don't have GIT installed already, look here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

As for required libraries, these are here with the correct git command to paste into your console.
| Library | GIT |
| ------ | ------ |
| discord | git install discord |
| ephem | git install ephem |
| datetime | git install datetime |
| pytz | git install pytz |
| math | git install math |
| asyncio | git install asyncio |

## Getting-Started
1. Ensure all libraries are installed.
2. Using a text editor (please god not notepad) open bot.py. At the very top, you will see the following code to update. Nothing else needs to be changed, and the included comments should be pretty straight-forward:
```sh
#=================================================================================
#Update the variables in this box

# Replace TOKEN with your bot's API token
TOKEN = '#####################'

# Replace LATITUDE and LONGITUDE with the coordinates where you want to predict the satellite passes
# https://www.latlong.net/ <- NOT MY WEBSITE, this is just what I used
LATITUDE = '##########'
LONGITUDE = '#########'

#set the minimum elevation to ensure you don't recieve the next pass sent in discord isnt a crappy 1 degree pass
Minimum_Elevation = 20

# Set the time zone for the observer
# A list of timezones can be found here: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
timezone = pytz.timezone('Pacific/Auckland')

#for 1H automation, change ChannelName to the name of your channel. DO NOT ADD QUOTATIONS, THIS MUST BE NUMERIC NOT A STRING
channel = bot.get_channel(##############)
#=================================================================================
```
4. ENSURE all these files are in one folder.
3. There is an included batch file to run this bot, and a succesfull connection to your bot will look like this:
```sh
discord.client logging in using static token
discord.gateway Shard ID None has connected to Gateway (Session ID: #######################)
```
If you share your token anywhere on the internet, you will get an error like this below
```sh
discord.gateway Shard ID None session has been invalidated.
```
If this happens, please learn your lesson of not sharing this token anywhere, and generate a new one via https://discord.com/developers/applications

# Updating TLE's
The included satellites.txt file includes NOAA-15, NOAA 18, NOAA 19 and METEOR M-2 TLE's, however you are welcome to swap out any other TLE.
I believe ephem checks the TLE to ensure it is the most up to date, and if it is not - you will get a checksum error. Please ensure the most up-to-date TLE's are used.
You can find some here: https://celestrak.org/NORAD/elements/
Please ensure the satellites.txt is NOT renamed, and if editting TLE's, ensure they follow the correct format (Example provided below):
```sh
NOAA 15 [B]             
1 25338U 98030A   22341.84963576  .00000200  00000-0  10169-3 0  9993
2 25338  98.6276   8.9831 0010958 147.5172 212.6684 14.26204853277730
NOAA 18 [B]             
1 28654U 05018A   22341.79076297  .00000268  00000-0  16839-3 0  9994
2 28654  98.9327  51.9429 0014088 197.9373 162.1303 14.12818168904453
NOAA 19 [+]             
1 33591U 09005A   22341.81194952  .00000227  00000-0  14758-3 0  9995
2 33591  99.1281  19.4291 0014694  63.2908 296.9766 14.12647752712667
METEOR M2
1 40069U 14037A   22341.71436734  .00000011  00000-0  24095-4 0  9997
2 40069  98.4269 351.5740 0005789 167.9092 192.2218 14.20728651436461
```

# Issues:
Feel free to open an issue for anything (even just support) and i'll do my best to help

# To-Do
1 Automatically update the sattelites TLE's
2 Look into having a database of all TLE's, kept up to date, and allowing for !passes {Sat name} to check next passes for specific satelites
3 If I was to host this bot for all and have just an invite link - I would most probably require a database to store everyones Lat-Long and other variables in, in which im not very confortable doing for security purposes (you should be happy!)
