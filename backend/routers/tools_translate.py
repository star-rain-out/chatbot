from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import asyncio
import io
import base64

router = APIRouter()

class TranslateRequest(BaseModel):
    text: str

@router.post("/do")
async def translate_text(request: TranslateRequest):
    """
    Translate text using Google Translate API via deep-translator library.
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
        # A simple heuristic to decide target language:
        # If it contains Chinese characters, target is English.
        # Otherwise, target is Chinese (Simplified).
        
        has_chinese = any(u'\u4e00' <= c <= u'\u9fff' for c in text)
        
        if has_chinese:
            target_lang = 'en'
            source_lang_name = 'Chinese'
            target_lang_name = 'English'
            tts_lang = 'en'
        else:
            target_lang = 'zh-CN' # deep-translator expects zh-CN for Simplified Chinese
            source_lang_name = 'English'
            target_lang_name = 'Chinese'
            tts_lang = 'zh-cn' # gTTS expects zh-cn

        # Perform translation
        # Run in executor to avoid blocking main thread
        loop = asyncio.get_event_loop()
        
        def do_translate():
            return GoogleTranslator(source='auto', target=target_lang).translate(text)

        translated_text = await loop.run_in_executor(None, do_translate)
        
        # Generate audio if target is Chinese (or we could do it for English too, but user asked for Chinese audio)
        # The user specifically asked: "English translate to Chinese, then TTS to Chinese audio"
        # So we prioritize Chinese TTS.
        
        audio_base64 = None
        if target_lang == 'zh-CN':
            try:
                # Create gTTS object
                tts = gTTS(text=translated_text, lang=tts_lang)
                
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
            "source_language": "auto",
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