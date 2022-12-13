import discord
from discord.ext import commands
import ephem
import datetime
import pytz
import math
import asyncio

#=================================================================================
#Updat the variables in this box
# Replace TOKEN with your bot's API token
TOKEN = 'MTA1MTcyNjQxMjE2OTYwOTMwNg.GnKf2J.TLCY97fxBu5vWWrGWsEMtax09f5HnzLUEBpRj8'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

# Create an empty list to store outputs
outputs = []

# Replace LATITUDE and LONGITUDE with the coordinates where you want to predict the satellite passes
LATITUDE = '-37.791778'
LONGITUDE = '175.248126'

#set the minimum elevation to ensure you don't recieve the next pass as a pretty trash
Minimum_Elevation = 20

# Set the time zone for the observer
timezone = pytz.timezone('Pacific/Auckland')

#for 1H automation, change ChannelName to the name of your channel
channel = bot.get_channel(1048688504537882654)

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

            # if current prediction is less than 20 degrees, search again at that passes time, to find the next pass.
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
        await channel.message.send(f"Satellite: {passes['satellite']}\nPass Time: {passes['pass_time']}")    
bot.run(TOKEN)

async def run_every_hour():
  while True:
    # Wait for one hour
    await asyncio.sleep(60 * 60)

    # Run the bot
    await bot.run()