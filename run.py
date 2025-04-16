from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx

app = FastAPI()

@app.get("/stream")
async def proxy_stream():
    STREAM_URL = "https://fi.okarisa.cfd/hls/FFR.m3u8"
    HEADERS = {
        "Referer": "http://www.fawanews.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Origin": "http://www.fawanews.com"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(STREAM_URL, headers=HEADERS)
        return StreamingResponse(response.iter_bytes(), media_type=response.headers["Content-Type"])
