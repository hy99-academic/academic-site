# 网站维护手册（SOP）

这份手册告诉你：以后想改网站时，**改哪个文件、怎么改、怎么上线、出问题怎么办**。
这个文件只在仓库里，不会出现在网站上。

> 💡 以后如果用别的 AI（ChatGPT 等）帮忙，可以把这份手册连同你要改的文件一起发给它，它就知道网站是怎么搭的了。

---

## 一、每次修改网站的固定流程（最重要）

在 VSCode 里打开 `C:\Dev\academic-site` 文件夹，然后打开终端（Terminal → New Terminal）。

### 第 1 步：先同步最新版本
```
git checkout main
git pull
```
> 每次开始前都要 `git pull`。因为 GitHub 每周一会自动更新论文列表，不先拉取的话，推送时会冲突。

### 第 2 步：打开本地预览
```
hugo server
```
浏览器打开 **http://localhost:1313**。这个终端窗口要一直开着。

### 第 3 步：修改文件
在 VSCode 左边找到要改的文件（见下面"二、文件地图"），改完按 `Ctrl + S` 保存。
浏览器会**自动刷新**，马上就能看到效果。

### 第 4 步：确认没问题后，推送上线
在终端按 `Ctrl + C` 停掉预览（或者新开一个终端），然后：
```
git add .
git commit -m "简单写一下改了什么"
git push
```
（这就是你原来 `common_push.txt` 里的三行，只是把提交说明换成你这次改的内容。）

### 第 5 步：等待上线并检查
1. 打开 GitHub 仓库 → 点上方 **Actions**
2. 等 **"Deploy Hugo site to Pages"** 变成绿色 ✅（大约 1–2 分钟）
3. 打开 yuxihuang.com，按 **`Ctrl + F5`** 强制刷新（浏览器会缓存旧页面，最多 10 分钟）

---

## 二、文件地图：想改什么，就打开哪个文件

| 想改的内容 | 文件 |
|---|---|
| 首页简介、教育经历、工作经历、邮箱 | `content/_index.md` |
| 首页和招生页的两张研究卡片 | `data/research.yaml` |
| Research 页全部内容（研究介绍、项目、代表作） | `content/research/_index.md` |
| 手动添加 / 修改论文 | `data/publications.yaml` |
| 招生页（Prospective Students） | `content/join/_index.md` |
| Beyond 页（剑道、电影） | `content/beyond/_index.md` |
| 照片 | `static/images/` 文件夹 |
| 名字、职位、单位、社交链接、导航栏、首页招生横幅 | `hugo.yaml` |
| 颜色、字体、样式 | `assets/css/extended/custom.css` |

**⚠️ 一般不要动的文件/文件夹：**
- `data/publications_auto.json` —— ORCID 自动生成的，手动改了下周会被覆盖
- `themes/` —— 网站主题
- `layouts/`、`.github/`、`scripts/` —— 网站的"机器部分"，不确定就别动
- `public/` —— 旧的生成文件，不影响线上网站，不用管

---

## 三、常见情况怎么做

### 情况 1：发表了新论文
**大多数情况什么都不用做。** 每周一 GitHub 会自动从你的 ORCID 拉取新论文并更新网站。
前提是：论文已经在你的 ORCID 上，并且公开范围设为 **Everyone**。

**想马上更新，不想等到周一：**
GitHub 仓库 → **Actions** → 左边点 **"Update publications from ORCID"** → 右边 **Run workflow** → 绿色 **Run workflow**。

**论文已接收但还没有 DOI / 不在 ORCID 上：**
打开 `data/publications.yaml`，在 `manual:` 下面复制一段已有的论文，改成新论文的信息。例如：
```yaml
  - type: journal
    authors: "**Huang, Y.**, Luft, J. A., & Smith, A."
    year: "in press"
    title: "Your paper title here"
    venue: "Journal Name"
```
注意：
- 每行前面的空格要和上面的论文**对齐**（用空格，不要用 Tab）
- 你的名字写成 `**Huang, Y.**` 才会加粗
- 文字里有冒号 `:` 的，一定要用英文双引号 `"..."` 包起来
- 等它有了 DOI、ORCID 也拉到了，网站会自动用你手写的这条（不会重复出现）

**某篇论文 ORCID 显示得不对（作者名、标题有小错）：**
在 `data/publications.yaml` 的 `manual:` 里手写一条正确的版本（标题要和原来大致相同）。手写的版本会自动替换掉 ORCID 的版本。

**某篇不想显示在网站上：**
在 `data/publications.yaml` 最下面的 `hide:` 里加上它的 DOI：
```yaml
hide:
  - "10.1080/xxxxxxx"
```

### 情况 2：想在 Research 页加一张"代表作"论文卡片
打开 `content/research/_index.md`，找到 `{{< papers "..." "..." >}}` 这一行，在里面加上论文的 DOI（用英文双引号，空格隔开）。
⚠️ 这篇论文必须**已经写在 `data/publications.yaml` 的 `manual:` 里**，并且 DOI 是**小写字母**，卡片才会出现。

