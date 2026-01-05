# 部署指南

## Supabase 配置已完成 ✅

- URL: https://hlbszanbniewhweznuwy.supabase.co
- Anon Key: sb_publishable_yLDI2T89qW5zXUbcBYlkDA_rlm-1W-H

## 部署步骤

### 方式1: Vercel 部署（推荐）

1. **安装 Vercel CLI**（如果还没有）:
   ```bash
   npm i -g vercel
   ```

2. **登录 Vercel**:
   ```bash
   vercel login
   ```

3. **在项目根目录部署**:
   ```bash
   cd web
   vercel
   ```

4. **配置环境变量**:
   在 Vercel Dashboard 中，进入项目设置 → Environment Variables，添加：
   - `NEXT_PUBLIC_SUPABASE_URL` = `https://hlbszanbniewhweznuwy.supabase.co`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `sb_publishable_yLDI2T89qW5zXUbcBYlkDA_rlm-1W-H`
   - `NEXT_PUBLIC_API_URL` = `你的后端API地址`（如果后端已部署）

5. **重新部署**:
   ```bash
   vercel --prod
   ```

### 方式2: 通过 GitHub + Vercel（推荐用于生产）

1. **推送代码到 GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **在 Vercel 导入项目**:
   - 访问 [vercel.com](https://vercel.com)
   - 点击 "New Project"
   - 导入 GitHub 仓库
   - **重要**: 设置 Root Directory 为 `web`
   - 配置环境变量（同上）
   - 部署

### 方式3: 本地测试运行

1. **安装依赖**:
   ```bash
   cd web
   npm install
   ```

2. **创建 .env.local**:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://hlbszanbniewhweznuwy.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_yLDI2T89qW5zXUbcBYlkDA_rlm-1W-H
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **启动开发服务器**:
   ```bash
   npm run dev
   ```

4. **启动后端 API**（另一个终端）:
   ```bash
   cd api
   python main.py
   ```

5. **访问**: http://localhost:3000

## 后端 API 部署

### 选项1: Railway（推荐）

1. 访问 [railway.app](https://railway.app)
2. 创建新项目，从 GitHub 导入
3. 设置 Root Directory 为 `api`
4. 配置环境变量：
   - `OPENAI_API_KEY` = 你的 OpenAI API Key
   - `OPENAI_MODEL` = `gpt-4o`
   - `PORT` = `8000`
5. 部署后，更新前端的 `NEXT_PUBLIC_API_URL`

### 选项2: Render

1. 访问 [render.com](https://render.com)
2. 创建新的 Web Service
3. 连接 GitHub 仓库
4. 设置：
   - Build Command: `pip install -r requirements.txt && pip install -r ../requirements.txt`
   - Start Command: `python main.py`
   - Root Directory: `api`
5. 配置环境变量（同上）

### 选项3: 本地运行 + ngrok（开发测试）

```bash
# 启动 API
cd api
python main.py

# 在另一个终端
ngrok http 8000
# 使用 ngrok 提供的 URL 更新 NEXT_PUBLIC_API_URL
```

## 重要提示

1. **Supabase Auth 配置**:
   - 在 Supabase Dashboard → Authentication → URL Configuration
   - 添加你的前端域名到 "Redirect URLs"
   - 例如: `https://your-app.vercel.app/auth/callback`

2. **CORS 配置**:
   - 如果后端和前端不同域名，需要在 `api/main.py` 中更新 `allow_origins`

3. **环境变量**:
   - 生产环境必须使用环境变量，不要硬编码
   - Vercel 会自动注入环境变量到构建过程

## 验证部署

部署完成后，检查：
- [ ] 首页可以访问
- [ ] 可以输入公司名生成内容
- [ ] 登录功能正常
- [ ] 打卡功能正常
- [ ] 历史记录可以查看

## 故障排除

**问题**: 前端无法连接 Supabase
- 检查环境变量是否正确设置
- 检查 Supabase 项目的 API 设置

**问题**: API 调用失败
- 检查后端是否运行
- 检查 `NEXT_PUBLIC_API_URL` 是否正确
- 检查 CORS 配置

**问题**: 登录后无法跳转
- 检查 Supabase Auth 的 Redirect URLs 配置
- 检查 `/auth/callback` 路由是否正确

