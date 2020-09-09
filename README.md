# KUAS_BusHelper

[t.me/KUAS_BusHelper_bot](t.me/KUAS_BusHelper_bot)(2018.11.13 關閉服務)



這是一個架在telegram bot上的校車預約服務 (建工以及燕巢的校車)

主要的API是[NKUST-ITC/AP-API](https://github.com/NKUST-ITC/AP-API) ，在這裡再次感謝！



**[注意]** 為了方便性，目前第一次執行會需要NKUST的帳號密碼，並 **會儲存在伺服器端**

有任何bug歡迎提issuse

## 主要功能介紹

**使用以下功能之前，需要先輸入NKUST帳號密碼後，與telegram chat Id 連結**



查詢已預約車次

![](https://raw.githubusercontent.com/takidog/img_library/master/KUAS_BusHelprt/1.gif)

查詢車次

![](https://raw.githubusercontent.com/takidog/img_library/master/KUAS_BusHelprt/2.gif)

預約乘車

![](https://raw.githubusercontent.com/takidog/img_library/master/KUAS_BusHelprt/3.gif)

取消預約

![](https://raw.githubusercontent.com/takidog/img_library/master/KUAS_BusHelprt/4.gif)

## 自行架設

請參考doc/setup.md裡面的文件!





## 目前狀態

經過詢問[NKUST-ITC/AP-API](https://github.com/NKUST-ITC/AP-API) 採用MIT授權之後開始製作:P

2018.11.13

關閉服務

修正上一版的時間計算錯誤



2018.10.16

修正伺服器回傳過去時間的預約記錄



2018.09.07 

剛開始編寫，還有多處肉眼可見bug

先製作出一個簡單的手動預約，以方便後續改建置telegram bot上



2018.09.15 

經過一個禮拜的搭乘，目前還沒遇見什麼會導致bug的現實問題!?

移植到telegram bot上，完成 **查詢預約車次**/**查詢車次**/**預約乘車**/**取消預約** 主要功能

2018.09.17 

修正SQL injection 。

更新README.md  demo image URL


<br>

<br>

<br>



再次感謝[NKUST-ITC/AP-API](https://github.com/NKUST-ITC/AP-API) 

