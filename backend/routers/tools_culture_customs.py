from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class CultureQuery(BaseModel):
    region: str
    culture_type: Optional[str] = None  # festival, custom, tradition, art
    season: Optional[str] = None  # spring, summer, autumn, winter

# 模拟文化习俗数据库
CULTURE_DATABASE = {
    "北京": {
        "festival": [
            {
                "name": "春节庙会",
                "description": "传统春节活动，各种小吃、手工艺品、民俗表演",
                "location": "地坛、龙潭湖、厂甸",
                "time": "正月初一到初七",
                "highlights": ["舞龙舞狮", "杂技表演", "传统小吃", "手工艺品"],
                "tips": "人流量大，注意安全，建议错峰出行"
            },
            {
                "name": "中秋赏月",
                "description": "传统中秋节，赏月、吃月饼、家庭团圆",
                "location": "北海公园、颐和园、什刹海",
                "time": "农历八月十五",
                "highlights": ["月亮景观", "传统音乐", "月饼品尝", "花灯展示"],
                "tips": "提前预约门票，携带防蚊用品"
            }
        ],
        "custom": [
            {
                "name": "四合院文化",
                "description": "传统北京民居建筑，体现北方建筑特色",
                "features": "青砖灰瓦、雕梁画栋、内外有别、中轴对称",
                "location": "南锣鼓巷、什刹海地区",
                "etiquette": "进入院落要轻声细语，不要随意拍照"
            },
            {
                "name": "京剧文化",
                "description": "中国传统戏曲艺术，北京的文化名片",
                "elements": "生旦净丑、唱念做打、脸谱艺术、服装道具",
                "venues": "长安大戏院、梅兰芳大剧院",
                "tips": "初次观看可提前了解剧情，尊重演员表演"
            }
        ],
        "tradition": [
            {
                "name": "喝茶文化",
                "description": "老北京的茶馆文化，休闲社交场所",
                "practice": "盖碗茶、茶点搭配、聊天交友、听相声评书",
                "famous_teas": "茉莉花茶、铁观音、普洱茶",
                "venues": "老舍茶馆、吴裕泰茶庄"
            }
        ]
    },
    "四川": {
        "festival": [
            {
                "name": "成都花会",
                "description": "传统花卉展览，展示各种春花",
                "location": "青羊宫、文化公园",
                "time": "农历二月",
                "highlights": ["盆景展示", "花灯表演", "民俗活动", "美食展销"],
                "tips": "春季最佳赏花时节，适合拍照"
            },
            {
                "name": "火锅节",
                "description": "四川火锅文化盛典，各种口味火锅",
                "location": "宽窄巷子、锦里",
                "time": "每年10-11月",
                "highlights": ["火锅比赛", "辣椒展览", "文化演出", "美食体验"],
                "tips": "不吃辣的人也有清汤火锅选择"
            }
        ],
        "custom": [
            {
                "name": "茶馆文化",
                "description": "四川人悠闲生活的代表，慢生活体验",
                "features": "竹椅木桌、盖碗茶、麻将、采耳服务",
                "activities": "聊天、打麻将、看川剧变脸、采耳",
                "famous": "人民公园茶馆、鹤鸣茶社",
                "etiquette": "可以长时间停留，消费不贵"
            },
            {
                "name": "川剧变脸",
                "description": "四川传统戏曲绝活，神秘莫测的变脸艺术",
                "technique": "瞬间变换脸谱，运用机关道具",
                "performance": "配合戏曲动作，音乐节奏",
                "venues": "锦江剧场、蜀风雅韵",
                "tips": "不要拍照录像，尊重表演艺术"
            }
        ]
    },
    "江浙": {
        "festival": [
            {
                "name": "西湖龙井茶节",
                "description": "杭州传统茶文化活动",
                "location": "龙井村、中国茶叶博物馆",
                "time": "每年4月采茶季节",
                "highlights": ["采茶体验", "茶艺表演", "茶道讲座", "茶叶品鉴"],
                "tips": "可参与采茶制茶，学习传统茶艺"
            },
            {
                "name": "苏州园林节",
                "description": "江南园林文化活动",
                "location": "拙政园、留园、网师园",
                "time": "春秋季节最佳",
                "highlights": ["园林游览", "古琴演奏", "书法展示", "诗词朗诵"],
                "tips": "春秋季节景色最美，人相对较少"
            }
        ],
        "custom": [
            {
                "name": "园林文化",
                "description": "江南私家园林，体现文人审美",
                "elements": "假山池塘、亭台楼阁、花草树木、匾额楹联",
                "philosophy": "小中见大、曲径通幽、移步换景",
                "representative": "苏州四大名园、扬州个园"
            },
            {
                "name": "水乡文化",
                "description": "江南水乡特色生活",
                "features": "小桥流水、乌篷船、白墙黑瓦、石板小巷",
                "life": "船运交通、河浜洗菜、桥头聚会、水上集市",
                "famous_towns": "乌镇、西塘、周庄、同里"
            }
        ]
    },
    "广东": {
        "festival": [
            {
                "name": "广府庙会",
                "description": "传统广府文化活动",
                "location": "越秀公园、中山纪念堂",
                "time": "正月十五前后",
                "highlights": ["粤剧表演", "舞狮舞龙", "传统手工艺", "广式美食"],
                "tips": "体验正宗广府文化，品尝传统小吃"
            },
            {
                "name": "端午龙舟节",
                "description": "传统端午节活动",
                "location": "珠江、荔湾湖",
                "time": "农历五月初五",
                "highlights": ["龙舟竞渡", "粽子制作", "民俗表演", "传统美食"],
                "tips": "观看龙舟比赛要注意安全，提前占位"
            }
        ],
        "custom": [
            {
                "name": "早茶文化",
                "description": "广东人特有的饮食习惯",
                "practice": "一盅两件、茶点搭配、报纸聊天、老友聚会",
                "etiquette": "轻叩桌面表示谢意，不大声喧哗",
                "time": "早上6点到11点最佳",
                "famous": "广州酒家、陶陶居、点都德"
            },
            {
                "name": "粤语文化",
                "description": "广东话语言文化和特色表达",
                "features": "九声六调、丰富俚语、歌曲文化、影视影响",
                "greetings": "早晨、你好、多谢、唔该",
                "tips": "学几句基本粤语，当地人会很高兴"
            }
        ]
    }
}

