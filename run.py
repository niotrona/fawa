from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
import httpx
import re
import urllib.parse

main_app = FastAPI()

# Headers used for both .m3u8 and .key requests
CUSTOM_HEADERS = {
    "Referer": "http://www.fawanews.com/",
    "Origin": "http://www.fawanews.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

@main_app.get("/mediaflow-proxy")
async def media_proxy(url: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=CUSTOM_HEADERS, timeout=15.0)
            content_type = resp.headers.get("content-type", "")

            # Handle and rewrite .m3u8 playlist
            if "application/vnd.apple.mpegurl" in content_type or url.endswith(".m3u8"):
                playlist = resp.text

                # Replace EXT-X-KEY URI with our own key-proxy route
                modified = re.sub(
                    r'URI="(.*?)"',
                    lambda m: f'URI="/key-proxy?url={urllib.parse.quote(m.group(1), safe="")}"',
                    playlist
                )
                return Response(modified, media_type="application/vnd.apple.mpegurl")

            # For media segments (.ts, etc.)
            return StreamingResponse(iter([resp.content]), media_type=content_type)

    except Exception as e:
        return {"error": str(e)}

# Handles key file downloads with headers injected
@main_app.get("/key-proxy")
async def key_proxy(url: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=CUSTOM_HEADERS, timeout=10.0)
            return Response(content=resp.content, media_type="application/octet-stream")
    except Exception as e:
        return {"error": str(e)}
