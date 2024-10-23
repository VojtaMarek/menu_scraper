import datetime
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from selenium.webdriver.common.by import By
from rocketchat_API.rocketchat import RocketChat

import config
from ai_module import process_food_image

subject = config.RESTAURANT.get('name', 'Restaurant') + ' menu'


def send_rocketchat_notification(content, email):
    # RocketChat
    try:
        # instantiate RocketChat only if there are urgent notifications
        if config.ROCKET_CHAT['host']:
            rocket = RocketChat(user=config.ROCKET_CHAT['user'], password=config.ROCKET_CHAT['password'],
                                server_url=config.ROCKET_CHAT['host'])
        else:
            rocket = None
    except Exception as connection_error:
        print(f'Cannot connect to RocketChat API: {connection_error}')
        rocket = None
    if rocket:
        try:
            msg_to = email
            channel = '@' + msg_to.split('@')[0]
            rocket.chat_post_message(content, channel=channel, alias=subject, emoji=':fork_and_knife:')
        except Exception as send_error:
            print(f'Error while sending RocketChat notification: {send_error}')


# def send_email(img_png, link, subject, recipients):
#     smtp = config.SMTP
#     # Set up the server
#     smtp_server = smtp.get('host')
#     smtp_port = smtp.get('port')
#     username = smtp.get('user')
#     password = smtp.get('password')
#
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(user=username, password=password)
#         # compose a message
#         msg = MIMEMultipart()
#         msg.set_charset('utf-8')
#         msg['From'] = username
#         msg['To'] = ', '.join(recipients)
#         msg['Subject'] = f'{subject}: {subject}'
#         # msg['X-Priority'] = str(configuration['email_priority'])
#         # html_text = MIMEText(configuration['message'].format(url=config.PUBLIC_URL), 'html', _charset='utf-8')
#
#         # Add body to the email
#         body = f'Here is the picture of the post: {link}'
#         msg.attach(MIMEText(body, 'plain'))
#
#         # Attach the image
#         attachment = MIMEBase('application', 'octet-stream')
#         attachment.set_payload(img_png)
#         encoders.encode_base64(attachment)
#         attachment.add_header('Content-Disposition', f'attachment; filename=raavi_post.png')
#         msg.attach(attachment)
#
#         try:
#             server.send_message(msg)
#             return True
#         except Exception as send_error:
#             print(f'Cannot send email: {send_error}')
#             return False


def run_scraping_no_auth():
    global post_link, img_base64

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    # Create a Service object to define the path to chromedriver
    service = Service('/usr/bin/chromedriver')  # Ensure the path is correct
    # Initialize the WebDriver using the service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Now use driver.get() and other Selenium commands
    driver.get('https://www.facebook.com/profile.php?id=100093070844873&locale=en_US')

    # Find the button by class name
    try:
        button = driver.find_element(By.XPATH, "//span[text()='Decline optional cookies']")
        button.click()
        print("Button clicked successfully!")
    except Exception as e:
        print(f"Error: {e}")

    # Wait for the page to load
    time.sleep(1)

    # Find the close button by aria-label
    try:
        close_button = driver.find_element(By.XPATH, "//div[@aria-label='Close']")
        close_button.click()
        print("Close button clicked successfully!")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)

    # Click on the picture
    try:
        pic = driver.find_element(By.XPATH,
                                  '''//*[@id=':r1a:']/div[1]/div/div/div/div[1]/a/div[1]/div[1]/div/img''')
        time.sleep(1)  # Wait a bit after scrolling
        pic.click()
    except Exception as e:
        print(f"Error: {e}")
        return

    # get current url
    time.sleep(2)
    current_url = driver.current_url

    # Get the normal resolution picture
    normal_res_picture = driver.find_elements(By.TAG_NAME, 'img')[-1]
    # time.sleep(2)
    post_link = normal_res_picture.parent.current_url
    img_base64 = normal_res_picture.screenshot_as_base64
    image_link = normal_res_picture.get_attribute('src')

    return image_link


if __name__ == '__main__':
    # emails = sys.argv[1].split(',')

    todays_menu = False
    while not todays_menu:  # loop until the menu is from today
        while True:  # Infinite loop to keep trying until the menu is found
            if current_url := run_scraping_no_auth():
                food_data = process_food_image(current_url)
                if food_data.get('date') and datetime.date.fromisoformat(food_data['date']) == datetime.date.today():
                    todays_menu = True
                todays_menu = True  # Remove this line to enable date checking
                break
            else:
                print('Not found, trying again later...')
                time.sleep(5)  # wait 5 seconds before trying again

    # Prepare the content in markdown
    content = f"**Today's menu**\n\n"
    for item in food_data.get('menu', []):
        content += f"**{item.get('food_name', '')}** " \
                  f"{'🌶' * item.get('spiciness', '')}\n" \
                  f"{item.get('czech_translation', '')}\n\n"
    content += f"\n\n[Link to the menu picture]({post_link or ''})"
    print(content)

    emails = config.RECIPIENTS

    for email in emails:
        send_rocketchat_notification(content, email)
