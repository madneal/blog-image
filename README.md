# blog-image

博客图床仓库：**GitHub + jsDelivr**。

仓库：`madneal/blog-image` · 默认分支：`main`

## 链接格式

```text
https://cdn.jsdelivr.net/gh/madneal/blog-image@main/<路径>
```

示例：

```markdown
![cover](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/post-covers/gshark-0a91e37472.jpg)
```

## 目录结构

| 路径 | 来源 | 说明 |
|------|------|------|
| `images/post-covers/` | `madneal/blog` → `static/img/post-covers/` | 文章封面 |
| `images/recovered/` | `static/img/recovered/` | 正文历史配图 |
| `images/au9999-gold-trend/` | `static/img/au9999-gold-trend/` | 专题图 |
| `images/icons/` | `static/icons/` | 站点图标集 |
| `images/site/` | `static/` 根目录 | favicon 等 |
| `images/assets/` | `assets/img/` | 头像 / 微信等 |
| `images/external/` | 正文外链备份 | 从 loli / postimg / medium / github 等抓取 |
| `LOCAL-MAP.tsv` | — | 本地路径 → CDN 映射 |
| `MIGRATION-MAP.tsv` | — | 外链 URL → 备份路径 / 失败原因 |

## 从 blog 迁移说明

1. **本地图**：完整镜像 `static/img/*`、`static/icons`、`assets/img` 与站点根图标。
2. **外链图**：备份易失效图床（loli、postimg、七牛旧链、sm.ms 等）及 GitHub/Medium 等引用图。
3. 部分外链已 404 / DNS 失效，见 `MIGRATION-MAP.tsv` 中 `fail:` 行。

### 博客内相对路径对应 CDN

| 博客路径 | CDN |
|----------|-----|
| `/img/post-covers/xxx.jpg` | `https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/post-covers/xxx.jpg` |
| `/img/recovered/xxx.jpg` | `https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/recovered/xxx.jpg` |

## 上传新图

### 优化上传（推荐）

安装 Python 3 和 WebP 命令行工具（macOS：`brew install webp`）。在本仓库运行：

```bash
python3 upload-optimized.py --push /absolute/path/screenshot.png
python3 upload-optimized.py --cover --push /absolute/path/cover.jpg
```

正文图转换为 WebP；GIF 保留动画，已有 WebP 直接复用。封面另外生成 320px、720px 版本，供博客响应式加载。输出为可复制的 CDN URL。

文件存储在 `images/optimized/content/` 或 `images/optimized/covers/`，名称取自图片内容哈希。新图片生成新地址，旧地址持续有效，勿覆盖或删除已引用文件。`--push` 要求 main 分支且工作区干净，会先同步远端，再提交和推送。省略 `--push` 可仅准备图片并检查结果。

将封面的完整 URL 写入博客 `cover` 字段，博客模板会自动使用对应的 `-320.webp` 和 `-720.webp`。其他来源封面仍按原 URL 加载。

原 PicGo 上传方式继续可用；需要压缩和封面多尺寸时使用此命令。

### PicGo

| 配置项 | 值 |
|--------|-----|
| 仓库 | `madneal/blog-image` |
| 分支 | `main` |
| 路径 | `images/` |
| 自定义域名 | `https://cdn.jsdelivr.net/gh/madneal/blog-image@main` |

### CLI

```bash
picgo upload ./shot.png
# 或
blog-img-upload ./shot.png
```

### Git

```bash
git add images/ && git commit -m "upload: xxx" && git push
```

## 刷新 CDN

```text
https://purge.jsdelivr.net/gh/madneal/blog-image@main/images/post-covers/xxx.jpg
```

## 注意

- 仓库保持 **Public**，jsDelivr 才能访问。
- 单文件勿过大（建议 < 20MB）。
