Ptt表特版爬圖(網址)程式



至Ptt表特版，搜尋標題為 [正妹] 的標題，進入後將圖片網址存入Google sheets內。

程式上傳至heroku雲端,運用APScheduler套件在雲端每日12時執行程式(台灣時間20:00)，自動更新Google sheets內的圖片。

用Google Apps Script連結line developer，當linebot接收到特定字'抽'時會啟動app,至已存好的Google sheets內隨機抽取圖片網址並回傳給linebot。

