import requests, json, tempfile, os


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
    
def create_embed(username):
    profile_data = prim_stats(username)['data']['matchedUser']['profile']
    problem_data = prob_stats(username)['data']
    all_data = {'ranking': profile_data['ranking'], 'avatar': profile_data['userAvatar'], 'name': profile_data['realName']}
    
    if all_data['name'] == '':
      all_data['name'] = username
    
    if len(all_data['name']) <= 12:
      all_data['name'] += "'s Leetcode Stats"
    else:
      all_data['name'] += "'s Stats"
    
    for i in range(4):
      tmp_data = problem_data['allQuestionsCount'][i]
      diff = tmp_data['difficulty'].lower() + '_cnt'
      all_data[diff] = tmp_data['count']
      
      tmp_data = problem_data['matchedUser']['submitStatsGlobal']['acSubmissionNum'][i]
      diff = tmp_data['difficulty'].lower() + '_sub'
      all_data[diff] = tmp_data['count']
      
    for i in range(3):
      tmp_data = problem_data['matchedUser']['problemsSolvedBeatsStats'][i]
      diff = tmp_data['difficulty'].lower() + '_pct'
      all_data[diff] = tmp_data['percentage']
      if all_data[diff] is None:
        all_data[diff] = 0
      
    for diff in ['easy', 'medium', 'hard']:
      total_cnt = all_data[diff + '_cnt']
      sub_cnt = all_data[diff + '_sub']
      
      if sub_cnt == 0:
        all_data[diff + '_bar'] = ""
        continue
      
      ratio = sub_cnt / total_cnt * 200
      
      blank = """
      <path id="{diff}-filled"
        d="M0,0
        h{ratio}
        a5,5 0 0 1 0,10
        h-{ratio}
        a5,5 0 0 1 0,-10
      z"/>
      """
      
      all_data[diff + '_bar'] = blank.format(diff=diff, ratio=ratio)
    
    template = open('template.svg', 'r').read()
    filled_embed = template.format(**all_data)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.svg') as tmp:
      tmp.write(filled_embed)
      tmp.flush()
      
      os.system(f'inkscape "{tmp.name}" -o "{tmp.name}.png"')
      
      return tmp.name + '.png'
  
if __name__ == '__main__':
    print(create_embed('kotero'))