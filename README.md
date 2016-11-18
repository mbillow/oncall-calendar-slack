# Google Calendar to Slack Sync

Built for @ComputerScienceHouse at the Rochester Institute of Technology

The goal of this utility was to read from a Google Calendar that has our sys-admin on-call schedule and then translate that to a User Group on Slack and putting the current on-call in the topic of our discussion channel. This enables us to mention [at]oncall on Slack to send a notification to our on-call sys-admin as well as notify interested parties who is on-call via channel topic.

Built using the [slacker](https://github.com/os/slacker) module by @os.