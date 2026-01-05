# 每日5分钟读懂一家公司 - Web 产品

一个基于 Next.js + FastAPI + Supabase 的 Web 应用，让用户通过每日打卡系统性学习公司知识。

## 技术栈

- **前端**: Next.js 14 (App Router) + TypeScript + TailwindCSS
- **后端 API**: FastAPI (Python)
- **数据库 & Auth**: Supabase (PostgreSQL)
- **部署**: Vercel (前端) + Supabase (后端服务)

## 项目结构

```
.
├── web/                 # Next.js 前端
│   ├── app/            # App Router 页面
│   ├── components/     # React 组件
│   ├── lib/            # 工具函数和 API 客户端
│   └── constants/      # 配置常量
├── api/                # FastAPI 后端
│   └── main.py         # API 入口
├── supabase/           # 数据库 Schema
│   └── schema.sql      # SQL 建表脚本
├── company_story.py    # 核心生成器（Python）
├── schemas.py          # 数据模型
├── prompts.py          # 提示词模板
└── utils.py            # 工具函数
```

## 快速开始

### 1. 环境准备

#### 前端 (Next.js)

```bash
cd web
npm install
```

#### 后端 (FastAPI)

```bash
cd api
pip install -r requirements.txt
# 还需要安装核心代码的依赖
pip install -r ../requirements.txt
```

### 2. 配置 Supabase

1. 在 [Supabase](https://supabase.com) 创建新项目
2. 在 SQL Editor 中运行 `supabase/schema.sql` 创建表
3. 获取项目 URL 和 anon key

### 3. 配置环境变量

#### 前端 (.env.local)

```bash
cd web
cp .env.example .env.local
```

编辑 `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 后端 (.env)

```bash
cd api
cp .env.example .env
```

编辑 `.env`:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
PORT=8000
```

### 4. 启动服务

#### 启动后端 API

```bash
cd api
python main.py
# 或使用 uvicorn
uvicorn main:app --reload --port 8000
```

后端将在 `http://localhost:8000` 运行

#### 启动前端

```bash
cd web
npm run dev
```

前端将在 `http://localhost:3000` 运行

## 功能说明

### 已实现功能

1. **首页**: 输入公司名/代码生成内容
2. **公司内容页**: 展示生成的深度文章，支持打卡
3. **历史记录**: 查看浏览过的公司
4. **打卡记录**: 显示连续打卡天数、日历、历史记录
5. **个人中心**: 学习统计数据
6. **登录系统**: Supabase Auth (Magic Link)

### 核心特性

- ✅ 24小时内容缓存（避免重复生成）
- ✅ 每日打卡唯一性约束
- ✅ 连续打卡 streak 计算
- ✅ 响应式设计
- ✅ 文艺复兴美学 UI

## 部署

### 前端部署 (Vercel)

1. 将代码推送到 GitHub
2. 在 Vercel 导入项目
3. 选择 `web` 目录作为根目录
4. 配置环境变量
5. 部署

### 后端部署

#### 选项1: Vercel Serverless Functions (推荐)

将 FastAPI 转换为 Vercel 函数（需要适配）

#### 选项2: Railway / Render

1. 连接 GitHub 仓库
2. 选择 `api` 目录
3. 配置环境变量
4. 部署

#### 选项3: 本地运行 + ngrok (开发测试)

```bash
# 启动 API
cd api && python main.py

# 在另一个终端
ngrok http 8000
# 使用 ngrok URL 更新 NEXT_PUBLIC_API_URL
```

### Supabase 配置

1. 在 Supabase Dashboard 运行 `supabase/schema.sql`
2. 配置 Auth 设置（邮箱登录）
3. 配置 RLS 策略（已在 schema.sql 中）

## 开发说明

### 核心代码集成

核心 Python 代码位于项目根目录：
- `company_story.py`: 主生成器类
- `schemas.py`: 数据模型
- `prompts.py`: 提示词
- `utils.py`: 工具函数

FastAPI 通过 `sys.path` 导入这些模块。

### 内容生成流程

1. 用户输入公司名/代码
2. 前端调用 `/api/generate` (FastAPI)
3. FastAPI 调用 `CompanyStoryGenerator.generate()`
4. 返回 Markdown 文章和 FactPack
5. 前端解析并展示
6. 可选：缓存到 Supabase

### 缓存策略

- 同一 ticker 24小时内优先使用缓存
- 缓存存储在 `company_content_cache` 表
- 前端检查缓存 → 如有则直接使用 → 否则调用 API

## 常见问题

### Q: API 调用失败？

A: 检查：
1. 后端是否运行在 `http://localhost:8000`
2. `OPENAI_API_KEY` 是否正确
3. 网络连接是否正常

### Q: Supabase 连接失败？

A: 检查：
1. `NEXT_PUBLIC_SUPABASE_URL` 和 `NEXT_PUBLIC_SUPABASE_ANON_KEY` 是否正确
2. Supabase 项目是否已创建表（运行 schema.sql）
3. RLS 策略是否正确配置

### Q: 打卡功能不工作？

A: 检查：
1. 用户是否已登录
2. 数据库表 `checkins` 是否已创建
3. 唯一性约束是否生效

## 未来扩展 (TODO)

- [ ] App 版本 (React Native)
- [ ] 推送提醒（每日学习提醒）
- [ ] 学习计划（推荐学习路径）
- [ ] 收藏夹功能
- [ ] 订阅功能（付费解锁更多内容）
- [ ] 社交功能（分享学习成果）
- [ ] 数据分析（学习报告）
- [ ] 多语言支持

## 许可证

MIT License

