from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import requests
import os

router = APIRouter()

# ================= 配置区 =================
# 请将你的 SerpApi Key 填入环境变量或直接替换下方的字符串
# 注册地址: https://serpapi.com/
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "416c3f455698c1a4f445e5afc78980a9ed90428e700aae4cc25f18e0c0b9377d") 
# ==========================================

class ImageSearchRequest(BaseModel):
    query: str

class ImageResult(BaseModel):
    url: str
    thumbnail: str
    title: str  # 增加标题字段方便展示
    source: str # 增加来源字段

@router.post("/search")
async def search_images(request: ImageSearchRequest):
    """
    Search for images using Google Images via SerpApi
    Returns 3 real images related to the search query
    """
    
    if not request.query or not request.query.strip():
        return {
            "bot_response": """🖼️ **Image Search**

Welcome to Image Search! I can find beautiful images of landmarks, places, and attractions for you.

**How to use:**
Just tell me what you want to see, for example:
• "Great Wall"
• "Eiffel Tower"
• "Mount Fuji"
• "Taj Mahal"

I'll show you high-quality images found on Google! 📸""",
            "images": []
        }
    
    query = request.query.strip()
    
    # 检查 API Key 是否配置
    if "你的_SERPAPI_KEY" in SERPAPI_KEY or not SERPAPI_KEY:
        print("⚠️ 警告: SerpApi Key 未配置，请在代码中填写。")
        # 这里你可以选择抛出错误，或者降级回原来的 demo 模式
        # 为了演示，我们先抛出错误提示
        raise HTTPException(status_code=500, detail="SerpApi Key not configured on server.")

    try:
        # SerpApi Google Images 参数构建
        # 文档: https://serpapi.com/images-results
        params = {
            "engine": "google_images",
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 5,        # 请求前 5 张图，防备有些图链接失效
            "safe": "active" # 开启安全搜索
        }

        print(f"DEBUG: Searching Google Images for '{query}'...")
        
        # 发送请求
        response = requests.get("https://serpapi.com/search", params=params, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"SerpApi Error: {response.status_code} - {response.text}")

        data = response.json()
        
        # 解析结果
        # SerpApi 返回的图片列表在 'images_results' 字段中
        results = data.get("images_results", [])
        
        if not results:
            return {
                "bot_response": f"😔 I couldn't find any images for **{query}**.",
                "images": [],
                "query": query
            }

        # 提取前 3 张图片
        final_images = []
        for img in results[:3]:
            final_images.append({
                "url": img.get("original"),         # 原图 URL
                "thumbnail": img.get("thumbnail"),  # 缩略图 URL
                "title": img.get("title", query),   # 图片标题
                "source": img.get("source", "Google Images")
            })

        response_text = f"""🖼️ **Image Search Results for "{query}"**

I found {len(final_images)} images for you using Google Search! 🌏

📸 **Here are the top results:**
"""
        
        return {
            "bot_response": response_text,
            "images": final_images,
            "query": query
        }
        
    except Exception as e:
        print(f"❌ Error searching images: {str(e)}")
        # 生产环境中建议记录日志而不是直接返回详细错误给前端
        raise HTTPException(status_code=500, detail=f"An error occurred while searching: {str(e)}")

@router.get("/info")
async def get_image_search_info():
    """
    Get information about the image search feature
    """
    return {
        "bot_response": """🖼️ **Real-time Image Search**

I can help you find beautiful images of any landmark, place, or attraction using Google Images!

**How it works:**
1. Tell me what you want to see (e.g., "Great Wall", "Eiffel Tower")
2. I'll search Google in real-time and show you the best results.
3. Perfect for finding references or travel inspiration!

**Popular searches:**
• Famous landmarks (Great Wall, Taj Mahal)
• Natural wonders (Grand Canyon, Northern Lights)
• Cute animals (Golden Retriever, Pandas)
• Concepts (Cyberpunk city, Minimalist office)

What would you like to see today? 🌍✨"""
    }