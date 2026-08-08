# blog-image

博客图床仓库，通过 **GitHub + jsDelivr** 提供图片 CDN 直链。

## 链接格式

```text
https://cdn.jsdelivr.net/gh/madneal/blog-image@main/<图片路径>
```

示例：

```markdown
![示例](https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/example.jpg)
```

> 也可用 raw 链接（无 CDN 加速）：  
> `https://raw.githubusercontent.com/madneal/blog-image/main/images/example.jpg`

## 目录约定

| 路径 | 说明 |
|------|------|
| `images/` | 默认上传目录（PicGo / Git 均可） |
| `images/YYYY/` | 可选：按年份归档 |
| `images/posts/` | 可选：文章配图 |

## 上传方式

### 1. PicGo（推荐）

1. 安装 [PicGo](https://github.com/Molunerfinn/PicGo) 与 **github-plus** / 内置 GitHub 图床
2. 图床设置示例：

| 配置项 | 值 |
|--------|-----|
| 仓库名 | `madneal/blog-image` |
| 分支 | `main` |
| 存储路径 | `images/` |
| 自定义域名 | `https://cdn.jsdelivr.net/gh/madneal/blog-image@main` |
| Token | 有 `public_repo` 或 `repo` 权限的 GitHub PAT |

3. 上传后链接形如：  
   `https://cdn.jsdelivr.net/gh/madneal/blog-image@main/images/xxx.png`

### 2. Git 手动上传

```bash
git clone git@github.com:madneal/blog-image.git
cd blog-image
# 把图片放到 images/
git add images/
git commit -m "upload: xxx"
git push origin main
```

上传后稍等几秒再访问 jsDelivr（首次拉取可能有短延迟）。

## 刷新 CDN 缓存

若覆盖同名文件后仍显示旧图，可刷新 jsDelivr：

```text
https://purge.jsdelivr.net/gh/madneal/blog-image@main/images/example.jpg
```

或在链接中使用带 commit hash 的版本（更稳，适合永久引用）：

```text
https://cdn.jsdelivr.net/gh/madneal/blog-image@<commit-sha>/images/example.jpg
```

## 注意

- 仓库需为 **Public**，jsDelivr 才能公开访问。
- 单文件建议控制体积（过大可能影响 Git 与 CDN）。
- 勿提交敏感/未授权图片。
