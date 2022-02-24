<div align="center">
    <h1>MrPython</h1>
    <p>This is a Multifunction bot. Current Bot language is de-DE but I will change it soon.</p>
    <p>The bot is still in Development so please when you find any issues, report it here over the issues tab</p>
</div>

## Index

* [Commands](#commands)
  * [Administration](#administration)
  * [User](#user-commands)
  * [Custom Server Commands](#custom-server-commands)
* [API List](#api-list)

### Commands
Here are listed all the Commands that the Bot has.

#### Administration
* [x] `$mccreate (category id)` -> To create up to 4 channel, when more than 4 channel already available, it takes the first four, when under four channel are available it will create create channel up to 4. The channel contents are are: all Users on the Discord, User that are Online, User inside a voice channel and All Voicechannel.
* [ ] `$jtc set (voicechannel id)` -> Set a Join to Create(JTC) channel. issue: <a href="github.com/kenexar/discord-mr-python/issues/18">#18</a>
* [ ] `$levelsystem (true | false)` -> To activate or deactivate the Levelsystem for the server
* [ ] `$twitchnotify set (streamer name)` ->  Set a streamer name or more for Twitchnotify (it needed a channel to activate it)
* [ ] `$twitchnotify define (notify channel mention)`
#### User-Commands
* [ ] `$jtc channel (owner | set-owner [member mention] | name [new name] | info)` -> this command changes or show information about the current channel (you must be inside a custom voice channel for that action)
* [x] `$credits` -> Show the Credits from the Bot
* [x] `$lyrics (artist) (title)` -> Show the lyrics to the Song!
* [x] `$faceit player (faceit nickname)` -> Find a Faceit player and show his Csgo Stats
* [ ] `$faceit_verify` -> Sets the current channel (where the message was send) to the Verify channel. issue: <a href="github.com/kenexar/discord-mr-python/issues/20">#20</a>

#### Custom-server-commands
##### Betrayed community server:
###### Management
  * [x] `$selfrole (agent | ranks)` -> Send the Agent/Rank selector messages new

### API-List
* [x] `Faceit` -> Player stats tracking and Player finder
* [x] `Lyrics.ovh` -> Get Lyrics from songs
* [ ] `Trackergg` -> Player stats tracking, Player finder, Clan creation
* [ ] `SteamWebAPI` -> Information to find multiple user with the same interests

note: I (exersalza) have no partnership with any of the Games or Api Provider, I just love to have API's inside of the Bot to bring a little swing inside the Community
