from bs4 import BeautifulSoup
import requests
import re
from data_obj import Event
from collections import defaultdict


def scrape_website():
    events = []
    website_link = (
        "https://www.discoverdurham.com/events/things-to-do-in-durham-this-week/"
    )
    response = requests.get(website_link)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, "html.parser")
    for event_tag in soup.find_all("div", {"class": "blk from-wysiwyg"}):
        if event_tag.text.split(",")[0].strip() in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]:
            date = event_tag.find("h2").text
            time = None
            for p_tag in event_tag.find_all("p"):
                is_time_tag = "p.m." in p_tag.text or "a.m." in p_tag.text
                if is_time_tag:
                    time = p_tag.text
                elif time != None:
                    # print(p_tag.text)
                    event_list = p_tag.text.split("at")
                    event = Event(
                        name=event_list[0].strip(),
                        start_time=time.strip(),
                        website=p_tag.find("a", attrs={"href": re.compile("^https://")})
                        .get("href")
                        .strip(),
                        date=date.strip(),
                        location=event_list[1].strip(),
                    )
                    events.append(event)

            # find time
            # while loop until new time
            # inside while, keep creating a new event
    write_events_to_file(events=events)
    return events


def clear_event_file():
    file = open("email.txt", "w")
    file.write("")


def write_events_to_file(events):
    clear_event_file()
    day_event = defaultdict(list)
    for event in events:
        day_event[event.date].append(event)
    file = open("email.txt", "a")
    for day in day_event:
        text = f"""
<h1>{day}</h1>
        """
        for event in day_event[day]:
            text += f"""
<p><a href="{event.website}" target="_blank"><strong>{event.name}</strong> at {event.location}</a>
Event Time: {event.start_time}</p>
"""
        file.write(text)


def get_recipients():
    addresses = []
    file = open("recipients.txt", "r")
    for address in file.readlines():
        if isValid(address):
            addresses.append(address.strip())
    return addresses


# recipients: list[]
def add_recipients_to_file(recipients):
    file = open("recipients.txt", "a")
    existing_recipients = get_recipients()
    for recipient in recipients:
        if recipient not in existing_recipients and isValid(recipient):
            file.write(recipient + "\n")


def isValid(address):
    nonEmpty = address.strip() != ""
    # todo: @____.com, no whitespace
    return nonEmpty


# print(get_recipients())
# add_recipients(["trisha00menon@gmail.com"])
# print(get_recipients())
