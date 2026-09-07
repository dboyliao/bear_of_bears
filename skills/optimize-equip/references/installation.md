# 使用 uv 安裝

本專案尚未發布至 PyPI，請從 GitHub 原始碼安裝，不要執行 `uv tool install bear-of-bears`。
安裝本專案需要 uv 與 Git，且可以連線至 GitHub。

## 尚未安裝 uv

先執行 `uv --version`；若可顯示版本，跳過此節。
若找不到指令，依作業系統選擇一種安裝方式，不需要全部執行。

### macOS 與 Linux

使用官方獨立安裝程式：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

若沒有 `curl`，可改用 `wget`：

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

若已使用 Homebrew，也可改用：

```bash
brew install uv
```

### Windows

在 PowerShell 使用官方獨立安裝程式：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

若已使用 WinGet，也可改用：

```powershell
winget install --id=astral-sh.uv -e
```

### 確認環境

官方獨立安裝指令會下載並執行遠端指令碼，執行前可先下載並檢閱內容。
安裝後重新開啟終端機，再確認 uv 與 Git：

```bash
uv --version
git --version
```

若仍找不到 uv，依安裝程式提示確認 `PATH` 設定；此時不能靠尚無法執行的 `uv tool update-shell` 修復。
若缺少 Git，先依 [Git 官方安裝說明](https://git-scm.com/install/)安裝，再繼續。
uv 的獨立安裝方式不需要預先安裝 Python，後續 `--python 3.12` 可在需要時由 uv 自動下載對應版本。

## 安裝命令列工具

若只需要使用命令列工具，可直接從 GitHub 安裝至 uv 管理的獨立環境，不需要先複製儲存庫。
`uv tool install` 直接接受 Git URL，不使用 `--from`；該選項用於 `uv tool run` 或 `uvx`。

執行以下指令安裝並查看說明：

```bash
uv tool install --python 3.12 'git+https://github.com/dboyliao/bear_of_bears.git'
bear-of-bears optimize-equip --help
```

若找不到 `bear-of-bears` 指令，執行 `uv tool update-shell`，再重新開啟終端機。
此安裝方式不需要進入專案目錄，直接執行 `bear-of-bears`，不要加上 `uv run`。

```bash
bear-of-bears optimize-equip '/背包檔案路徑/inventory.json' -a 1 -d 1 -i 1 -g 1
```

## 指定分支、標籤或提交

在 Git URL 後加上 `@版本參照`，即可指定分支、標籤或提交。
執行前，將下列占位文字替換為儲存庫中實際存在的參照：

```bash
uv tool install --python 3.12 'git+https://github.com/dboyliao/bear_of_bears.git@版本參照'
```

若需要固定原始碼版本以重現結果，使用完整的提交雜湊值；分支可能隨後續提交而變動。

## 從原始碼執行

若需要使用專案內的 `uv run` 工作流程，先取得原始碼並安裝相依套件：

```bash
git clone https://github.com/dboyliao/bear_of_bears.git
cd bear_of_bears
uv sync --python 3.12
uv run bear-of-bears optimize-equip --help
```

若已有本機專案，使用該目錄，不要重複複製或覆寫既有檔案。
後續在專案根目錄執行技能中的 `uv run bear-of-bears` 指令。

## 確認安裝

確認說明輸出包含 `optimize-equip` 的背包檔案參數，以及 `-a`、`-d`、`-i`、`-g` 四項權重選項。
若安裝失敗或選項不符，回報實際錯誤並停止，不要改用不存在的 PyPI 發行套件。
安裝與本機裝備最佳化不需要 Telegram 登入；不要為此索取 API 憑證或啟動爬取流程。

## 參考來源

uv 本身的安裝方式依據 [uv 官方安裝文件](https://docs.astral.sh/uv/getting-started/installation/)。
安裝方式與 Git 來源語法依據 [uv 官方工具使用文件](https://docs.astral.sh/uv/guides/tools/#installing-tools)。
指定分支、標籤或提交的語法見[指定其他來源](https://docs.astral.sh/uv/guides/tools/#requesting-different-sources)。
每次安裝後，依照「確認安裝」一節檢查實際可用的指令與選項，不以先前安裝結果代替本次驗證。
