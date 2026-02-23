# Railway 部署指南

本文档详细说明如何将 Unst2st 部署到 Railway 平台（完全免费）。

---

## 📋 准备工作

### 1. 注册智谱AI账号并获取API密钥

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录账号
3. 进入控制台 → API管理 → API密钥
4. 点击「创建新的API密钥」
5. 复制并保存密钥（格式类似：`xxx.xxxxxxxxxxxxxxxxxx`）

**重要**：妥善保管你的API密钥，不要泄露给他人！

### 2. 注册Railway账号

1. 访问 [Railway.app](https://railway.app)
2. 点击「Login」，选择「Login with GitHub」
3. 授权Railway访问你的GitHub账号

---

## 🚀 部署步骤

### 方式一：从GitHub仓库部署（推荐）

#### 第1步：将代码推送到GitHub

```bash
# 在项目目录下
cd D:\code\20260223_Unst2st

# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Unst2st v1.0"

# 在GitHub上创建新仓库（访问 https://github.com/new）
# 然后关联远程仓库
git remote add origin https://github.com/你的用户名/unst2st.git

# 推送到GitHub
git push -u origin main
```

#### 第2步：在Railway创建项目

1. 登录Railway控制台
2. 点击「New Project」
3. 选择「Deploy from GitHub repo」
4. 选择你刚才创建的仓库（如：unst2st）
5. Railway会自动检测到Dockerfile并开始构建

#### 第3步：配置环境变量

1. 在Railway项目页面，点击你的服务
2. 切换到「Variables」标签
3. 点击「New Variable」，添加：
   - **Variable Name**: `ZHIPU_API_KEY`
   - **Value**: 粘贴你的智谱AI API密钥
4. 点击「Add」保存

#### 第4步：等待部署完成

- Railway会自动重新部署服务
- 部署过程约2-5分钟
- 部署成功后，在「Deployments」可以看到绿色的✓标记

#### 第5步：获取访问地址

1. 在服务页面，点击「Settings」标签
2. 找到「Domains」部分
3. 点击「Generate Domain」
4. Railway会自动生成一个域名，如：`unst2st-production.up.railway.app`
5. 点击域名即可访问你的系统！

---

### 方式二：使用Railway CLI部署

#### 安装Railway CLI

```bash
# 使用npm安装
npm install -g @railway/cli

# 或使用Homebrew (Mac)
brew install railway
```

#### 登录并部署

```bash
# 登录Railway
railway login

# 初始化项目
cd D:\code\20260223_Unst2st
railway init

# 配置环境变量
railway variables set ZHIPU_API_KEY=你的API密钥

# 部署
railway up

# 打开项目
railway open
```

---

## ✅ 验证部署

### 1. 检查健康状态

访问 `https://你的域名/health`，应该看到：

```json
{
  "status": "healthy",
  "api_key_configured": true
}
```

如果 `api_key_configured` 为 `false`，说明环境变量未正确配置。

### 2. 访问前端页面

访问 `https://你的域名/`，应该能看到 Unst2st 的主界面。

### 3. 测试功能

1. 创建一个测试模板
2. 上传一个测试文档
3. 查看提取结果

---

## 🔧 常见问题

### Q1: 部署失败，显示"Build failed"

**原因**：可能是Dockerfile配置或依赖安装失败

**解决方法**：
1. 检查Railway的部署日志（Deployments → 点击失败的部署 → View Logs）
2. 查看具体错误信息
3. 常见问题：
   - 缺少某个Python包 → 检查 `requirements.txt`
   - 系统依赖缺失 → 检查 `Dockerfile` 中的 `apt-get install`

### Q2: 访问域名显示"Application failed to respond"

**原因**：服务未正确启动或端口配置错误

**解决方法**：
1. 检查Railway的日志，查看服务是否成功启动
2. 确认环境变量 `ZHIPU_API_KEY` 已正确配置
3. 检查 `Dockerfile` 中的 `EXPOSE 8000` 和启动命令

### Q3: API调用失败，提示"未配置API密钥"

**原因**：环境变量未设置或设置错误

**解决方法**：
1. 进入Railway项目 → Variables
2. 检查 `ZHIPU_API_KEY` 是否存在且值正确
3. 重新部署服务

### Q4: 免费额度用完了怎么办？

**Railway免费额度**：500小时/月
- 如果用完，可以升级到付费计划（约$5/月）
- 或者设置服务休眠策略，闲置时自动休眠

**智谱AI免费额度**：400万tokens/月
- 每月1号自动重置
- 如果提前用完，可以升级到付费计划或等待重置

### Q5: 如何查看使用量？

**Railway使用量**：
- 进入项目 → Settings → Usage
- 可以看到当前月份的使用时长

**智谱AI使用量**：
- 登录智谱AI控制台
- 进入「用量统计」查看

---

## 🎯 优化建议

### 1. 配置自定义域名（可选）

如果你有自己的域名，可以在Railway中配置：

1. 进入项目 → Settings → Domains
2. 点击「Custom Domain」
3. 输入你的域名（如：`unst2st.yourdomain.com`）
4. 按照提示配置DNS记录
5. 等待DNS生效（约5-10分钟）

### 2. 启用休眠策略（节省额度）

Railway支持配置闲置自动休眠：

1. 进入项目 → Settings
2. 找到「Sleep on Idle」选项
3. 开启后，15分钟无访问会自动休眠
4. 访问时自动唤醒（首次访问可能需要10-20秒启动）

**推荐**：开启休眠功能，可以让500小时免费额度使用整月！

### 3. 配置日志监控

Railway自动收集应用日志：

1. 进入项目 → Observability
2. 可以看到实时日志和历史日志
3. 方便排查问题

---

## 📊 成本估算

### 完全免费方案

- **Railway**: 500小时/月（开启休眠功能可用整月）
- **智谱AI**: 400万tokens/月

**适用场景**：小团队（5-10人），每天处理50个文档以内

### 付费升级方案（如需要）

- **Railway Pro**: $5/月（更多资源和服务时长）
- **智谱AI**: 按需付费（约0.01元/千tokens）

---

## 🎉 部署成功！

恭喜！你的 Unst2st 系统已成功部署到云端。

现在你可以：
- 分享访问地址给团队成员
- 在任何设备的浏览器中使用
- 无需担心本地电脑关机影响使用

**访问地址示例**：`https://unst2st-production.up.railway.app`

---

有任何问题欢迎查看项目README或提交Issue！
