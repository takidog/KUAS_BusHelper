# KUAS_BusHelper

[t.me/KUAS_BusHelper_bot](tg://resolve?domain=KUAS_BusHelper_bot)



這是一個架在telegram bot上的校車預約服務 (建工以及燕巢的校車)

主要的API是[NKUST-ITC/AP-API](https://github.com/NKUST-ITC/AP-API) ，在這裡再次感謝！



**[注意]**為了方便性，目前第一次執行會需要NKUST的帳號密碼，並**會儲存在伺服器端**

我不太想這麼做，但...沒有辦法，目前儲存用SQLite (人數應該不多，所以先採用這)

雖然這東西很廢QQ 只是滿足我自己，或是周圍不怕死的同學使用

有任何bug歡迎提issuse 或是 buluni.ha@gmail.com 我會盡力的修正



因為需要儲存帳號密碼，其實我蠻希望這東西能給學校架設~~(不敢背鍋的)~~



## 主要功能介紹

**使用以下功能之前，需要先輸入NKUST帳號密碼後，與telegram chat Id 連結**



查詢已預約車次



查詢車次



預約乘車



取消預約



## 自行架設

請參考doc/setup.md裡面的文件!



## 原定的最終目標

~~依照填入的每週固定搭車時間自動預約 (自動部分尚未完成)~~

~~後續架設到Telegram bot 上，方便IOS用戶預約/取消~~



目前學校的查詢車次還是需要登入，如果這樣做可能要把我自己帳號丟下去自動撈資料..

還怕哪天智障幫使用者預約車次，反而害到人QQ

目前先這樣

<br>



## 目前狀態

經過詢問[NKUST-ITC/AP-API](https://github.com/NKUST-ITC/AP-API) 採用MIT授權之後開始製作:P



2018.09.07 剛開始編寫，還有多處肉眼可見bug

先製作出一個簡單的手動預約，以方便後續改建置telegram bot上



2018.09.15 經過一個禮拜的搭乘，目前還沒遇見什麼會導致bug的現實問題!?

移植到telegram bot上，完成 **查詢預約車次**/**查詢車次**/**預約乘車**/**取消預約** 主要功能



<br>

<br>

<br>

#### 題外話

我IOS用戶，但發現學校App好像下架了QQ

so.... 我打算開發到telegram bot 上

不清楚實際搭乘會有什麼狀況

還有很多問題我不清楚，等開學後開始當搭車後開始調整

~~轉學仔沒理解校區的悲歌~~



我以前只開發純推波資訊的telegram bot，開發與bot交談的是第一次

先使用telegram官方的範例做修改~~(魔改)~~，程式碼內還有一些沒用的def沒砍XDD







再次感謝[NKUST-ITC/AP-API](https://github.com/NKUST-ITC/AP-API) 

省了麻煩的一大塊!