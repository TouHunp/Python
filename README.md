# Python AI youtube
通過鎖定單一頻道，抓取其最新30則影片的點閱數以及點讚數。
來推斷出何種影片類型相對較受觀眾青睞。


透過YouTube Data API : https://developers.google.com/youtube/v3/docs
在官方API文件內可以查詢各種資源及各種請求方法。

![image](https://user-images.githubusercontent.com/114973441/198531939-c3340f00-dd57-499b-98f4-384a33b48f45.png)

使用channels路徑來取得，需帶上"id"、"key"、"part"等查詢參數。
id 代表頻道 ID；key 代表我們的 API Key；part 代表想取得的資源屬性。

![image](https://user-images.githubusercontent.com/114973441/198532189-0a89a7a7-4e60-4f92-91bf-60bac13a5b51.png)

