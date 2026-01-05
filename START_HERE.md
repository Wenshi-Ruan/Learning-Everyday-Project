# 🚀 开始部署

## 当前状态

✅ **Supabase 已配置**
- URL: https://hlbszanbniewhweznuwy.supabase.co
- Anon Key: sb_publishable_yLDI2T89qW5zXUbcBYlkDA_rlm-1W-H
- Schema 已创建

✅ **代码已就绪**
- 所有页面和功能已实现
- 环境变量已配置

## 立即部署到 Vercel

### 最简单的方法（推荐）

1. **安装 Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **登录 Vercel**:
   ```bash
   vercel login
   ```

3. **部署**:
   ```bash
   cd web
   vercel
   ```
   
   当提示输入环境变量时，输入：
   - `NEXT_PUBLIC_SUPABASE_URL` = `https://hlbszanbniewhweznuwy.supabase.co`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = `sb_publishable_yLDI2T89qW5zXUbcBYlkDA_rlm-1W-H`
   - `NEXT_PUBLIC_API_URL` = `http://localhost:8000` (暂时，后续可更新)

4. **生产环境部署**:
   ```bash
   vercel --prod
   ```

5. **配置 Supabase Auth**:
   - 访问 Supabase Dashboard
   - Authentication → URL Configuration
   - 添加 Redirect URL: `https://your-app.vercel.app/auth/callback`

### 或者通过 GitHub + Vercel Web UI

1. **推送代码到 GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **在 Vercel 部署**:
   - 访问 https://vercel.com/new
   - 导入 GitHub 仓库
   - **重要**: Root Directory 设置为 `web`
   - 添加环境变量（见上方）
   - Deploy

## 部署后

访问你的 Vercel URL，你应该能看到：
- ✅ 极简的首页
- ✅ 可以输入公司名生成内容
- ✅ 登录功能
- ✅ 打卡功能

## 需要帮助？

查看详细文档：
- `README_WEB.md` - 完整文档
- `DEPLOY.md` - 详细部署指南
- `DEPLOY_CHECKLIST.md` - 检查清单

