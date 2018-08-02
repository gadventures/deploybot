# Deploy-Bot

## Quick Start
First, install deploybot

create a `constants.py` file with the following:

```
SLACK_WEBHOOK_URL = 'https://slack.com/api/'
SLACK_TOKEN = {your slack token, probably xoxp followed by a bunch of numbers}
```

Send the initial command with `SlackPost`. The first param is appended to the end of your base_msg, and the base_msg doesn't change. The idea here being to update the 'Status' of your deploys.
```
base_msg = """:parking: _Polaris_ Deployment Started :parking:
    *Environment*: _{}_
    *Branch:* `{}`
    *User:* {}
    *Status:* """.format(
        environment,
        git_branch,
        getpass.get_user(),
    )
msg = SlackPost('Deployment Started', base_msg=base_msg
```

Update your msg with `update`:
```
msg.update('Updating and Restarting')
```

Wrap sections that print to stdout with `threading`:
```
with msg.threading():
    print("hello")
```