@router.post("/explore")
async def explore_culture(query: CultureQuery):
    """
    探索文化习俗
    """
    region = query.region.strip()

    if not region:
        return {
            "bot_response": """🏮 中国文化习俗探索助手

带您深入了解中国各地的传统文化和民俗风情！

**🎭 文化类型：**
• **节庆活动** - 传统节日和庆典活动
• **民俗习惯** - 地方特色生活方式
• **传统艺术** - 戏曲、工艺、文学艺术
• **建筑文化** - 传统建筑和园林艺术

**🗺️ 文化区域：**
• **北京** - 皇家文化、四合院、京剧
• **四川** - 川剧变脸、茶馆文化、悠闲生活
• **江浙** - 园林艺术、水乡风情、文人文化
• **广东** - 广府文化、粤剧、早茶文化

**🌸 季节特色：**
• 春节 - 庙会、花市、团圆饭
• 端午 - 龙舟、粽子、香包
• 中秋 - 赏月、月饼、花灯
• 重阳 - 登高、菊花、敬老

请告诉我您想了解哪个地区的文化？ 🏛️""",
            "suggestions": [
                "北京的传统节日",
                "四川的茶馆文化",
                "江南园林艺术",
                "广东早茶文化"
            ]
        }

    # 查找区域文化
    region_culture = None
    culture_region = None

    # 精确匹配
    if region in CULTURE_DATABASE:
        region_culture = CULTURE_DATABASE[region]
        culture_region = region
    else:
        # 模糊匹配
        for db_region, culture_info in CULTURE_DATABASE.items():
            if region in db_region or db_region in region:
                region_culture = culture_info
                culture_region = db_region
                break

    if not region_culture:
        return {
            "bot_response": f"""🏮 文化探索结果

❌ **暂未找到该地区的文化信息**

**搜索地区：** {region}

**可能的原因：**
• 该地区暂时不在文化数据库中
• 地区名称可能需要调整

**🌟 当前覆盖地区：**
• **北京** - 皇家文化、传统习俗
• **四川** - 巴蜀文化、悠闲生活
• **江浙** - 江南文化、园林艺术
• **广东** - 广府文化、粤式生活

**💡 建议：**
• 使用标准地区名称查询
• 选择上述文化区域深入了解
• 可询问特定文化类型的信息

需要其他地区文化信息请告知 🔄""",
            "available_regions": list(CULTURE_DATABASE.keys())
        }

    # 筛选文化类型
    cultural_items = []

    if query.culture_type:
        if query.culture_type in region_culture:
            cultural_items = region_culture[query.culture_type]
        else:
            available_types = list(region_culture.keys())
            return {
                "bot_response": f"""🏮 文化探索结果

❌ **该地区暂无此类文化信息**

**地区：** {culture_region}
**文化类型：** {query.culture_type}

**可用文化类型：**
• {' • '.join(available_types)}

请选择其他文化类型重新查询 🔄""",
                "region": culture_region,
                "available_types": available_types
            }
    else:
        # 推荐所有类型
        for culture_type, items in region_culture.items():
            cultural_items.extend(items)

    if not cultural_items:
        return {
            "bot_response": f"""🏮 文化探索结果

📍 **地区：** {culture_region}
❌ **没有找到相关的文化信息**

**您的查询条件：**
{f"🎭 文化类型：{query.culture_type}" if query.culture_type else ""}
{f"🌸 季节特色：{query.season}" if query.season else ""}

需要我为您推荐该地区的所有文化信息吗？ 🤔""",
            "region": culture_region
        }

    # 构建结果
    result_text = f"""🏮 **{culture_region}文化习俗探索**

为您找到了 **{len(cultural_items)}** 项文化内容：\n"""

    for i, item in enumerate(cultural_items, 1):
        result_text += f"""
## {i}. {item['name']}

📝 **文化介绍：** {item['description']}"""

        if "location" in item:
            result_text += f"\n📍 **活动地点：** {item['location']}"

        if "time" in item:
            result_text += f"\n⏰ **时间安排：** {item['time']}"

        if "highlights" in item:
            result_text += f"\n✨ **特色亮点：**"
            for highlight in item['highlights']:
                result_text += f"\n  • {highlight}"

        if "features" in item:
            result_text += f"\n🏛️ **文化特征：** {item['features']}"

        if "activities" in item:
            result_text += f"\n🎯 **主要活动：** {item['activities']}"

        if "etiquette" in item:
            result_text += f"\n📜 **注意事项：** {item['etiquette']}"

        if "tips" in item:
            result_text += f"\n💡 **参观贴士：** {item['tips']}"

        result_text += "\n" + "-" * 50

    result_text += f"""

**🎭 您的文化兴趣：**
{f"🏛️ 文化地区：{culture_region}" if culture_region else ""}
{f"🎪 文化类型：{query.culture_type}" if query.culture_type else ""}
{f"🌸 季节偏好：{query.season}" if query.season else ""}

**🎯 文化体验建议：**
• 尊重当地文化习俗和传统
• 主动了解文化背景和历史渊源
• 参与文化活动时遵守相关规定
• 拍照前询问是否允许
• 保持礼貌，与当地人友好交流

让我们一起探索中国传统文化的魅力！ 🌟"""

    return {
        "bot_response": result_text,
        "region": culture_region,
        "found_items": len(cultural_items)
    }

