import httpx
import json
from nonebot.log import logger



def get_user_public_profile(username):
    '''获取用户公开信息'''
    try:
        get_data = httpx.post("https://leetcode.com/graphql", json={
            "operationName": "userPublicProfile",
            "variables": {
                "username": username
            },
            "query": "query userPublicProfile($username: String!) { matchedUser(username: $username) { contestBadge { name expired hoverText icon } username githubUrl twitterUrl linkedinUrl profile { ranking userAvatar realName aboutMe school websites countryName company jobTitle skillTags postViewCount postViewCountDiff reputation reputationDiff solutionCount solutionCountDiff categoryDiscussCount categoryDiscussCountDiff } } }"
        })
        user_public_data = json.loads(get_data.text)
        return user_public_data
    except Exception as e:
        logger.error("[LC查询] 获取用户公开信息时出错。",e)
        raise e



def get_user_question_progress(username):
    '''获取用户已通过题目'''
    try:
        get_data = httpx.post("https://leetcode.com/graphql", json={
            "operationName": "userProblemsSolved",
            "variables": {
                "username": username
            },
            "query": "query userProblemsSolved($username: String!) { allQuestionsCount { difficulty count } matchedUser(username: $username) { problemsSolvedBeatsStats { difficulty percentage } submitStatsGlobal { acSubmissionNum { difficulty count } } } }"
        })
        user_question_progress = json.loads(get_data.text)
        return user_question_progress
    except Exception as e:
        logger.error("[LC查询] 获取用户已通过题目时出错。",e)
        raise e


def get_user_profile_articles(username):
    '''获取用户最新题解题目'''
    try:
        get_data = httpx.post("https://leetcode.com/graphql", json={
            "operationName": "recentAcSubmissions",
            "variables": {
                "username": username,
                "limit": 15
            },
            "query": "query recentAcSubmissions($username: String!, $limit: Int!) {recentAcSubmissionList(username: $username, limit: $limit) { id title titleSlug timestamp } } "
        })
        user_profile_articles = json.loads(get_data.text)
        return user_profile_articles
    except Exception as e:
        logger.error("[LC查询] 获取用户最新题解时出错。",e)
        raise e


def get_user_medals(username):
    '''获取用户勋章'''
    try:
        get_data = httpx.post("https://leetcode.com/graphql", json={
            "operationName": "userBadges",
            "variables": {
                "username": username
            },
            "query": "query userBadges($username: String!) { matchedUser(username: $username) { badges { id name shortName displayName icon hoverText medal {   slug   config {     iconGif     iconGifBackground   } } creationDate category } upcomingBadges { name icon progress } } } "
        })
        user_medals = json.loads(get_data.text)
        return user_medals
    except Exception as e:
        logger.error("[LC查询] 获取用户勋章信息时出错。",e)
        raise e

def get_user_languages(username):
    try:
        get_data = httpx.post("https://leetcode.com/graphql", json={
            "operationName": "languageStats",
            "variables": {
                "username": username
            },
            "query": " query languageStats($username: String!) { matchedUser(username: $username) { languageProblemCount { languageName problemsSolved } } } "
        })
        user_languages = json.loads(get_data.text)
        return user_languages
    except Exception as e:
        logger.error("[LC查询] 获取用户勋章信息时出错。",e)
        raise e