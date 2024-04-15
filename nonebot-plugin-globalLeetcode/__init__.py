from nonebot import on_command, require, get_bot, get_driver
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from nonebot_plugin_htmlrender import html_to_pic

from .get_problem_data import *
from .get_user_data import *



request_today = on_command("lc每日",aliases={"lc","leetcode"},priority = 10,block = True)

request_search = on_command("lc查找",aliases={"lc搜索","leetcode搜索"},priority = 10,block = True)

request_random = on_command("lc随机",aliases={"lc随机一题","leetcode随机"},priority = 10,block = True)

request_user = on_command("lc查询",aliases={"lc查询用户","leetcode查询"},priority = 10,block = True)


try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except Exception as e:
    logger.error("[LC查询] require定时插件时出错，请检查插件加载顺序。")




#查询每日一题
@request_today.handle()
async def send_today_problem(bot: Bot,event:Event):
    try:
        today_title = get_today_title()
        logger.info(f"[LC查询] 获取今日题目成功，题目为{today_title}.")
        today_data = get_sub_problem_data(today_title)
        logger.info("[LC查询] 获取题目内容成功。")
        logger.debug(f"[LC查询] 题目{today_data[0]}的难度为{today_data[1]}")
    except Exception as e:
        logger.error("[LC查询] 无法连接至leetcode，请检查网络和网络代理状态。")
        await request_today.finish("连接到leetcode失败...呜呜呜...\n请稍后再试！！")

    pic = await html_to_pic(today_data[4], viewport={"width": 840, "height": 400})
    await request_today.send("获取今日每日一题成功~加油哦ww\n"+"\n".join(today_data[:4])+MessageSegment.image(pic)+f"\n{today_data[5]}")






