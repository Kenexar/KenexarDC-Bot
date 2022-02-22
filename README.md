<div align="center">
    <h1>MrPython</h1>
    <p>This is a Multifunction bot. Current Bot language is de-DE but I will change it soon.</p>
    <p>The bot is still in Development so please when you find any issues, report it here over the issues tab</p>
</div>

## Index

* [Commands](#commands)
  * [Administration](#administration)
  * [User](#user commands)
  * [Custom Server Commands](#custom server commands)
* [API List](#api-list)

### Commands
Here are listed all the Commands that the Bot has.

#### Administration
* [ ] `$create` -> To create a Category with four channel inside it, the channels are: all Users on the Discord, User that are Online, User inside a voice channel and All Voicechannel. issue (#19)
* [ ] `$jtc set (voicechannel id)` -> Set a Join to Create(JTC) channel. issue: (#18)
* [ ] `$levelsystem (true | false)` -> To activate or deactivate the Levelsystem for the server
* [ ] `$twitchnotify set (streamer name)` ->  Set a streamer name or more for Twitchnotify (it needed a channel to activate it)
* [ ] `$twitchnotify define (notify channel mention)`
#### User Commands
* [ ] `$jtc channel (owner | set-owner [member mention] | name [new name] | info)` -> this command changes or show information about the current channel (you must be inside a custom voice channel for that action)
* [x] `$credits` -> Show the Credits from the Bot
* [x] `$lyrics (artist) (title)` -> Show the lyrics to the Song!
* [x] `$faceit player (faceit nickname)` -> Find a Faceit player and show his Csgo Stats
* [ ] `$faceit_verify` -> Sets the current channel (where the message was send) to the Verify channel. issue: (#20)

#### Custom server commands
##### Betrayed community server:
###### Management
  * [x] `$selfrole (agent | ranks)` -> Send the Agent/Rank selector messages new

### API-List
* [x] `Faceit` -> Player stats tracking and Player finder
* [ ] `Trackergg` -> Player stats tracking, Player finder, Clan creation
* [ ] `SteamWebAPI` -> Information to find multiple user with the same interests

note: I (exersalza) have no partnership with any of the Games or Api Provider, I just love to API's inside of the Bot to bring a little swing inside the Community
