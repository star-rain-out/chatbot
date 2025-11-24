from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime, timedelta

router = APIRouter()

class FestivalQuery(BaseModel):
    date: Optional[str] = None  # 查询特定日期的节日
    month: Optional[str] = None  # 查询特定月份的节日
    festival_type: Optional[str] = None  # traditional, ethnic, modern
    region: Optional[str] = None  # 全国性、地区性

# 中国节日数据库
CHINESE_FESTIVALS = {
    "traditional": [
        {
            "name": "春节",
            "english_name": "Spring Festival",
            "date": "农历正月初一",
            "duration": "7天法定假期",
            "description": "中国最重要的传统节日，家庭团圆、辞旧迎新",
            "customs": ["贴春联", "放鞭炮", "吃年夜饭", "拜年", "发红包"],
            "foods": ["饺子", "年糕", "鱼", "汤圆", "春卷"],
            "activities": ["庙会", "花市", "灯会", "舞龙舞狮"],
            "best_cities": ["北京", "西安", "成都", "广州"],
            "travel_impact": "出行高峰，建议提前预订",
            "2025_date": "2025年1月29日"
        },
        {
            "name": "元宵节",
            "english_name": "Lantern Festival",
            "date": "农历正月十五",
            "duration": "1天",
            "description": "春节的结束，赏花灯、猜灯谜、吃元宵",
            "customs": ["赏花灯", "猜灯谜", "吃元宵", "舞龙"],
            "foods": ["元宵", "汤圆"],
            "activities": ["灯会", "焰火表演", "民俗表演"],
            "best_cities": ["南京", "西安", "北京", "苏州"],
            "travel_impact": "短途旅游高峰，灯会周边交通拥堵",
            "2025_date": "2025年2月12日"
        },
        {
            "name": "清明节",
            "english_name": "Qingming Festival",
            "date": "农历三月初一后第15日",
            "duration": "3天法定假期",
            "description": "祭祖扫墓、踏青赏春的传统节日",
            "customs": ["扫墓", "踏青", "放风筝", "植树"],
            "foods": ["青团", "清明粿", "艾草糕"],
            "activities": ["祭祖", "踏青郊游", "风筝节"],
            "best_cities": ["杭州", "苏州", "西安", "洛阳"],
            "travel_impact": "短途出行高峰，踏青景点人流量大",
            "2025_date": "2025年4月4日"
        },
        {
            "name": "端午节",
            "english_name": "Dragon Boat Festival",
            "date": "农历五月初五",
            "duration": "3天法定假期",
            "description": "纪念屈原的传统节日，赛龙舟、吃粽子",
            "customs": ["赛龙舟", "包粽子", "挂艾草", "戴香包"],
            "foods": ["粽子", "咸鸭蛋", "雄黄酒"],
            "activities": ["龙舟竞渡", "包粽子比赛", "民俗表演"],
            "best_cities": ["汨罗", "宜昌", "广州", "苏州"],
            "travel_impact": "水上活动地区游客增多",
            "2025_date": "2025年5月31日"
        },
        {
            "name": "七夕节",
            "english_name": "Qixi Festival",
            "date": "农历七月初七",
            "duration": "1天",
            "description": "中国情人节，牛郎织女相会的浪漫节日",
            "customs": ["观星", "穿针乞巧", "拜织女"],
            "foods": ["巧果", "面条", "瓜果"],
            "activities": ["观星活动", "传统婚礼", "民俗表演"],
            "best_cities": ["西安", "南京", "杭州", "北京"],
            "travel_impact": "情侣出游增多，浪漫场所受欢迎",
            "2025_date": "2025年8月29日"
        },
        {
            "name": "中秋节",
            "english_name": "Mid-Autumn Festival",
            "date": "农历八月十五",
            "duration": "3天法定假期",
            "description": "家庭团圆、赏月、吃月饼的传统节日",
            "customs": ["赏月", "吃月饼", "家人团圆", "提灯笼"],
            "foods": ["月饼", "柚子", "桂花酒", "芋头"],
            "activities": ["赏月晚会", "灯谜活动", "月饼制作"],
            "best_cities": ["杭州", "苏州", "北京", "桂林"],
            "travel_impact": "家庭出游高峰，观月地点热门",
            "2025_date": "2025年10月6日"
        },
        {
            "name": "重阳节",
            "english_name": "Double Ninth Festival",
            "date": "农历九月初九",
            "duration": "1天",
            "description": "登高望远、敬老爱老的传统节日",
            "customs": ["登高", "赏菊", "饮菊花酒", "敬老"],
            "foods": ["重阳糕", "菊花酒", "螃蟹"],
            "activities": ["登山活动", "赏菊展览", "敬老活动"],
            "best_cities": ["北京", "西安", "成都", "南京"],
            "travel_impact": "登山景点游客增多",
            "2025_date": "2025年10月29日"
        }
    ],
    "ethnic": [
        {
            "name": "泼水节",
            "english_name": "Water-Splashing Festival",
            "date": "公历4月中旬",
            "duration": "3-7天",
            "region": "云南西双版纳",
            "description": "傣族新年，互相泼水祝福",
            "customs": ["泼水祝福", "赛龙舟", "放高升", "赶摆"],
            "foods": ["菠萝饭", "烤鱼", "竹筒饭", "热带水果"],
            "activities": ["泼水狂欢", "民俗表演", "赶集活动"],
            "travel_impact": "西双版纳旅游高峰，住宿紧张",
            "2025_date": "2025年4月13-16日"
        },
        {
            "name": "那达慕大会",
            "english_name": "Naadam Festival",
            "date": "公历7-8月",
            "duration": "3-7天",
            "region": "内蒙古",
            "description": "蒙古族传统体育竞技盛会",
            "customs": ["摔跤", "赛马", "射箭", "歌舞表演"],
            "foods": ["手扒肉", "奶制品", "马奶酒", "烤全羊"],
            "activities": ["传统体育比赛", "歌舞表演", "草原旅游"],
            "travel_impact": "内蒙古旅游旺季，草原住宿紧张",
            "2025_date": "2025年7月25-27日"
        },
        {
            "name": "火把节",
            "english_name": "Torch Festival",
            "date": "农历六月二十四",
            "duration": "3天",
            "region": "四川凉山、云南楚雄",
            "description": "彝族传统节日，点燃火把驱邪祈福",
            "customs": "点火把、跳篝火、歌舞比赛",
            "foods": ["坨坨肉", "荞麦饼", "酸菜汤", "米酒"],
            "activities": ["火把游行", "篝火晚会", "歌舞比赛"],
            "travel_impact": "彝族地区旅游高峰",
            "2025_date": "2025年7月29日"
        }
    ],
    "modern": [
        {
            "name": "国庆节",
            "english_name": "National Day",
            "date": "公历10月1日",
            "duration": "7天法定假期",
            "description": "中华人民共和国国庆日，全国性庆祝活动",
            "customs": ["升旗仪式", "阅兵式", "文艺表演", "国庆晚会"],
            "foods": ["国庆面", "生日蛋糕", "各地特色菜"],
            "activities": ["国庆庆典", "旅游观光", "购物促销"],
            "best_cities": ["北京", "上海", "广州", "深圳"],
            "travel_impact": "全年最长假期，全国旅游高峰",
            "2025_date": "2025年10月1-7日"
        },
        {
            "name": "劳动节",
            "english_name": "Labor Day",
            "date": "公历5月1日",
            "duration": "5天法定假期",
            "description": "国际劳动节，劳动者休息日",
            "customs": ["庆祝活动", "表彰劳模", "文艺演出"],
            "foods": ["团聚餐", "地方特色美食"],
            "activities": ["旅游观光", "购物娱乐", "休闲放松"],
            "travel_impact": "小长假旅游高峰",
            "2025_date": "2025年5月1-5日"
        }
    ]
}

