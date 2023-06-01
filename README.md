# Dave Prime
## A modern Discord bot for the Nekomeowncer community

This is a specialised bot for Twitch streamer (and friend) [TheNekomeowncer](https://www.twitch.tv/thenekomeowncer)'s Discord server.

It's just a personal project for fun so don't look into it too much!

## Current features

- "Streamerboost": Give any member who is currently streaming a special role. This can be used to show people streaming above everyone else on the member list in order to promote them. NOTE: This will unfortunately cause your Audit Log to fill up if triggered often.
- Moderation Alerts: Instant Discord time-out, ban, and unban alerts.
- Various app commands

All commands in this bot use Discord's slash-commands. Type a "/" in chat and select Dave Prime's icon to see all of the commands.

## Setup

1.  Clone this repo
2.  Install dependencies from requirements.txt file
3.  Create ".env" file in bot directory
4.  Format like so:
    
    ```
    BOT_TOKEN=""     # string
    MAIN_GUILD=""    # string (Discord Snowflake)
    TEST_GUILD=""    # string (Discord Snowflake)
    TEST_ENV=""      # bool (true/false)
    OPENAI_KEY=""    # string
    ```

3.  Fill the variables with the appropriate values
4.  Run main.py
5.  Go wild

## Formatting

This project is formatted with the [Black](https://github.com/psf/black) formatter.
