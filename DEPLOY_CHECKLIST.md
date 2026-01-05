# 部署检查清单 ✅

## 已完成 ✅

- [x] Supabase 项目已创建
- [x] Database Schema 已运行 (`supabase/schema.sql`)
- [x] Supabase URL 和 Anon Key 已配置
- [x] 环境变量文件已创建 (`web/.env.local`)
- [x] 所有代码文件已就绪
- [x] CORS 配置已更新

## 部署前检查

### 1. Supabase 配置验证

访问 Supabase Dashboard 确认：
- [x] 表已创建：`company_views`, `checkins`, `company_content_cache`
- [ ] RLS 策略已启用
- [ ] Auth 已启用（Email/Magic Link）

### 2. 代码准备

- [x] 所有页面文件已创建
- [x] API 路由已配置
- [x] 数据库操作函数已实现
- [x] 环境变量模板已创建

### 3. 部署步骤

#### 选项A: Vercel CLI（最快）

```bash
# 1. 安装 Vercel CLI（如果还没有）
npm i -g vercel

# 2. 登录
vercel login

# 3. 进入 web 目录
cd web

# 4. 部署（会提示配置环境变量）
vercel

# 5. 生产环境部署
vercel --prod
```

#### 选项B: GitHub + Vercel Web UI（推荐）

1. **推送代码到 GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **在 Vercel 部署**:
   - 访问 https://vercel.com/new
   - 导入 GitHub 仓库
   - **重要**: Root Directory 设置为 `web`
   - 环境变量：
     - `NEXT_PUBLIC_SUPABASE_URL` = `https://hlbszanbniewhweznuwy.supabase.co`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `sb_publishable_yLDI2T89qW5zXUbcBYlkDA_rlm-1W-H`
     - `NEXT_PUBLIC_API_URL` = `http://localhost:8000` (或你的后端地址)
   - 点击 Deploy

3. **配置 Supabase Auth Redirect**:
   - Supabase Dashboard → Authentication → URL Configuration
   - 添加: `https://your-app.vercel.app/auth/callback`

## 部署后验证

访问你的 Vercel URL，测试：

- [ ] 首页可以访问
- [ ] 可以输入公司名（如 "Apple" 或 "AAPL"）
- [ ] 生成内容功能（需要后端 API 运行）
- [ ] 登录功能（Magic Link）
- [ ] 历史记录页面
- [ ] 打卡功能
- [ ] 个人中心

## 后端 API 部署（可选）

如果后端也需要上线：

### Railway 部署

1. 访问 https://railway.app
2. New Project → Deploy from GitHub
3. 选择仓库，Root Directory: `api`
4. 环境变量：
   - `OPENAI_API_KEY` = 你的 OpenAI Key
   - `OPENAI_MODEL` = `gpt-4o`
   - `PORT` = `8000`
5. 部署后，更新前端的 `NEXT_PUBLIC_API_URL`

## 故障排除

**问题**: 构建失败
- 检查 Node.js 版本（需要 18+）
- 检查 `package.json` 依赖是否正确

**问题**: Supabase 连接失败
- 检查环境变量是否正确
- 检查 Supabase 项目是否激活

**问题**: 登录后无法跳转
- 检查 Supabase Auth Redirect URLs 配置
- 检查 `/auth/callback` 路由

**问题**: API 调用失败
- 检查后端是否运行
- 检查 `NEXT_PUBLIC_API_URL` 是否正确
- 检查 CORS 配置

