import discord
import requests
import json
from datetime import date


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def prob_stats(username):
    cookies = {
        '__stripe_mid': '-',
        'csrftoken': '-',
    }

    headers = {
        'authority': 'leetcode.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': '',
        'content-type': 'application/json',
        'origin': 'https://leetcode.com',
        'referer': 'https://leetcode.com/patelshyamal016/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',
        'x-csrftoken': '9wjYjzwi9km3CkxuIu6w9MY3KNErXyIgiEFFVcpLsA5lrC4kdKapSG8mBS0DwWAD',
    }

    json_data = {
            'query': '\n    query userProblemsSolved($username: String!) {\n  allQuestionsCount {\n    difficulty\n    count\n  }\n  matchedUser(username: $username) {\n    problemsSolvedBeatsStats {\n      difficulty\n      percentage\n    }\n    submitStatsGlobal {\n      acSubmissionNum {\n        difficulty\n        count\n      }\n    }\n  }\n}\n    ',
            'variables': {
                'username': f'{username}',
        },
    }

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    json_data = json.loads(response.text)
    return json_data

    pass


def prim_stats(username):
    cookies = {
        'csrftoken': '-',
    }

    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        'query': 'query userPublicProfile($username: String!) {\n\tmatchedUser(username: $username) {\n\t\tcontestBadge {\n\t\t\tname\n\t\t\texpired\n\t\t\thoverText\n\t\t\ticon\n\t\t}\n\t\tusername\n\t\tgithubUrl\n\t\ttwitterUrl\n\t\tlinkedinUrl\n\t\tprofile {\n\t\t\tranking\n\t\t\tuserAvatar\n\t\t\trealName\n\t\t\taboutMe\n\t\t\tschool\n\t\t\twebsites\n\t\t\tcountryName\n\t\t\tcompany\n\t\t\tjobTitle\n\t\t\tskillTags\n\t\t\tpostViewCount\n\t\t\tpostViewCountDiff\n\t\t\treputation\n\t\t\treputationDiff\n\t\t\tsolutionCount\n\t\t\tsolutionCountDiff\n\t\t\tcategoryDiscussCount\n\t\t\tcategoryDiscussCountDiff\n\t\t}\n\t}\n}\n',
        'variables': {
            'username': f'{username}',
        },
        'operationName': 'userPublicProfile',
    }

    response = requests.post('https://leetcode.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    json_data = json.loads(response.text)
    
    return json_data

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

