## SwedwishWeatherBot

SwedwishWeatherBot is a Telegram bot designed to provide weather information for different cities. Whether you're curious about the current temperature, weather conditions, or wind speed, this bot has you covered.

### Features:

- **Set Your City:** Use the `/set_city` command to set your city, so the bot can provide weather updates specific to your location.

- **Set Language Preference:** Choose your preferred language with the `/set_lang` command. Currently, supported languages include English (`en`) and Russian (`ru`).

- **Get Weather Updates:** Once your city is set, use the `/get_weather` command to receive detailed weather forecasts, including temperature, weather conditions, cloudiness, and wind speed.

### How to Use:

1. **Start the Bot:**
   - Begin by starting the bot with the `/start` command. This initializes your user profile.

2. **Set Your City:**
   - Use the `/set_city` command to set your city. Follow the prompts to input your city name.

3. **Set Language Preference:**
   - Optionally, use the `/set_lang` command to choose your preferred language.

4. **Get Weather Updates:**
   - Once your city is set, use the `/get_weather` command to receive detailed weather updates.

### Dependencies:

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): The Python wrapper for the Telegram Bot API.

- [OpenWeatherMap API](https://openweathermap.org/): Access weather data to provide accurate forecasts.
