from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx

main_app = FastAPI()

@main_app.get("/mediaflow-proxy")
async def proxy(request: Request, url: str):
    headers = {
        "Referer": "http://www.fawanews.com/",
        "Origin": "http://www.fawanews.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=15.0)
            return StreamingResponse(
                iter([resp.content]),
                media_type=resp.headers.get("content-type", "application/vnd.apple.mpegurl")
            )
    except Exception as e:
        return {"error": str(e)}
