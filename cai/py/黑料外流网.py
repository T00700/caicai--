# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
sys.path.append('..')
xurl = "https://xn--l2xp81b1lj.hlwlw010.com"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}
class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        res = requests.get(xurl, headers=headerx, timeout=20, allow_redirects=False)
        res.encoding = "utf-8"
        res = res.text
        doc = BeautifulSoup(res, "html.parser")
        result = {}
        result['class'] = []

        vodss = doc.find('div', id="youmu")
        vods = vodss.find_all('a')
        for vod in vods:
            id = vod['href'].replace('.html', "")
            if 'http' in id or id == '/':
                continue
            name = vod.text
            if not any(d['type_name'] == name for d in result['class']):
                result['class'].append({'type_id': id, 'type_name': name})
        return result

    def homeVideoContent(self):
        videos = []
        try:
            detail = requests.get(url=xurl, headers=headerx)
            detail.encoding = "utf-8"
            doc = BeautifulSoup(detail.text, "html.parser")

            soup = doc.find_all('ul', class_="thumbnail-group clearfix")
            for vods in soup:
                sourcediv = vods.find_all('li')

                for item in sourcediv:
                    name = item.select_one("div h5 a").text
                    if "[" in name or "]" in name:
                        name = name.replace("[", "").replace("]", "")
                    if "'" in name:
                        name = name.replace("'", "")
                    id = xurl + item.select_one("div h5 a")["href"]
                    if 'http' in item.select_one("div h5 a")["href"]:
                        continue
                    pic = item.select_one("a img ")["src"]
                    remark = item.select_one("div p").text
                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark
                    }
                    videos.append(video)
                result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if not pg:
            pg = 1

        videos = []
        try:

            res = requests.get(xurl + cid + '/page/' + str(pg) + '.html', headers=headerx)
            res.encoding = "utf-8"
            doc = BeautifulSoup(res.text, "html.parser")
            soup = doc.find('ul', class_="thumbnail-group clearfix")
            sourcediv = soup.find_all('li')
            for item in sourcediv:
                name = item.select_one("div h5 a").text
                if "[" in name or "]" in name:
                    name = name.replace("[", "").replace("]", "")
                if "'" in name:
                    name = name.replace("'", "")
                id = xurl + item.select_one("div h5 a")["href"]
                if 'http' in item.select_one("div h5 a")["href"]:
                    continue
                pic = item.select_one("a img ")["src"]
                remark = item.select_one("div p").text
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                }
                videos.append(video)

        except:
            pass

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        videos = []
        result = {}
        res = requests.get(did, headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r'<li><a href="(.*?)" title="正片">立即播放', res.text)

        if match:
            purl = match.group(1)

        videos.append({
            "vod_id": '',
            "vod_name": '',
            "vod_pic": "",
            "type_name": "ぃぅおか🍬 คิดถึง",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": "",
            "vod_play_from": "直链播放",
            "vod_play_url": purl
        })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        res = requests.get(xurl + id, headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r'\},"url":"(.*?)"', res.text)

        if match:
            purl = match.group(1).replace('\\', '')
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = purl
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, page):
        # https://yaselulu.autos/?s=%E6%88%91%E7%9A%84&paged=2

        result = {}
        videos = []
        if not page:
            page = 1

        res = requests.post(xurl + '/index.php/vod/search/page/' + str(page) + '/wd/' + key + '.html', headers=headerx)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        soup = doc.find('ul', class_="thumbnail-group clearfix")
        sourcediv = soup.find_all('li')
        for item in sourcediv:
            name = item.select_one("div h5 a").text
            if "[" in name or "]" in name:
                name = name.replace("[", "").replace("]", "")
            if "'" in name:
                name = name.replace("'", "")
            id = xurl + item.select_one("div h5 a")["href"]
            if 'http' in item.select_one("div h5 a")["href"]:
                continue
            pic = item.select_one("a img ")["src"]
            remark = item.select_one("div p").text
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            }
            videos.append(video)

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result
    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')



    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None
