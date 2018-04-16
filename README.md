# 🤖 Slack Channel Archiver
It is a serverless function that periodically archive old / no message channel.

***DEMO:***

![image](https://user-images.githubusercontent.com/1152469/37551788-0e4f95cc-29eb-11e8-9c7f-db281960837b.png)

## Description
Using Slack's LEGACY TOKEN to check channels, and archive old channel.
This Lambda function starts periodically by AWS Cloudwatch Events.
LEGACY TOKEN needs to be create manually, but AWS side automates environment construction by using Serverless Framework.

## Requirement
- AWS Account
- Serverless Framework
- [serverless-plugin-aws-alerts](https://serverless.com/blog/serverless-ops-metrics/) (optional)
- Slack Account

## Installation
1. Create LEGACY TOKEN from [Here](https://api.slack.com/custom-integrations/legacy-tokens)

2. Clone this repo.
```
$ git clone https://github.com/saitota/SlackChannelArchiver.git
```

4. Modify environment_dev.yml 's two TOKEN to your token.
``` environment_dev.yml
LEGACY_TOKEN: 'xoxp-000000000000-000000000000-000000000000-0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x0x'
```

5. Deploy with Serverless Framework (you must aws-cli initialize before)
```
$ sls deploy ./SlackChannelArchiver
...
api keys:
  None
endpoints:
  None
functions:
  fnc: SlackChannelArchiver-dev-fnc
```
6. Done! Wait a time to archive. (12:00 JST  is the default)

# 🤔 Anything Else
I wrote article about this function.

[古い Slack チャンネルを自動でアーカイブする機能を作りました - Qiita](https://qiita.com/saitotak/items/6f84de5218b71831ce2b)

# 🐑 Author
[saitotak](https://qiita.com/saitotak)

# ✍ License
[MIT](./LICENSE)

