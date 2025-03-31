# Earthquake Notification

This is a simple Earthquake Notification service that sends real-time alerts to Discord whenever an earthquake of magnitude 3.0 or higher occurs. The alerts include details such as the earthquake's magnitude, location, and the time it occurred, all formatted for easy readability in Thailand's local timezone (UTC+7).

## Features
- Fetches earthquake data from the USGS Earthquake API.
- Sends notifications to Discord using a webhook.
- Alerts are sent every minute, or can be triggered manually via GitHub Actions.
- The color of the message in Discord varies based on the earthquake's magnitude:
  - Red for magnitudes 7.0 and above
  - Orange for magnitudes 6.0-6.9
  - Yellow for magnitudes 5.0-5.9
  - Green for magnitudes below 5.0

## Setup

### Prerequisites
- You need a GitHub repository with GitHub Actions enabled.
- A Discord webhook URL for receiving notifications.

### Environment Variables
- Set the `DISCORD_WEBHOOK_URL` as a secret in your GitHub repository. This webhook URL will be used to send the earthquake notifications to your Discord channel.

### Workflow

The notification system is automated using GitHub Actions. It runs every minute based on a cron schedule, and it can also be triggered manually. 

The GitHub Actions workflow file `.github/workflows/earthquake_notification.yml` is configured as follows:

```yaml
name: Earthquake Notification

on:
  schedule:
    - cron: "* * * * *"  # Run every minute
  workflow_dispatch:  # Allows manual trigger

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.x"
      - name: Install Dependencies
        run: |
          pip install requests
          pip install pytz
      - name: Run Script
        env:
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python earthquake_alert.py
