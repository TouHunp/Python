# Python AI youtube
通過鎖定單一頻道，抓取其最新30則影片的點閱數以及點讚數。
來推斷出何種影片類型相對較受觀眾青睞。


透過YouTube Data API : https://developers.google.com/youtube/v3/docs
在官方API文件內可以查詢各種資源及各種請求方法。

![image](https://user-images.githubusercontent.com/114973441/198531939-c3340f00-dd57-499b-98f4-384a33b48f45.png)

使用channels路徑來取得，需帶上"id"、"key"、"part"等查詢參數。
id 代表頻道 ID；key 代表我們的 API Key；part 代表想取得的資源屬性。

![image](https://user-images.githubusercontent.com/114973441/198532189-0a89a7a7-4e60-4f92-91bf-60bac13a5b51.png)

使用playlistItems路徑來取得，需帶上"playlistId"、"key"、"part"等查詢參數。
playlistId 代表播放列表 ID；key 代表我們的 API Key；part 代表想取得的資源屬性。
要抓此頻道上傳影片，所以 playlistId 帶入上一步抓到的"上傳影片"清單的 ID。

![image](https://user-images.githubusercontent.com/114973441/198532473-568332d6-d064-45f6-8423-1ebdcac6b836.png)

使用videos路徑來取得，需帶上"id"、"key"、"part"等查詢參數。
id 代表影片 ID；key 代表我們的 API Key；part 代表想取得的資源屬性。

![image](https://user-images.githubusercontent.com/114973441/198532578-cc7430c5-0e33-4a98-8610-aec4cd58428d.png)

將上述抓取的資料呼叫出來，以及建立資料集將資料存入。

![image](https://user-images.githubusercontent.com/114973441/198532695-daa7f52b-e163-4296-931f-21beae5f2508.png)

使用基因演算法，經由最佳化得出解—評分最高的影片。

![image](https://user-images.githubusercontent.com/114973441/198532965-9147e7ab-53fc-41da-b04f-46a9da306dde.png)

結果顯示出一筆最優秀影片，利用分數確認影片內容
可以看出分數比起其他影片是高了幾倍之多，並且點閱數略高但沒有差距非常大
可以看出除了平時的遊戲影片，偶爾的日常內容是非常好的決策。

![image](https://user-images.githubusercontent.com/114973441/198533037-6cc8b462-a0b5-46fd-9cbe-12387ee69e53.png)