### 情况 3：换一年招生 / 不招生了
"Fall 2027" 出现在 **4 个地方**，要一起改：
1. `hugo.yaml` → `recruiting:` 下面的 `text:`
2. `content/_index.md` → "I am recruiting Ph.D. students for Fall 2027"
3. `content/join/_index.md` → 第一段
4. `content/research/_index.md` → 最下面的 "Fall 2027"

**暂时不招生：**
- 把 `hugo.yaml` 里 `recruiting:` 下面的 `show: true` 改成 `show: false`（首页横幅消失）
- 改掉上面 2–4 里的招生句子

### 情况 4：在 Beyond 页加照片
1. **先压缩照片**：打开 https://squoosh.app ，拖入照片，右边选 MozJPEG、宽度设 1600 左右，下载。目标是每张 **500KB 以下**（手机原图常常 3–5MB，会让网页很慢）。
2. 把照片放进 `static/images/` 文件夹。**文件名用英文、不要有空格**，例如 `Film_005.jpg`。
3. 打开 `content/beyond/_index.md`，在对应的 `<div class="img-pair">` 里面复制一段：
```html
  <figure>
    <img src="/images/Film_005.jpg" alt="简短描述照片内容">
    <figcaption>照片下方显示的说明文字</figcaption>
  </figure>
```
- 电影部分是**两张一排**（`img-pair`）
- 剑道部分是**三张一排**（`img-pair three`）

### 情况 5：换头像
把新照片（建议正方形或竖版，压缩到 200KB 以下）命名为 **`avatar.jpg`**，替换 `static/images/avatar.jpg`。

### 情况 6：改职位、单位、邮箱、社交链接
打开 `hugo.yaml`：
- 左侧边栏的名字、职位、单位：`sidebar:` 下面的 `name`、`role`、`affiliation`
- 社交图标链接：`socialIcons:` 下面每一项的 `url`
- 首页底部的邮箱在 `content/_index.md` 最后一行；招生页的邮件按钮在 `content/join/_index.md` 最后一行

### 情况 7：加 Service（审稿、委员会等）
打开 `content/_index.md`，在 `## Professional Experience` 那一段下面，照着同样的格式加：
```markdown
## Service

- **2026 – Present** · Reviewer, *Journal of Research in Science Teaching*
- **2025** · Program Committee, ICLS 2025
```

---

## 四、出问题了怎么办

### `git pull` 时提示 "Your local changes would be overwritten"
说明你本地有改动还没提交。先提交再拉取：
```
git add .
git commit -m "save my changes"
git pull
```

### `git push` 时提示 "rejected" 或 "fetch first"
说明 GitHub 上有新内容（通常是周一的论文自动更新）。先拉取再推送：
```
git pull --no-edit
git push
```
（`--no-edit` 是为了不让终端里弹出编辑器。如果还是不小心进了一个看不懂的编辑界面，依次按 `Esc`，输入 `:wq`，再按回车就能退出。）

### `git pull` 提示 "CONFLICT"（冲突）
两边改了同一个地方。最简单的办法：
1. 在 VSCode 里打开提示冲突的文件，会看到 `<<<<<<<`、`=======`、`>>>>>>>` 标记
2. VSCode 会在上方显示按钮："Accept Current Change"（保留你的）/ "Accept Incoming Change"（保留 GitHub 上的）/ "Accept Both"
3. 选好后保存，然后：
```
git add .
git commit -m "fix conflict"
git push
```
> 如果冲突的是 `data/publications_auto.json`，选 **Accept Incoming Change**（保留 GitHub 上的）。

### `hugo server` 报红字错误
错误信息里会写**哪个文件、第几行**。最常见的原因：
- YAML 文件（`.yaml`）缩进不对齐、用了 Tab、冒号后面少了空格
- 文字里有冒号或引号，但没有用 `"..."` 包起来
- 删东西时多删或少删了 `{{< ... >}}` 的一部分

按 `Ctrl + Z` 撤销刚才的修改，再一点点重新改，通常就能找到问题。

### GitHub Actions 出现红色 ❌
1. 点进去，再点红色的那一步，看错误信息（和上面 `hugo server` 的错误一样）
2. 在本地用 `hugo server` 重现、修好，再 `git add .` / `git commit` / `git push`

**来不及修、想先恢复上一个版本：**
```
git revert HEAD
git push
```
这会撤销你最近的一次提交，网站恢复原样。

### 网站没有变化
1. 先看 Actions 是否已经绿色 ✅
2. 按 `Ctrl + F5` 强制刷新，或者用无痕窗口打开
3. 还是旧的就再等 10 分钟

### 推送时弹出 GitHub 登录窗口
正常现象，在浏览器里登录 GitHub 授权即可。
⚠️ **永远不要**把 `ghp_` 开头的令牌（token）写进网址或发给任何人。

---

## 五、自动运行的东西（了解即可）

| 什么 | 什么时候 | 做什么 |
|---|---|---|
| Deploy Hugo site to Pages | 每次推送到 `main` | 生成网站并发布到 yuxihuang.com |
| Update publications from ORCID | 每周一 + 你手动点 Run workflow | 从 ORCID 拉论文，有新论文就自动更新网站 |
