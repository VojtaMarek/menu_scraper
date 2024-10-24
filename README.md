# Restaurant Menu Scraper

This Python script automates the task of scraping the daily menu from a restaurant's Facebook page and sending notifications to users via RocketChat.

## Features
- Scrapes Facebook profile for menu images.
- Extracts food data from the images using AI image processing.
- Sends RocketChat notifications with the daily menu.
- Uses Selenium for web automation and scraping.
- Optional email notification functionality (currently commented out).

## Requirements
The following libraries and services are required to run the script:

- Python 3.x
- Selenium
- RocketChat API
- `chromedriver` installed at `/usr/bin/chromedriver`
- AI module for food image processing (from `ai_module`)
- Configuration file (`config.py`)

### Python Libraries
Install the necessary libraries using pipenv package manager:

```bash
pipenv install
```
### ChromeDriver
Make sure you have chromedriver installed and placed in the correct path. On Linux, you can install it using:

```bash
sudo apt-get install chromium-chromedriver
```
### Configuration
Create a config.py file with the following structure:

```python
RESTAURANT = {
    'name': 'Your Restaurant Name',
    'fb_page': 'https://www.facebook.com/your-restaurant-page',
}

OPEN_AI_KEY = 'your-openai-api-key'

ROCKET_CHAT = {
    'host': 'https://your-rocketchat-server.com',
    'user': 'your-username',
    'password': 'your-password',
}

# SMTP = {
#     'host': 'smtp.your-email-server.com',
#     'port': 587,
#     'user': 'your-email@example.com',
#     'password': 'your-password',
# }

RECIPIENTS = ['user1@example.com', 'user2@example.com']
```
### How to Run
Ensure that chromedriver is installed and accessible at /usr/bin/chromedriver.
Run the script using the following command:
```bash
pipenv run python your_script.py
```
The script will:
* Scrape the menu from Facebook.
* Extract food information using the `process_food_image` function from the `ai_module`.
* Send a RocketChat notification to the recipients specified in config.RECIPIENTS.
* RocketChat Notifications
* The `send_rocketchat_notification` function sends a message to the user's RocketChat channel (based on their email). It sends the extracted menu data and a link to the scraped image.

### Email Notifications (Optional)
In progress, the feature is currently commented out in the script. The script can send email notifications to the recipients specified in the config file. To enable this feature, uncomment the email notification code in the script.

### Example Output
After running, the script will generate and send a message like this to RocketChat:

```markdown
**Today's menu**

**Vegetable soup** 🌶
Zeleninová polévka - klasická zeleninová polévka se sezónní zeleninou.

**Chicken Tikka Masala** 🌶🌶🌶
Kuřecí Tikka Masala - kuřecí kousky v kořeněné omáčce, typické indické jídlo s krémovou texturou.

[Link to the menu picture](https://www.facebook.com/photo-link)
```
### Error Handling
The script handles common errors, such as:

* Connection issues with RocketChat.
* Issues with finding the appropriate elements on the webpage.
If any issues arise during scraping, the script will retry after a 5-second delay.

### License
```
This project is licensed under the MIT License.
```

Note: This script is for educational purposes only. Please respect the terms of service of the websites you are scraping. 
This file was created with the help of OpenAI's GPT-4o.