# 📦 项目部署和分发指南

本文档说明如何将项目打包给其他人使用。

## 🎯 打包前checklist

在打包项目之前，请确保：

- [ ] 所有功能都已测试通过
- [ ] README.md 已更新
- [ ] 所有依赖都在 requirements.txt 和 package.json 中
- [ ] 移除了敏感信息（API keys, passwords等）
- [ ] Git 仓库是干净的（已提交所有更改）

## 📋 方式一：Git 仓库分发（推荐）

### 步骤

1. **推送到 Git 仓库**
```bash
# 如果还没有远程仓库，创建一个（GitHub/GitLab/Gitee）
git remote add origin <your-repo-url>
git push -u origin master
```

2. **分享仓库链接**
```
其他人可以通过以下命令获取：
git clone <your-repo-url>
cd chatbot
```

3. **提供安装说明**
```
参考 README.md 中的"快速开始"部分
```

### 优点
- ✅ 版本控制
- ✅ 易于更新
- ✅ 自动排除不必要的文件（通过 .gitignore）
- ✅ 协作开发友好

## 📋 方式二：压缩包分发

### 步骤

1. **清理项目**
```bash
# 删除不必要的文件
rm -rf frontend/node_modules
rm -rf backend/__pycache__
rm -rf backend/.venv
rm -rf .git  # 如果不需要 Git 历史
```

2. **创建压缩包**

**Windows (PowerShell):**
```powershell
Compress-Archive -Path . -DestinationPath ../chatbot-project.zip
```

**macOS/Linux:**
```bash
cd ..
tar -czf chatbot-project.tar.gz chatbot/
```

3. **包含以下文件说明书（创建 SETUP_GUIDE.txt）**
```
中国旅游AI聊天机器人 - 安装指南
================================

环境要求：
- Python 3.8+
- Node.js 14.x+
- npm 6.x+

快速开始：
1. 解压文件到任意目录
2. 双击运行 start-backend.bat（启动后端）
3. 双击运行 start-frontend.bat（启动前端）
4. 打开浏览器访问 http://localhost:3000

详细说明请参考 README.md
```

## 📋 方式三：Docker 容器化（高级）

### 创建 Dockerfile

**Backend Dockerfile** (`backend/Dockerfile`)：
```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile** (`frontend/Dockerfile`)：
```dockerfile
FROM node:14 as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose** (`docker-compose.yml`)：
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

### 使用方法
```bash
docker-compose up -d
```

## 🗂️ 项目文件夹结构（给其他人）

打包后，确保包含以下文件：

```
chatbot/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   └── (不包含: __pycache__, .venv, *.pyc)
├── frontend/
│   ├── package.json
│   ├── public/
│   ├── src/
│   └── (不包含: node_modules/, build/)
├── start-backend.bat
├── start-frontend.bat
├── README.md
├── .gitignore
└── SETUP_GUIDE.txt (可选)
```

## ⚠️ 注意事项

### 必须排除的文件/文件夹

**Backend:**
- `__pycache__/`
- `*.pyc`
- `.venv/` 或 `venv/`
- `*.log`
- `.env` (如果有环境变量文件)

**Frontend:**
- `node_modules/`
- `build/`
- `.env` (如果有)

**通用:**
- `.git/` (如果不需要 Git 历史)
- `.DS_Store` (macOS)
- `Thumbs.db` (Windows)
- 测试图片/PDF（如 great_wall_real.jpg, flight_ticket.pdf）

### 已经被 .gitignore 排除的文件

你的项目已经有 `.gitignore`，以下文件会自动排除：
- `node_modules/`
- `build/`
- `__pycache__/`
- `.venv/`
- `*.pyc`
- 等等...

## 📧 分发给其他人的说明模板

你可以给其他人发送以下消息：

---

**主题：中国旅游AI聊天机器人 - 项目分享**

你好！

我想分享一个我开发的中国旅游AI聊天机器人项目。

**项目简介：**
一个功能丰富的AI旅游助手，包含天气查询、翻译、票据识别等15+功能。

**获取方式：**
方式1：Git 仓库（推荐）
```
git clone <your-repo-url>
```

方式2：下载压缩包
[附件：chatbot-project.zip]

**快速开始：**
1. 安装 Python 3.8+ 和 Node.js 14.x+
2. 解压/克隆项目
3. 运行 `start-backend.bat`（后端）
4. 运行 `start-frontend.bat`（前端）
5. 访问 http://localhost:3000

**详细文档：**
请参考项目中的 README.md 文件

有任何问题随时联系我！

---

## 🔧 给接收者的首次运行步骤

### Windows 用户

1. **安装依赖**（首次需要）
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd ../frontend
npm install
```

2. **启动项目**
```bash
# 返回项目根目录
cd ..

# 启动后端（双击或命令行运行）
start-backend.bat

# 新开一个终端，启动前端
start-frontend.bat
```

### macOS/Linux 用户

需要创建对应的 shell 脚本：

**start-backend.sh:**
```bash
#!/bin/bash
cd backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**start-frontend.sh:**
```bash
#!/bin/bash
cd frontend
npm start
```

给予执行权限：
```bash
chmod +x start-backend.sh
chmod +x start-frontend.sh
```

## ✅ 验证打包是否成功

打包后，在另一台干净的电脑上测试：

1. ✅ 解压/克隆项目
2. ✅ 安装依赖成功
3. ✅ 后端启动成功（http://localhost:8000）
4. ✅ 前端启动成功（http://localhost:3000）
5. ✅ 能够注册新用户
6. ✅ 能够登录
7. ✅ 所有功能正常工作

## 📞 技术支持

如果其他人遇到问题，建议他们：

1. **检查环境要求**
   - Python 版本：`python --version`
   - Node.js 版本：`node --version`
   - npm 版本：`npm --version`

2. **查看日志**
   - 后端日志：启动终端的输出
   - 前端日志：浏览器控制台（F12）

3. **常见问题参考 README.md 的"Troubleshooting"部分**

---

**祝分发顺利！🎉**
