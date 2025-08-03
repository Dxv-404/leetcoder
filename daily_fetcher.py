import requests

def get_daily_problem_slug():
    query = """
    {
      activeDailyCodingChallengeQuestion {
        question {
          titleSlug
        }
      }
    }
    """
    res = requests.post("https://leetcode.com/graphql", json={"query": query})
    return res.json()['data']['activeDailyCodingChallengeQuestion']['question']['titleSlug']

def get_question_details(slug):
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        content
        difficulty
        sampleTestCase
      }
    }
    """
    res = requests.post("https://leetcode.com/graphql", json={"query": query, "variables": {"titleSlug": slug}})
    return res.json()['data']['question']
