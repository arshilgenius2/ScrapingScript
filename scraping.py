from bs4 import BeautifulSoup
import requests
import smtplib
import time
from keep_alive import keep_alive
# Set up the email account information
sender_email = 'arshilgenius@gmail.com'
sender_password = 'dadapaqzfunezaiu'
receiver_email = 'arshilgenius@gmail.com'


# Words to skip in post titles
skip_words = [
  "music", "dance", "chess", "rubiks cube", "quran", "tamil",
  "philosophy", "hydraulic", "aircraft", "aerospace", "hindi", "accounting",
  "qaida", "speaking", "japanese", "mandarin", "chinese", "arabic", "turkish",
  "trade", "thinking", "verilog", "keyboard", "piano", "vocal", "blockchain",
  "bioinformatics", "tinkercard", "speech", "finance", "health", "discrete",
  "ielts", "autocad", "dart", "animation", "multisim", "industrial",
  "structural", "malayalam", "swift", "islamic", "french", "spanish", "tabla",
  "yoruba", "dance", "zumba", "twi", "flight", "cfa",
  "hydrology", "urdu", "laravel", "financial", "yoga", "art",
  "salesforce", "hifz", "soldity", "paint", "slokas", "russian", ".net", "law",
  "bollywood", "gujrati", "medicine", "drums", "sex", "cooking", "account",
  "taxation", "accountancy", "fitness", "selenium", "tax", "nursing", "guitar",
  "machine", "vba", "histology", "stochastic", "islam", "keras", "pte", "gym",
  "unity", "gre", "pentesting", "veena", "surveying", "german", "ccna",
  "radiation", "psychology", "spss", "abacus", "odoo", "biomaterials",
  "nuclear", "funds", "astronautics", "trading", "dermatology", "dental",
  "architecture", "translation", "singing", "grammar", "archeology", "media",
  "oriya", "rendering", "rhinoceros", "violen", "revit", "gis", "celpip",
  "grass", "somalia", "editor", "hifdth", "political", "swahili",
 "flute", "simulation", "marketing", "biomechanics", "eagle",
  "voice", "fba", "blender", "control", "supply", "italian", "linguistics",
  "nuke", "econometrics", "bharatanatyam", "acca", "kurdish", "amharic",
  "mbbs", "reservoir", "pharmacology", "cadence", "epidemiology", "dyslexia",
  "blender", "interior", "filipino", "cryptography", "physiology", "fea",
  "sanskrit", "celpip", "shlokas", "drawing"
]
# Set up previous scraped data

prev_scraped_data = []


def has_no_number(string):
  """
    Returns True if the given string does not contain any digit (0-9), False otherwise.
    """
  return not any(char.isdigit() for char in string)


keep_alive()

while True:
  # Send request to the website
  url = "https://www.teacheron.com/tutor-jobs"
  response = requests.get(url)

  # Parse HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")

  # Find the main container of the posts
  main_container = soup.find("div", {"id": "tutorOrJobSearchItemList"})

  # Set up current scraped data
  scraped_data = []

  # Loop through each post and extract the desired information
  for post in main_container.find_all("div", class_="inner-results"):
    post_link = post.find("a").get("href")
    post_title = post.find("a").text.strip()

    # Check if post title contains any of the skip words
    if any(word in post_title.lower() for word in skip_words):
      continue

    # Send request to the post link and extract the post description
    post_response = requests.get(post_link)
    post_soup = BeautifulSoup(post_response.content, "html.parser")
    post_description = post.find('p', class_='job-description').text.strip()
    post_amount = ""
    post_location = ""
    for li in post.find_all("li", class_="tooltips margin-right-10"):
      if "data-original-title" in li.attrs and "USD" in li.attrs[
          "data-original-title"]:
        post_amount = li.attrs["data-original-title"].split("D")[0] + "D"

      x = li.find("span",
                  class_=False,
                  string=lambda text: text and "ago" not in text and "/" not in
                  text and "(" not in text)
      if x:
        post_location = x.text.strip()
        # print(post_location)
        # print(amount)
        # break
    if not any(word in post_location for word in [
        "Pakistan",
        "Turkey",
        "Kenya",
        "Sri Lanka",
        "Ghana",
        "Uganda",
        "Bangladesh",
        "Yemen",
        "Nigeria",
        "Lebanon",
        "Iraq",
      "India"
    ]):
      scraped_data.append(
        f"Link: {post_link}\nTitle: {post_title}\nAmount: {post_amount}\nLocation: {post_location}\nDescription: {post_description}\n"
      )

  # Send email with new scraped data
  if new_scraped_data:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
      server.starttls()
      server.login(sender_email, sender_password)
      message = 'Subject: TeacherOn Tutor Jobs\n\n' + '\n'.join(
        new_scraped_data)
      message = message.encode("utf-8")  # encode message as UTF-8
      server.sendmail(sender_email, receiver_email, message)
      


  # Wait for 60  minutes before scraping again
  time.sleep(300)
