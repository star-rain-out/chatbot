from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from googletrans import Translator
from gtts import gTTS
import asyncio
import io
import base64

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str

# Initialize translator
translator = Translator()

@router.post("/do")
async def translate_text(request: TranslateRequest):
    """
    Translate text using Google Translate API via googletrans library.
    Automatically detects language and translates to the other (Chinese <-> English).
    """
    text = request.text.strip()

    if not text:
        return {
            "bot_response": """🌐 Translation Assistant

Please enter text you want to translate. I can translate between Chinese and English.

For example:
• "Hello world"
• "你好世界"
""",
            "suggestions": ["Hello", "你好", "Good morning"]
        }

    try:
        # Detect language
        # googletrans detection can be a bit slow, so we can try to infer from characters first for speed,
        # but for accuracy let's let google handle it or just try to translate to English first, 
        # if it's already English, translate to Chinese.
        
        # A simple heuristic to decide target language:
        # If it contains Chinese characters, target is English.
        # Otherwise, target is Chinese (Simplified).
        
        has_chinese = any(u'\u4e00' <= c <= u'\u9fff' for c in text)
        
        if has_chinese:
            target_lang = 'en'
            source_lang_name = 'Chinese'
            target_lang_name = 'English'
        else:
            target_lang = 'zh-cn'
            source_lang_name = 'English'
            target_lang_name = 'Chinese'

        # Perform translation
        # Run in executor because googletrans might be blocking
        loop = asyncio.get_event_loop()
        translation = await loop.run_in_executor(None, lambda: translator.translate(text, dest=target_lang))
        
        translated_text = translation.text
        
        # Generate audio if target is Chinese
        audio_base64 = None
        if target_lang == 'zh-cn':
            try:
                # Create gTTS object
                tts = gTTS(text=translated_text, lang='zh-cn')
                
                # Save to memory buffer
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                
                # Convert to base64
                audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
            except Exception as e:
                print(f"TTS error: {e}")

        response_text = f"""🌐 Translation Assistant

👉 {source_lang_name} to {target_lang_name}

**Original**:
{text}

**Translation**:
{translated_text}
"""

        return {
            "bot_response": response_text,
            "original_text": text,
            "translated_text": translated_text,
            "source_language": translation.src,
            "target_language": target_lang,
            "audio_base64": audio_base64
        }

    except Exception as e:
        print(f"Translation error: {e}")
        return {
            "bot_response": f"""🌐 Translation Assistant

❌ Translation failed. 
Error: {str(e)}

Please try again later or try a different text.""",
            "original_text": text,
            "error": str(e)
        }