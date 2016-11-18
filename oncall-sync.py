from slacker import Slacker
from datetime import date
import requests
import keys
import re

calendar_api = "https://www.googleapis.com/calendar/v3/calendars/g.rit.edu_61hmcjev3u2m4q98ooa5h1v5sk%40group." \
               "calendar.google.com/events?alwaysIncludeEmail=false&maxResults=1&orderBy=startTime&showDeleted=false" \
               "&singleEvents=true&timeMin={current_date}T00%3A00%3A00-00%3A00%3A00&fields=items" \
               "(description%2Csummary)&key={api_key}".format(api_key=keys.google_api,
                                                              current_date=date.today())
channel_id = "C0D9KMD7G"
oncall_group = "S346MV9U4"


def get_channel_topic(slack_instance, channel):
    channel_info = slack_instance.channels.info(channel=channel)
    current_topic = channel_info.body['channel']['topic']['value']
    return current_topic


def set_channel_topic(slack_instance, channel, topic):
    slack_instance.channels.set_topic(channel=channel,
                                      topic=topic)


def get_id_from_username(slack_instance, uid):
    user_list = slack_instance.users.list().body['members']
    for user in user_list:
        if user['name'] == uid:
            return user['id']


def set_group_members(slack_instance, group, users_list):
    slack_instance.usergroups.users.update(usergroup=group,
                                           users=users_list)


def get_current_oncall():
    # Returns a tuple of (<Name>, <Slack Username>) from the Google
    # Calendar API Service.
    api_result = requests.get(calendar_api).json()['items'][0]
    return api_result['summary'], api_result['description']

if __name__ == "__main__":

    slack = Slacker(keys.slack_api)

    # Get the current on-call from the Calendar
    name, username = get_current_oncall()

    # Get the current topic and replace the username.
    topic = get_channel_topic(slack, channel_id)
    topic_groups = re.match(pattern="(.*)(@\w*)(\*.*)",
                            string=topic).groups()

    # Check if the current on-call was the same yesterday.
    if topic_groups[1] != username:
        updated_topic = topic_groups[0]+username+topic_groups[2]
        set_channel_topic(slack, channel_id, updated_topic)
        set_group_members(slack, oncall_group, [get_id_from_username(slack, username[1:])])