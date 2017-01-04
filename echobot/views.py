from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import urllib.request
from bs4 import BeautifulSoup
url = 'http://www.cwb.gov.tw/V7/forecast/f_index.htm'
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
query = [("桃園","Taoyuan_City"),("基隆","Keelung_City"),("臺北","Taipei_City")\
         ,("新竹","Hsinchu_City"),("新北","New_Taipei_City"),("新竹縣","Hsinchu_County")\
         ,("苗栗","Miaoli_Country"),("臺中","Taichung_City"),("彰化","Changhus_County")\
         ,("南投","Nantou_Country"),("雲林","Yunlin_County"),("嘉義","Chiayi_City")\
         ,("嘉義縣","Chiayi_County"),("宜蘭","Yilan_County"),("花蓮","Hualien_County")\
         ,("臺東","Taitung_County"),("臺南","Tainan_City"),("高雄","Kaohsiung_City")\
         ,("屏東","Pingtung_County"),("連江","Lienchiang_County"),("金門","Kinmen_County")\
         ,("澎湖","Penghu_City"),("台中","Taichung_City"),("台北","Taipei_City")\
         ,("台東","Taitung_County"),("台南","Tainan_City")\
         ]

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    returnString = ""
                    flag = 0
                    # flag表達是否找到天氣資訊，避免重複搜尋
                    # city[0]表示中文輸入關鍵字，city[1]表示英文關鍵字
                    # returnString記錄回復訊息
                    for city in query:
                        if city[0] in event.message.text:
                            html = urllib.request.urlopen(url).read()
                            soup = BeautifulSoup(html,"html.parser")
                            returnString+=city[0]
                            for link in soup.find_all('a'):
                                if city[1] in link.get('href'):
                                    for a in link.find_all('img'):
                                        if "symbol" in a.get('src') and flag == 0:
                                            returnString+=a.get('alt')
                                            flag=1
                    if flag==1 :
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=returnString)
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
