# 快速启动指南

## 🚀 5 分钟快速开始

### 1. 安装依赖

```bash
# 前端
cd web
npm install

# 后端（需要 Python 3.10+）
cd ../api
pip install -r requirements.txt
pip install -r ../requirements.txt
```

### 2. 配置 Supabase

1. 访问 [supabase.com](https://supabase.com) 创建项目
2. 在 SQL Editor 中运行 `supabase/schema.sql`
3. 获取项目 URL 和 anon key

### 3. 配置环境变量

**前端** (`web/.env.local`):
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**后端** (`api/.env`):
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
PORT=8000
```

### 4. 启动服务

**终端1 - 后端**:
```bash
cd api
python main.py
```

**终端2 - 前端**:
```bash
cd web
npm run dev
```

### 5. 访问应用

打开浏览器访问: http://localhost:3000

## 📁 项目结构

```
.
├── web/              # Next.js 前端
│   ├── app/         # 页面和路由
│   ├── components/  # React 组件
│   └── lib/         # 工具函数
├── api/             # FastAPI 后端
│   └── main.py      # API 入口
├── supabase/        # 数据库 Schema
└── [核心 Python 代码]
```

## ✅ 功能清单

- [x] 用户登录（Magic Link）
- [x] 公司故事生成
- [x] 历史记录
- [x] 打卡功能（streak 计算）
- [x] 个人中心（统计数据）
- [x] 24小时内容缓存
- [x] 文艺复兴美学 UI

## 🐛 常见问题

**Q: API 调用失败？**
- 检查后端是否运行在 8000 端口
- 检查 OPENAI_API_KEY 是否正确

**Q: Supabase 连接失败？**
- 检查环境变量是否正确
- 确认已运行 schema.sql 创建表

**Q: 打卡功能不工作？**
- 确认用户已登录
- 检查数据库表是否创建成功

## 📚 详细文档

查看 `README_WEB.md` 获取完整文档。

