# LoL info bot
#### Video Demo:  [Link to the video](https://youtu.be/aowlEX_-1gY)
#### Description:
This app is about live checking if typed users are currently playing League of Legends and notyfying it directly on the desktop.

#### Insert data
At the beggining CLI asks you to input username and tag then it creates instance of class Player. When ever user is added to the app is sends requests to the Riot's API to check what are uuids of the users and write them in Player instance. 

#### Checking the players
Next it checks repetivly if the users started ranked match and is currently playing match in League of Legends sending proper requests to picked Riot APIs. If so, it pushes the desktop notification via plyer.notification and starts to check if this match has ended. When it is finished, checking the results of the match and checking new ranking stats of every player. Then it pushes notyfication with combined info of winning/losing and stats of this user in this particular match along with new solo rank stats.

Application is prepared to check several users at the same time, what is handy when you are checking your teammates. 

Current state of the app has hardcoded part about server region, thats why it is necessary to use EUROPE users only.


#### IMPORTANT
Before using app, you need to put your API Key received from Riot. Without this, you won't be able to receive any info.
You can receive temporary Riot API key here:
https://developer.riotgames.com/

But it is recommended to register developer/app to receive const API Key

Thank you for the course.
This was CS50P!

For now it is hardcoded only for EUROPE servers.