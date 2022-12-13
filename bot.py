import discord
from discord.ext import commands
import ephem
import datetime
import pytz
import math
import asyncio
#Discord for bot, Ephem to calc, datetime for converting, pytz for timezone, math for radials-degrees conversion and asyncio for 1H chat timer.

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
    
#Discord requires intents for bots now, for simplicity this is set to all.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

# Create an empty list to store outputs to be sorted
outputs = []

# This function will be called whenever the bot receives the "!passes" command
@bot.command()
async def passes(ctx):
    # Open the file containing the TLEs
    with open('satellites.txt', 'r') as f:
        # Read the TLEs from the file
        tles = f.readlines()
        
    # Create a new observer at the specified latitude and longitude
    observer = ephem.Observer()
    observer.lat = LATITUDE
    observer.lon = LONGITUDE
    
# Set the minimum elevation of the satellite to 20 degrees
    observer.horizon = 0
    
    # Iterate through the TLEs
    for i in range(0, len(tles), 3):
        # Read the satellite name and TLE data from the file
        satellite_name = tles[i].strip()
        tle1 = tles[i + 1].strip().replace('1 ', '1 ') #without this replacement, I would occasionally get checksum errors. Unknown error but stupid fix.
        tle2 = tles[i + 2].strip().replace('2 ', '2 ')
        
        # Set the observer date to the current time
        observer.date = ephem.date(timezone.localize(datetime.datetime.now()))
        
        # Create a new satellite using the TLE
        satellite = ephem.readtle(satellite_name, tle1, tle2)
        
        # Compute the position of the satellite at the current time
        satellite.compute(observer)
        
        # Compute the next pass of the satellite over the observer's location
        next_pass = observer.next_pass(satellite)
        elevation_degrees = math.degrees(next_pass[3])
        
        while elevation_degrees <= Minimum_Elevation:
            if elevation_degrees > Minimum_Elevation:
                break

            # Update the value of next_pass and elevation_degrees
            observer.date = next_pass[2]
            next_pass = observer.next_pass(satellite)
            elevation_degrees = math.degrees(next_pass[3])
        
        # Convert the pass time from Julian date to a human-readable date and time
        pass_time = timezone.fromutc(timezone.localize(ephem.date(next_pass[0]).datetime())).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        #add passes to list to be sorted
        outputs.append({ "satellite": satellite_name, "pass_time": pass_time})
    # Sort the list by pass time in ascending order
    passes_sorted = sorted(outputs, key=lambda p: p["pass_time"])
    # Format the list "passes_sorted" to readable content before parsing to discord
    for passes in passes_sorted:
        await ctx.send(f"Satellite: {passes['satellite']}\nPass Time: {passes['pass_time']}")    
bot.run(TOKEN)

# This function runs every-hour
@bot.event
async def on_ready():
        # Open the file containing the TLEs
    with open('satellites.txt', 'r') as f:
        # Read the TLEs from the file
        tles = f.readlines()
        
    # Create a new observer at the specified latitude and longitude
    observer = ephem.Observer()
    observer.lat = LATITUDE
    observer.lon = LONGITUDE
    
# Set the minimum elevation of the satellite to 20 degrees
    observer.horizon = 0
    
    # Iterate through the TLEs
    for i in range(0, len(tles), 3):
        # Read the satellite name and TLE data from the file
        satellite_name = tles[i].strip()
        tle1 = tles[i + 1].strip().replace('1 ', '1 ')
        tle2 = tles[i + 2].strip().replace('2 ', '2 ')
        
        # Set the observer date to the current time
        observer.date = ephem.date(timezone.localize(datetime.datetime.now()))
        
        # Create a new satellite using the TLE
        satellite = ephem.readtle(satellite_name, tle1, tle2)
        
        # Compute the position of the satellite at the current time
        satellite.compute(observer)
        
        
        # Compute the next pass of the satellite over the observer's location
        next_pass = observer.next_pass(satellite)
        elevation_degrees = math.degrees(next_pass[3])
        
        #loop to only get passes greater than minimum elevation set (default 20)
        while elevation_degrees <= Minimum_Elevation:
            if elevation_degrees > Minimum_Elevation:
                break

            # if current prediction is less than minimum elevation, search again at that passes time, to find the next pass.
            observer.date = next_pass[2]
            next_pass = observer.next_pass(satellite)
            # Output is in radials, degrees majority of people are familiar with so this is converteed here
            elevation_degrees = math.degrees(next_pass[3])
        
        
        
        # Convert the pass time from Julian date to a human-readable date and time
        pass_time = timezone.fromutc(timezone.localize(ephem.date(next_pass[0]).datetime())).strftime('%Y-%m-%d %H:%M:%S %Z%z')

        #add passes to list to be sorted
        outputs.append({ "satellite": satellite_name, "pass_time": pass_time})
        
    # Sort the list by pass time in ascending order
    passes_sorted = sorted(outputs, key=lambda p: p["pass_time"])
    
    # Format the list "passes_sorted" to readable content before parsing to discord
    for passes in passes_sorted:
        await channel.message.send(f"Satellite: {passes['satellite']}\nPass Time: {passes['pass_time']}")    
bot.run(TOKEN)

async def run_every_hour():
  while True:
    # Wait for one hour
    await asyncio.sleep(60 * 60)

    # Run the bot
    await bot.run()