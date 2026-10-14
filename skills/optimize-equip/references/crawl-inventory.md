# 取得背包資料

缺少背包 JSON 或需要更新資料時，使用 `crawl inventory` 從 Telegram 取得裝備。
以下使用已透過 `uv tool install` 安裝的指令；若使用原始碼環境，則在專案根目錄加上 `uv run`。

## 準備與登入

此操作會登入使用者的 Telegram 帳號，並傳送 `/inventory` 給 `BearOfBearsBot`。
代理執行前須取得使用者對此連線操作的明確授權，不得因為缺少檔案就自動爬取。
首次登入可能要求電話號碼、驗證碼及兩步驟驗證密碼，請使用者在自己的終端機操作。
代理不得啟動互動式登入，也不得要求使用者將憑證或驗證碼貼到對話中。

1. 前往 <https://my.telegram.org/apps> 取得 Telegram API ID 與 API HASH，這不是 Bot Token。
2. 在準備存放背包與登入狀態的目錄開啟終端機。
3. 確認輸出檔案尚不存在，或明確同意覆寫後，再執行：

```bash
bear-of-bears crawl inventory --output inventory.json
```

依終端機提示輸入 API ID、API HASH，以及 Telegram 登入資訊。
若檔案已存在且要保留，改用不同名稱，例如 `--output inventory-new.json`。
程式會直接覆寫輸出檔案，不會先詢問。

## 重複使用設定

工具支援 `TELEGRAM_API_ID` 與 `TELEGRAM_API_HASH` 環境變數，也會讀取目前目錄的 `.env.local`。
若希望免除每次輸入 API 資訊，可由使用者自行在本機建立 `.env.local`：

```dotenv
TELEGRAM_API_ID=你的_API_ID
TELEGRAM_API_HASH=你的_API_HASH
```

預設登入狀態儲存為目前目錄的 `bot.session`，可用下列方式指定其他位置或名稱：

```bash
bear-of-bears crawl --session '/登入狀態路徑/bear' inventory --output inventory.json
```

`--session`、`--api-id` 與 `--api-hash` 屬於 `crawl` 選項，必須放在 `inventory` 前面；`--output` 放在其後。
不要將 `.env.local`、登入狀態檔及其附屬檔案提交至 Git 或分享給他人，並避免將憑證直接寫入會留存歷史紀錄的指令。

## 確認結果並最佳化

程式收到符合條件的背包訊息後，會顯示裝備數量、儲存位置並結束連線。
若一直等待回覆，可在使用者終端機按下 Ctrl+C 停止；未取得輸出前不得宣稱爬取成功。
確認產生的 JSON 符合技能要求，且不是空陣列，再執行：

```bash
bear-of-bears optimize-equip inventory.json -a 1 -d 1 -i 1 -g 1
```

目前程式只解析收到的單則符合條件訊息，不會主動翻頁，因此不得保證包含分頁或其他訊息中的所有裝備。
完成後回到技能的驗證與回報流程，不要穿戴或拆解裝備。
