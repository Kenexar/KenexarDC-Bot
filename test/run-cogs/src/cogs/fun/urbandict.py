import requests
import nextcord

from nextcord.ext import commands


class UrbanDict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Command
    async def urban(self, ctx, term):
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

        querystring = {"term": term}

        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': self.bot.urban_key
        }

        response: requests.Response = requests.request("GET", url, headers=headers, params=querystring)
        embed = nextcord.Embed(title=term,
                               color=self.bot.embed_st,
                               timestamp=self.bot.current_timestamp())
        lst = response.json()['list']
        if response.status_code != 200 or not lst:  # clean all types of error codes to not crash the bot
            if response.status_code != 200:
                self.bot.logger.error(f'Error code at Urban Api {response.status_code!r}')

            embed.description = f'Cannot find your term or the Api didnt respond'
            return await ctx.send(embed=embed)

        data = response.json()['list'][0]
        whitespace = '\u200b'
        embed.title = f'[{data.get("word")}]({data.get("permalink")})'
        print(f'https://www.urbandictionary.com/author.php?author={data.get("author")}')
        embed.set_author(name=f'Author: {data.get("author")}')
        embed.description = f'**Definition:** {data.get("definition")}\n\n**Example:** {data.get("example")}'
        embed.set_footer(text=f'Upvotes: {data.get("thumbs_up")} - Downvotes: {data.get("thumbs_down")}')

        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UrbanDict(bot))
