	github：https://github.com/RonRonRonRon/linechot
	加入好友的連結：https://line.me/R/ti/p/%40pnf0968d

	將code push到heroku上，設定相關環境變數（LINE_CHANNEL_ACCESS_TOKEN、DISABLE_COLLECTSTATIC=1、LINE_CHANNEL_SECRET、SECRET_KEY），即可運作。

	加bot好友之後，可以輸入縣市關鍵字：台中、台南，也可以用整句敘述，如：「台中今天天氣如何？」bot會在處理後回答。若bot搜尋不到關鍵字，將會echo使用者所說的話。

	此作業使用heroku作為伺服器，所以有requirement.txt、procfile（助教網站上似乎誤植成profile）告知該安裝哪些library、如何執行，變數也存於heroku的settings中，故可使github上不被瀏覽重要的secret sky。

	此前也先使用過ngrok做為測試版本的伺服器，除了secret……變數寫在settings.py中與heroku版本並無太大的差異，故不贅述。

	在天氣抓取方面，我直接使用urllib抓取氣象局資料，使用BeautifulSoup4進行parsing，觀察後抓取了a、img等tag，最後獲得資料，處理字串，返回其值。

	