@router.get("/popular")
async def get_popular_cultures():
    """
    获取热门文化习俗
    """
    all_cultures = []
    for region, culture_info in CULTURE_DATABASE.items():
        for culture_type, items in culture_info.items():
            for item in items:
                culture_data = {
                    "name": item["name"],
                    "region": region,
                    "type": culture_type,
                    "description": item["description"]
                }
                all_cultures.append(culture_data)

    return {
        "bot_response": """🏮 **中国文化习俗大全**

为您介绍中国各地的传统文化和民俗风情：

**🏛️ 皇城文化（北京）：**
• 春节庙会 - 传统民俗表演和美食
• 四合院文化 - 传统建筑和生活习俗
• 京剧艺术 - 国粹戏曲表演
• 中秋赏月 - 传统家庭团聚活动

**🐼 巴蜀文化（四川）：**
• 茶馆文化 - 悠闲生活体验
• 川剧变脸 - 神秘的戏曲绝技
• 火锅节 - 四川美食文化盛典
• 成都花会 - 传统花卉展览

**🏞️ 江南文化（江浙）：**
• 园林艺术 - 文人审美和建筑智慧
• 水乡风情 - 小桥流水人家的生活
• 龙井茶文化 - 传统茶艺和品鉴
• 园林节 - 江南园林文化活动

**🌺 广府文化（广东）：**
• 早茶文化 - 广式生活和饮食习惯
• 粤剧艺术 - 传统戏曲和音乐
• 端午龙舟 - 水上竞技和民俗活动
• 广府庙会 - 传统庆典和文化展示

**💡 文化体验建议：**
• 参与当地传统节日活动
• 学习基础文化礼仪和习俗
• 品尝地方特色美食
• 参观历史文化景点
• 与当地人交流了解生活文化

选择地区即可深入了解具体文化内容！ 🎭""",
        "popular_cultures": all_cultures
    }

@router.get("/info")
async def get_culture_info():
    """
    获取文化探索功能介绍
    """
    return {
        "bot_response": """🏮 **中国文化习俗探索助手**

您的专属文化向导，带您深入体验中国传统文化！

**🎯 服务特色：**
• **深度文化介绍** - 详细的历史背景和文化内涵
• **民俗活动指导** - 参与传统节庆的实用建议
• **文化礼仪教学** - 了解和尊重当地习俗
• **最佳体验推荐** - 时间、地点、注意事项
• **互动体验机会** - 参与各种文化活动

**🏛️ 文化分类：**
• **节庆文化** - 传统节日和庆典活动
• **民俗习惯** - 地方特色生活方式
• **传统艺术** - 戏曲、工艺、表演艺术
• **建筑文化** - 古建筑、园林、民居

**🗺️ 文化区域覆盖：**
• **华北地区** - 皇家文化、京城习俗
• **西南地区** - 巴蜀文化、民族风情
• **华东地区** - 江南文化、园林艺术
• **华南地区** - 广府文化、海洋文化

**💡 文化体验贴士：**
1. 尊重当地文化传统和宗教信仰
2. 学习基本的文化礼仪和禁忌
3. 主动参与但要保持适当的距离
4. 拍照前征求允许，保护文化遗产
5. 品尝当地美食，了解饮食文化

让您的中国之旅成为深度的文化探索之旅！ 🌟""",
        "features": [
            "文化习俗介绍",
            "节庆活动推荐",
            "传统文化体验",
            "文化礼仪指导",
            "最佳参观建议"
        ],
        "culture_types": ["节庆活动", "民俗习惯", "传统艺术", "建筑文化"],
        "covered_regions": list(CULTURE_DATABASE.keys())
    }
