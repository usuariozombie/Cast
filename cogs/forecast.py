import nextcord, asyncio, json, requests
from weather import *
from nextcord.ext import commands
from datetime import datetime


class FORECAST(commands.Cog):

    """Weather Forecast."""

    def __init__(self, client):
        self.client = client

    COG_EMOJI = "🌦️"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\u001b[32m[{datetime.now().strftime('%H:%M:%S')} COG] » WEATHER enabled.\u001b[0m")
    
    @commands.command(help="🌡️ - It sends information about the selected location temperature.")
    async def weather(self ,ctx, *, location):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={"yourApiID"}&units=metric'
        try:
            data = parse_data(json.loads(requests.get(url).content)['main'])
            data2 = parse_data(json.loads(requests.get(url).content)['weather'])
            skyCondition = data2[0]['main']
            skyDesc = data2[0]['description']
            tempEmbed = weather_message(data, location)
            if skyCondition == "Clouds":
                tempEmbed.set_image("https://thumbs.gfycat.com/BountifulAcidicChihuahua-max-1mb.gif")
            elif skyCondition == "Tornado":
                tempEmbed.set_image("https://acegif.com/wp-content/uploads/2022/fzk5d/20-smooth-storm.gif")
            elif skyCondition == "Thunderstorm":
                tempEmbed.set_image("https://i.pinimg.com/originals/dd/f1/48/ddf1482dcd4dc5fc267cfa0a6c0cd720.gif")
            elif skyCondition == "Drizzle":
                tempEmbed.set_image("https://thumbs.gfycat.com/AbleWindingIceblueredtopzebra-size_restricted.gif")
            elif skyCondition == "Rain":
                tempEmbed.set_image("https://ewscripps.brightspotcdn.com/dims4/default/b092021/2147483647/strip/true/crop/597x336+0+0/resize/1280x720!/quality/90/?url=http%3A%2F%2Fewscripps-brightspot.s3.amazonaws.com%2Fbc%2F0d%2Fc3a24fcf488b8d82d5593b723f63%2Fhnet-image.gif")
            elif skyCondition == "Snow":
                tempEmbed.set_image("https://j.gifs.com/kRRx0K.gif")
            elif skyCondition == "Mist":
                tempEmbed.set_image("https://media4.giphy.com/media/ZWRCWdUymIGNW/giphy.gif")
            elif skyCondition == "Smoke":
                tempEmbed.set_image("https://64.media.tumblr.com/f35df9fd0a4b8840d342718f4bd54476/c039479d653db7fe-ad/s540x810/a2bb1d88ba2863e762d5b772e92db60c096a696a.gif")
            elif skyCondition == "Haze":
                tempEmbed.set_image("https://c.tenor.com/-GGPgili4BoAAAAC/foggy-fog.gif")
            elif skyCondition == "Dust":
                tempEmbed.set_image("https://thumbs.gfycat.com/CalmGlitteringBilby-size_restricted.gif")
            elif skyCondition == "Fog":
                tempEmbed.set_image("https://media.tenor.com/5ImWLS5QAJgAAAAC/foggy-fog.gif")
            elif skyCondition == "Sand":
                tempEmbed.set_image("https://media.tenor.com/zXtcL1numtAAAAAd/sand-sandstorm.gif")
            elif skyCondition == "Ash":
                tempEmbed.set_image("https://s.w-x.co/big-flakes.gif?crop=16:9&width=480")
            elif skyCondition == "Squall":
                tempEmbed.set_image("https://media.tenor.com/27mSeF5fDXEAAAAd/snow-day.gif")
            else:
                tempEmbed.set_image("https://i.pinimg.com/originals/3a/76/20/3a762091c6d9fb10d75ed9793d3beb29.gif")
            tempEmbed.set_footer(text=f"Sky status in {location} is: {skyDesc}")
            await ctx.send(embed=tempEmbed)
        except KeyError:
            await ctx.send(embed=error_message(location))
            
    @nextcord.slash_command(description="🌡️ - It sends information about the selected location temperature.")
    async def weathernow(self ,ctx, *, location):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={"7745a414566393bd03c26c9f7b65a359"}&units=metric'
        try:
            data = parse_data(json.loads(requests.get(url).content)['main'])
            data2 = parse_data(json.loads(requests.get(url).content)['weather'])
            skyCondition = data2[0]['main']
            skyDesc = data2[0]['description']
            tempEmbed = weather_message(data, location)
            if skyCondition == "Clouds":
                tempEmbed.set_image("https://thumbs.gfycat.com/BountifulAcidicChihuahua-max-1mb.gif")
            elif skyCondition == "Tornado":
                tempEmbed.set_image("https://acegif.com/wp-content/uploads/2022/fzk5d/20-smooth-storm.gif")
            elif skyCondition == "Thunderstorm":
                tempEmbed.set_image("https://i.pinimg.com/originals/dd/f1/48/ddf1482dcd4dc5fc267cfa0a6c0cd720.gif")
            elif skyCondition == "Drizzle":
                tempEmbed.set_image("https://thumbs.gfycat.com/AbleWindingIceblueredtopzebra-size_restricted.gif")
            elif skyCondition == "Rain":
                tempEmbed.set_image("https://media.discordapp.net/attachments/931640602490187866/1044333798797619220/descarga.gif")
            elif skyCondition == "Snow":
                tempEmbed.set_image("https://j.gifs.com/kRRx0K.gif")
            elif skyCondition == "Mist":
                tempEmbed.set_image("https://media4.giphy.com/media/ZWRCWdUymIGNW/giphy.gif")
            elif skyCondition == "Smoke":
                tempEmbed.set_image("https://64.media.tumblr.com/f35df9fd0a4b8840d342718f4bd54476/c039479d653db7fe-ad/s540x810/a2bb1d88ba2863e762d5b772e92db60c096a696a.gif")
            elif skyCondition == "Haze":
                tempEmbed.set_image("https://c.tenor.com/-GGPgili4BoAAAAC/foggy-fog.gif")
            elif skyCondition == "Dust":
                tempEmbed.set_image("https://thumbs.gfycat.com/CalmGlitteringBilby-size_restricted.gif")
            elif skyCondition == "Fog":
                tempEmbed.set_image("https://media.tenor.com/5ImWLS5QAJgAAAAC/foggy-fog.gif")
            elif skyCondition == "Sand":
                tempEmbed.set_image("https://media.tenor.com/zXtcL1numtAAAAAd/sand-sandstorm.gif")
            elif skyCondition == "Ash":
                tempEmbed.set_image("https://s.w-x.co/big-flakes.gif?crop=16:9&width=480")
            elif skyCondition == "Squall":
                tempEmbed.set_image("https://media.tenor.com/27mSeF5fDXEAAAAd/snow-day.gif")
            else:
                tempEmbed.set_image("https://i.pinimg.com/originals/3a/76/20/3a762091c6d9fb10d75ed9793d3beb29.gif")
            tempEmbed.set_footer(text=f"Sky status in {location} is: {skyDesc}")
            await ctx.send(embed=tempEmbed)
        except KeyError:
            await ctx.send(embed=error_message(location))
    
        
def setup(client):
    client.add_cog(FORECAST(client))
