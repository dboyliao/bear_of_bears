# 萬熊之熊裝備最佳器

透過 Telegram Bot 爬取背包裝備，並以整數規劃求解最佳裝備組合。

## 環境建置

本專案使用 [uv](https://docs.astral.sh/uv/) 管理環境與相依套件。

```bash
# 安裝相依套件並建立虛擬環境（.venv）
uv sync

# 執行 cli
uv run bear-of-bears --help
```

Telegram 的 API 資訊可透過環境變數設定，或於執行時依提示輸入。可將以下內容寫入 `.env.local`：

```dotenv
TELEGRAM_API_ID=你的_API_ID
TELEGRAM_API_HASH=你的_API_HASH
```

> API ID 與 API HASH 可在 <https://my.telegram.org> 申請取得。

## `bear-of-bears` CLI

```bash
uv run bear-of-bears [子指令] --help
```

### 子指令 `crawl`

從 Telegram Bot 爬取資料。此指令為一個指令群組，可帶入 Telegram 連線參數：

| 選項 | 說明 | 預設值 |
| --- | --- | --- |
| `--session` | session 名稱 | `bot` |
| `--api-id` | Telegram MTProto API ID（可用環境變數 `TELEGRAM_API_ID`） | 提示輸入 |
| `--api-hash` | Telegram MTProto API HASH（可用環境變數 `TELEGRAM_API_HASH`） | 提示輸入 |

**若已設定好 `.env.local`，則可省略 `--api-id` 與 `--api-hash` 選項。**

#### `crawl inventory`

爬取背包裝備並輸出成 JSON 檔。

```bash
uv run bear-of-bears crawl inventory --output inventory.json
```

| 選項 | 說明 | 預設值 |
| --- | --- | --- |
| `--output` | 輸出檔案路徑 | `inventory.json` |

### 子指令 `optimize-equip`

讀取 `crawl inventory` 輸出的裝備 JSON 檔，計算屬性加權後的最佳裝備組合（每個部位至多選一件）。

```bash
uv run bear-of-bears optimize-equip inventory.json -a 1.0 -d 1.0 -i 1.0
```

| 參數／選項 | 說明 | 預設值 |
| --- | --- | --- |
| `EQUIPMENTS_FILE` | 裝備 JSON 檔路徑（必填） | — |
| `--attack-weight` / `-a` | 攻擊權重 | `1.0` |
| `--defense-weight` / `-d` | 防禦權重 | `1.0` |
| `--intelligence-weight` / `-i` | 智力權重 | `1.0` |

> `dismantle` 指令開發中。

## References

- <https://developers.google.com/optimization/cp/cp_example>
- <https://docs.telethon.dev/en/stable/basic/quick-start.html>