#搜索题目
@request_search.handle()
async def parse(bot: Bot, event: Event, state: T_State,args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        state["keyword"] = arg


@request_search.got("keyword",prompt="请输出要在leetcode查找的内容哦~\n可为题号、题目、题干内容哒")
async def send_today_problem(bot: Bot,event:Event,  state: T_State):
    try:
        search_title = get_search_title(state["keyword"])
        if search_title:
            logger.info(f"[LC查询] 成功搜索到关键字题目，只取第一条，题目为{search_title}.")
        else:
            logger.info("[LC查询] 搜索成功，但并无相关题目。")
            request_search.finish("未搜索到相关题目！！\n要不...换个关键字再搜索一下吧~可为题号、题目、题干内容哒")

        data = get_sub_problem_data(search_title)
        logger.info("[LC查询] 获取题目内容成功。")
        logger.debug(f"[LC查询] 题目{data[0]}的难度为{data[1]}")
    except Exception as e:
        logger.error("[LC查询] 无法连接至leetcode，请检查网络和网络代理状态。")
        await request_search.finish("连接到leetcode失败...呜呜呜...\n请稍后再试！！")

    pic = await html_to_pic(data[4], viewport={"width": 840, "height": 400})
    await request_search.send("搜索成功~只发送了最相关题目哦ww\n"+"\n".join(data[:4])+MessageSegment.image(pic)+f"\n{data[5]}")






#随机一题
@request_random.handle()
async def send_random_problem(bot: Bot,event:Event):
    try:
        random_title = get_random_title()
        logger.info(f"[LC查询] 获取随机一题题目成功，题目为{random_title}.")
        random_data = get_sub_problem_data(random_title)
        logger.info("[LC查询] 获取题目内容成功。")
        logger.debug(f"[LC查询] 题目{random_data[0]}的难度为{random_data[1]}")
    except Exception as e:
        logger.error("[LC查询] 无法连接至leetcode，请检查网络和网络代理状态。")
        await request_random.finish("连接到leetcode失败...呜呜呜...\n请稍后再试！！")

    pic = await html_to_pic(random_data[4], viewport={"width": 840, "height": 400})
    await request_random.send("成功获取随机一题~加油哦ww\n"+"\n".join(random_data[:4])+MessageSegment.image(pic)+f"\n{random_data[5]}")






#查询用户信息
@request_user.handle()
async def parse(bot: Bot, event: Event, state: T_State,args: Message = CommandArg()):
    arg = args.extract_plain_text()
    if arg:
        state["userSlug"] = arg


@request_user.got("userSlug",prompt="请输出要在leetcode查询的用户哦~\n请写入用户ID，而非用户昵称哦~")
async def send_user_data(bot: Bot,event:Event,  state: T_State):
    try:
        #详细的返回json信息请查阅json/文件夹内的文本，或者参见get_user_data.py
        user_public_profile = get_user_public_profile(state["userSlug"])
        user_question_progress = get_user_question_progress(state["userSlug"])
        user_profile_articles = get_user_profile_articles(state["userSlug"])
        user_medals = get_user_medals(state["userSlug"])
        user_languages = get_user_languages(state["userSlug"])
    except Exception as e:
        logger.error("[LC查询] 无法连接至leetcode，请检查网络和网络代理状态。")
        await request_user.finish("连接到leetcode失败...呜呜呜...\n请稍后再试！！")
    try:
        userSlug = state["userSlug"]
        ranking = user_public_profile["data"]["matchedUser"]["profile"]["ranking"]
        userAvatar = httpx.get(user_public_profile["data"]["matchedUser"]["profile"]["userAvatar"])
        viewCount = user_public_profile["data"]["matchedUser"]["profile"]["postViewCount"]
        solutionCount = user_public_profile["data"]["matchedUser"]["profile"]["solutionCount"]
        reputation = user_public_profile["data"]["matchedUser"]["profile"]["reputation"]
        categoryDiscussCount = user_public_profile["data"]["matchedUser"]["profile"]["categoryDiscussCount"]

        logger.info("[LC查询] user_public_profile数据解析完成")

        acSubmissionNum = user_question_progress["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][0]["count"]
        acSubmissionNum_easy = user_question_progress["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][1]["count"]
        acSubmissionNum_medium = user_question_progress["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][2]["count"]
        acSubmissionNum_hard = user_question_progress["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][3]["count"]
        problemSolvedBeats_easy = user_question_progress["data"]["matchedUser"]["problemsSolvedBeatsStats"][0]["percentage"]
        problemSolvedBeats_medium = user_question_progress["data"]["matchedUser"]["problemsSolvedBeatsStats"][1]["percentage"]
        problemSolvedBeats_hard = user_question_progress["data"]["matchedUser"]["problemsSolvedBeatsStats"][2]["percentage"]
        allQuestionsCount = user_question_progress["data"]["allQuestionsCount"][0]["count"]
        allQuestionsCount_easy = user_question_progress["data"]["allQuestionsCount"][1]["count"]
        allQuestionsCount_medium = user_question_progress["data"]["allQuestionsCount"][2]["count"]
        allQuestionsCount_hard = user_question_progress["data"]["allQuestionsCount"][3]["count"]

        logger.info("[LC查询] user_question_progress数据解析完成")

        if user_medals["data"]["matchedUser"]["badges"]:
            latest_madal_name = user_medals["data"]["matchedUser"]["badges"][0]["name"]
            latest_madal_date = user_medals["data"]["matchedUser"]["badges"][0]["creationDate"]
            latest_madal = f"【最近勋章】  勋章名：{latest_madal_name} |获得时间：{latest_madal_date}\n"
        else:
            latest_madal = ""
        logger.info("[LC查询] user_medals数据解析完成")

        if user_profile_articles["data"]["recentAcSubmissionList"]:
            latest_article_title = f'【最近题解】：{user_profile_articles["data"]["recentAcSubmissionList"][0]["title"]}\n'
        else:
            latest_article_title = ""
        logger.info("[LC查询] user_profile_articles数据解析完成")

        languages = user_languages["data"]["matchedUser"]["languageProblemCount"]
        languagesstr = "|".join([f'{languages[i]["languageName"]}: {languages[i]["problemsSolved"]}/{acSubmissionNum}' for i in range(len(languages))])


    except Exception as e:
        logger.error(e)
        await request_user.finish("解析用户信息出错×\n用户ID错误或不存在，请输入用户ID而非用户昵称哦~")

    await request_user.send(\
        "用户查询数据成功~\n"+\
        MessageSegment.image(userAvatar.read())+\
        f"Username: {userSlug}(Rank: {ranking})\n"+\
        f"Languages: {languagesstr}\n"+\
            "========\n"+\
            f"Easy: {acSubmissionNum_easy}/{allQuestionsCount_easy} Beats: {problemSolvedBeats_easy}%\nMedium: {acSubmissionNum_medium}/{allQuestionsCount_medium} Beats: {problemSolvedBeats_medium}%\nHard: {acSubmissionNum_hard}/{allQuestionsCount_hard} Beats: {problemSolvedBeats_hard}%\nTotal: {acSubmissionNum}/{allQuestionsCount}\n"+
            "========\n"
            f"Views: {viewCount} | Solution: {solutionCount} | Reputation: {reputation} | Discuss: {categoryDiscussCount}\n"+\
            latest_madal+latest_article_title+\
            f"User Page：https://leetcode.com/{userSlug}/")





#定时发送

time_list = get_driver().config.leetcode_inform_time if hasattr(get_driver().config, "leetcode_inform_time") else list()

async def send_leetcode_everyday():
    qq_list = get_bot().config.leetcode_qq_friends if hasattr(get_driver().config, "leetcode_qq_friends") else list()
    group_list = get_bot().config.leetcode_qq_groups if hasattr(get_driver().config, "leetcode_qq_groups") else list()
    try:
        today_title = get_today_title()
        logger.info(f"[LC查询] 获取今日题目成功，题目为{today_title}.")
        today_data = get_sub_problem_data(today_title)
        logger.info("[LC查询] 获取题目内容成功。")
        logger.debug(f"[LC查询] 题目{today_data[0]}的难度为{today_data[1]}")
    except Exception as e:
        logger.error("[LC查询] 无法连接至leetcode，请检查网络和网络代理状态。")
        pass
    pic = await html_to_pic(today_data[4], viewport={"width": 840, "height": 400})
    try:
        for qq in qq_list:
            await get_bot().call_api("send_private_msg",user_id = qq ,message = "获取今日每日一题成功~加油哦ww\n"+"\n".join(today_data[:4])+MessageSegment.image(pic)+f"\n{today_data[5]}")
        for group in group_list:
            await get_bot().call_api("send_group_msg",group_id = group ,message = "获取今日每日一题成功~加油哦ww\n"+"\n".join(today_data[:4])+MessageSegment.image(pic)+f"\n{today_data[5]}")
    except TypeError:
        logger.error("[LC查询] 插件定时发送相关设置有误，请检查.env.*文件。")





try:
    for index, time in enumerate(time_list):
        scheduler.add_job(send_leetcode_everyday, "cron", hour=time["HOUR"], minute=time["MINUTE"], id=f"leetcode_{str(index)}")
        logger.info(f"[LC查询] 新建计划任务成功！！  id:leetcode_{index}，时间为:{time}.")
except TypeError:
    logger.error("[LC查询] 插件定时发送相关设置有误，请检查.env.*文件。")