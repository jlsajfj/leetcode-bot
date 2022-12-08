import discord
from datetime import date
from fetch_helper import *


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if(message.author == client.user):
        return

    username = str(message.author)
    u_message = str(message.content)
    fetch_uname = u_message.split(" ")
    channel = str(message.channel)

    print(f"{username} said: {u_message} in {channel}")
    if(u_message.startswith('.leetcode')):
        prim_data = prim_stats(fetch_uname[1])
        userName = prim_data['data']['matchedUser']['username']
        ranking = prim_data['data']['matchedUser']['profile']['ranking']
        avatar = prim_data['data']['matchedUser']['profile']['userAvatar']
        realname = prim_data['data']['matchedUser']['profile']['realName']
        print(userName, ranking, realname)
        
        prob_data = prob_stats(fetch_uname[1])
        total_prob = prob_data['data']['allQuestionsCount'][0]['count']
        total_prob_easy = prob_data['data']['allQuestionsCount'][1]['count']
        total_prob_med = prob_data['data']['allQuestionsCount'][2]['count']
        total_prob_hard = prob_data['data']['allQuestionsCount'][3]['count']
        print(total_prob, total_prob_easy, total_prob_med, total_prob_hard)

        total_solutions = prob_data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum'][0]["count"]
        easy_solutions = prob_data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum'][1]["count"]
        # if(easy_solutions == None):
        #     easy_solutions = 0
        med_solutions = prob_data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum'][2]["count"]
        hard_solutions = prob_data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum'][3]["count"]
        print(total_solutions, easy_solutions, med_solutions, hard_solutions)

        easy_per = prob_data['data']['matchedUser']['problemsSolvedBeatsStats'][0]["percentage"]
        if(easy_per == None):
            easy_per = 0
        medium_per = prob_data['data']['matchedUser']['problemsSolvedBeatsStats'][1]["percentage"]
        if(medium_per == None):
            medium_per = 0
        hard_per = prob_data['data']['matchedUser']['problemsSolvedBeatsStats'][2]["percentage"]
        if(hard_per == None):
            hard_per = 0
        print(easy_per, medium_per, hard_per)

        embed = discord.Embed(
            title = f"{realname}'s Leetcode Stats",
        )
        embed.set_footer(text=f"{date.today()}")
        embed.set_image(url=f"{avatar}")
        embed.set_thumbnail(url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fleetcode.com%2F&psig=AOvVaw1-HRl4lLGBKk1kLKjTrk9z&ust=1670571535327000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCMi9mYnC6fsCFQAAAAAdAAAAABAE")
        embed.set_author(name="Leetcode Fetcher")

        embed.add_field(name="Solved Leetcodes", value=f"{total_solutions}/{total_prob}", inline=False)
        embed.add_field(name="Easy", value=f"{easy_solutions}/{total_prob_easy}({easy_per})", inline=True)
        embed.add_field(name="Medium", value=f"{med_solutions}/{total_prob_med}({medium_per})", inline=True)
        embed.add_field(name="Hard", value=f"{hard_solutions}/{total_prob_hard}({hard_per})", inline=True)

        await message.channel.send(embed=embed)

        
client.run("-.-.-")

