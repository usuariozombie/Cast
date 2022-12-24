# -*- coding: utf-8 -*-

import nextcord, requests
from nextcord.ext.commands import Cog, command
from utils import Debug, JSON, now, TextClearer
from nextcord import Embed, Interaction, SlashOption, slash_command

SkyConditions = ["ash", "cast", "clouds", "drizzle", "dust", "fog", "haze", "mist", "rain", "sand", "smoke", "snow", "squall", "thunderstorm", "tornado"]
KeyFeatures = {"feels_like" : "Feels Like", "grnd_level": "Ground Level", "humidity" : "Humidity in %", "main" : "Sky Condition", "pressure" : "Pressure in Millibars", "sea_level": "Sea Level", "temp" : "Temperature", "temp_max" : "Maximum", "temp_min" : "Minimum"}

class Forecast(Cog):

	def __init__(self, client): self.client = client

	@Cog.listener()
	async def on_ready(self): Debug.Good(f"{self.__cog_name__} loaded successfully!")

	@command()
	async def weather(self, ctx, *, location):
		CastImages = requests.get("https://api.usuariozombie.com/discord/cast").json()["images"]
		ConfigData = JSON.Read("config.json")
		WeatherRequest = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={ConfigData['OWMAPIKey']}&q={location}&units={ConfigData['Units']}")

		if WeatherRequest.status_code == 200:
			try:
				WeatherData = WeatherRequest.json()
				SkyCondition = WeatherData["weather"][0]["main"]
				WeatherEmbed = Embed(color = 0xFF6500)
				WeatherEmbed.set_author(name = f"Weather in {TextClearer(location)}", icon_url = CastImages["cast"])
				WeatherEmbed.set_footer(text = f"Sky status in {TextClearer(location)} is: {WeatherData['weather'][0]['description']}")
				if SkyCondition.lower() in SkyConditions: WeatherEmbed.set_image(url = CastImages[SkyCondition.lower()])
				else: WeatherEmbed.set_image(url = CastImages["normal"])
				WeatherEmbed.set_thumbnail(url = CastImages["thumbnail"])
				for Key in WeatherData["main"]:
					WeatherEmbed.add_field(name = KeyFeatures[Key], value = WeatherData["main"][Key], inline = True)					
				await ctx.send(embed = WeatherEmbed)
			except Exception as Error:
				Debug.Error(f"Error fetching {location}:\n{Error}")
				ErrorEmbed = Embed(color = 0xFF0000, description = f"There was an error retrieving weather data for {TextClearer(location)[:256]}!", title = "ERROR!")
				await ctx.send(embed = ErrorEmbed)

		if WeatherRequest.status_code == 404:
			ErrorEmbed = Embed(color = 0xFF0000, description = f"No location was found for {TextClearer(location)[:256]}!", title = "ERROR!")
			await ctx.send(embed = ErrorEmbed)

	@slash_command(name = "weather")
	async def weather(self, interaction: Interaction): pass

	@weather.subcommand(name = "current", description = "🌡️ - Get in real time temperature information about the selected location.")
	async def current(self, interaction: Interaction, location):
		CastImages = requests.get("https://api.usuariozombie.com/discord/cast").json()["images"]
		ConfigData = JSON.Read("config.json")
		WeatherRequest = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={ConfigData['OWMAPIKey']}&q={location}&units={ConfigData['Units']}")
		if WeatherRequest.status_code == 200:
			try:
				WeatherData = WeatherRequest.json()
				SkyCondition = WeatherData["weather"][0]["main"]
				WeatherEmbed = Embed(color = 0xFF6500)
				WeatherEmbed.set_author(name = f"Weather in {TextClearer(location)}", icon_url = CastImages["cast"])
				WeatherEmbed.set_footer(text = f"Sky status in {TextClearer(location)} is: {WeatherData['weather'][0]['description']}")
				if SkyCondition.lower() in SkyConditions: WeatherEmbed.set_image(url = CastImages[SkyCondition.lower()])
				else: WeatherEmbed.set_image(url = CastImages["normal"])
				WeatherEmbed.set_thumbnail(url = CastImages["thumbnail"])
				for Key in WeatherData["main"]:
					WeatherEmbed.add_field(name = KeyFeatures[Key], value = WeatherData["main"][Key], inline = True)					
				await interaction.response.send_message(embed = WeatherEmbed)
			except Exception as Error:
				Debug.Error(f"Error fetching {location}:\n{Error}")
				ErrorEmbed = Embed(color = 0xFF0000, description = f"There was an error retrieving weather data for {TextClearer(location)[:256]}!", title = "ERROR!")
				await interaction.response.send_message(embed = ErrorEmbed)

		if WeatherRequest.status_code == 404:
			ErrorEmbed = Embed(color = 0xFF0000, description = f"No location was found for {TextClearer(location)[:256]}!", title = "ERROR!")
			await interaction.response.send_message(embed = ErrorEmbed)

	@weather.subcommand(name = "forecast", description = "🌡️ - Get in real time temperature information about the selected location.")
	async def forecast(self, interaction : Interaction, location, language : str = SlashOption(name = "language", choices = {"English": "en", "French": "fr", "Spanish": "es"})):
		CastImages = requests.get("https://api.usuariozombie.com/discord/cast").json()["images"]
		ConfigData = JSON.Read("config.json")
		WeatherRequest = requests.get(f"https://wttr.in/{TextClearer(location)}?format=j1")
		try:
			if WeatherRequest.status_code == 400:
				ErrorEmbed = Embed(color = 0xFF0000)
				ErrorEmbed.set_image(url = CastImages["error"])
				if language == "en": ErrorEmbed.set_author(name = f"An error occurred when requesting information from {TextClearer(location)[:256]}", icon_url = CastImages["cast"])
				if language == "es": ErrorEmbed.set_author(name = f"Hubo un error recopilando información de {TextClearer(location)[:256]}", icon_url = CastImages["cast"])
				if language == "fr": ErrorEmbed.set_author(name = f"Une erreur s'est produite lors de la demande d'informations de {TextClearer(location)[:256]}", icon_url = CastImages["cast"])
				await interaction.response.send_message(embed = ErrorEmbed)
			else:
				WeatherEmbed = Embed(color = nextcord.Color.random())
				WeatherEmbed.set_image(url = f"https://wttr.in/{TextClearer(location)}_2qp_lang={language}.png?m&{now('unix')}3")
				if language == "en":
					WeatherEmbed.set_author(name = f"Weather in {TextClearer(location)}", icon_url = CastImages["cast"])
					WeatherEmbed.set_footer(text = f"Requested by {TextClearer(interaction.user.display_name)} • 3 days weather forecast")
				elif language == "es":
					WeatherEmbed.set_author(name = f"Tiempo en {TextClearer(location)}", icon_url = CastImages["cast"])
					WeatherEmbed.set_footer(text = f"Solicitado por {TextClearer(interaction.user.display_name)} • Predicción de 3 días")
				elif language == "fr":
					WeatherEmbed.set_author(name = f"Temps en {TextClearer(location)}", icon_url = CastImages["cast"])
					WeatherEmbed.set_footer(text = f"Demandé par {TextClearer(interaction.user.display_name)} • Prévisions météorologiques à 3 jours")
				else:
					WeatherEmbed.set_author(name = f"Temps en {TextClearer(location)}", icon_url = CastImages["cast"])
					WeatherEmbed.set_footer(text = f"Demandé par {TextClearer(interaction.user.display_name)} • Prévisions météorologiques à 3 jours")
				await interaction.response.send_message(embed = WeatherEmbed)
		except:
			await interaction.response.send_message("> `An error has occurred while processing your request`", ephemeral = True)

def setup(client):
	client.add_cog(Forecast(client))