@router.post("/query")
async def query_festivals(query: FestivalQuery):
    """查询中国节日信息"""
    if not query.date and not query.month and not query.festival_type:
        return {
            "bot_response": """🎊 中国节庆日历助手

为您提供最全的中国传统节日、民族节日和现代节庆信息！

**🎭 节日类型：**
• **传统节日** - 春节、中秋、端午等千古传承
• **民族节日** - 各少数民族特色庆典
• **现代节庆** - 国庆节、劳动节等法定假日

**🗓️ 查询方式：**
• 按日期查询节日
• 按月份查看节日
• 按类型筛选节日
• 按地区了解特色节日

**🎯 服务内容：**
• 节日起源和意义
• 传统习俗和活动
• 特色美食推荐
• 最佳观赏地点
• 旅游出行建议

请选择查询方式，了解中国丰富的节庆文化！ 🏮""",
            "suggestions": [
                "查询2025年春节时间",
                "端午节有什么习俗",
                "云南民族节日推荐",
                "节假日旅游建议"
            ]
        }

    # 构建查询结果
    result_festivals = []

    if query.festival_type:
        if query.festival_type in CHINESE_FESTIVALS:
            result_festivals.extend(CHINESE_FESTIVALS[query.festival_type])

    if not result_festivals:
        # 如果没有特定类型，返回传统节日
        result_festivals = CHINESE_FESTIVALS["traditional"]

    result_text = f"""🎊 **中国节庆日历**

为您找到相关的节日信息：\n"""

    for i, festival in enumerate(result_festivals[:5], 1):  # 最多显示5个
        result_text += f"""
## {i}. {festival['name']} ({festival['english_name']})

📅 **节日时间：** {festival['date']}
🗓️ **2025年日期：** {festival.get('2025_date', '待计算')}
⏰ **节日时长：** {festival['duration']}

📝 **节日介绍：** {festival['description']}

🎊 **传统习俗：**"""
        for custom in festival['customs']:
            result_text += f"\n  • {custom}"

        result_text += f"\n\n🍜 **特色美食：**"
        for food in festival['foods']:
            result_text += f"\n  • {food}"

        result_text += f"\n\n🎯 **庆祝活动：**"
        for activity in festival['activities']:
            result_text += f"\n  • {activity}"

        if 'best_cities' in festival:
            result_text += f"\n\n🏙️ **最佳观赏城市：** {', '.join(festival['best_cities'])}"

        if 'region' in festival:
            result_text += f"\n📍 **主要地区：** {festival['region']}"

        result_text += f"\n\n⚠️ **旅游提醒：** {festival['travel_impact']}"
        result_text += "\n" + "-" * 60

    result_text += f"""

🎯 **您的查询条件：**
{f"📅 指定日期：{query.date}" if query.date else ""}
{f"📆 指定月份：{query.month}" if query.month else ""}
{f"🎭 节日类型：{query.festival_type}" if query.festival_type else ""}

💡 **旅游小贴士：**
• 节假日期间提前预订交通和住宿
• 了解当地习俗，尊重传统文化
• 准备相机记录精彩瞬间
• 品尝节日特色美食
• 参与当地庆祝活动

需要了解更多节日信息请随时询问！ 🌟"""

    return {
        "bot_response": result_text,
        "query_type": query.festival_type,
        "found_count": len(result_festivals)
    }

@router.post("/calendar")
async def get_festival_calendar():
    """获取年度节日日历"""
    return {
        "bot_response": """🎊 **2025年中国节庆日历**

**📅 传统节日：**
• **春节** - 1月29日 (农历正月初一)
• **元宵节** - 2月12日 (农历正月十五)
• **清明节** - 4月4日
• **端午节** - 5月31日 (农历五月初五)
• **七夕节** - 8月29日 (农历七月初七)
• **中秋节** - 10月6日 (农历八月十五)
• **重阳节** - 10月29日 (农历九月初九)

**🏮 民族节日：**
• **泼水节** - 4月13-16日 (云南)
• **那达慕大会** - 7月25-27日 (内蒙古)
• **火把节** - 7月29日 (四川、云南)

**🎆 现代节庆：**
• **劳动节** - 5月1-5日
• **国庆节** - 10月1-7日

📋 建议收藏这个日历，提前规划您的中国之旅！ 🌟"""
    }

@router.get("/info")
async def get_festival_info():
    """获取节日查询功能介绍"""
    return {
        "bot_response": """🎊 **中国节庆日历助手**

您的专属节庆文化向导，带您体验中国传统节日的魅力！

**🎯 核心功能：**
• **节日查询** - 按日期、类型、地区查询
• **文化介绍** - 节日起源、寓意、习俗
• **美食推荐** - 传统节庆特色食品
• **活动指南** - 庆祝活动和最佳观赏地
• **旅游建议** - 节假出行注意事项

**🎭 节日类型：**
• **传统节日** - 千古传承的文化瑰宝
• **民族节日** - 多元文化的绚丽风采
• **现代节庆** - 法定假日的欢庆时光

**🏮 服务特色：**
• 详细的2025年节日日历
• 传统文化背景介绍
    旅游出行专业建议
    特色美食体验指南
    最佳观赏地点推荐

让您的中国之旅充满文化韵味！ 🌟""",
        "features": [
            "节日时间查询",
            "传统文化介绍",
            "民俗习俗详解",
            "节庆美食推荐",
            "旅游出行建议"
        ],
        "festival_types": ["传统节日", "民族节日", "现代节庆"]
    }
