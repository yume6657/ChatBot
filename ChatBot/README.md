# DeepSeek智能对话系统

基于Django和DeepSeek API的智能对话系统，支持用户注册登录、多轮对话和历史记录管理。

## 功能特性

- 🔐 **用户认证系统**：基于Django内置认证，支持用户注册和登录
- 💾 **对话历史管理**：MySQL数据库存储对话记录，支持多轮对话上下文
- 🤖 **智能对话**：集成DeepSeek大模型，提供高质量的AI对话体验
- 📱 **响应式界面**：简洁美观的Web界面，支持移动端访问
- 📊 **使用统计**：实时显示用户对话统计和Token使用情况

## 技术栈

- **后端框架**：Django 4.2.7
- **数据库**：MySQL
- **AI服务**：DeepSeek API
- **前端技术**：HTML + CSS + JavaScript
- **部署环境**：Python 3.8+

## 安装部署

### 环境要求

- Python 3.8+
- MySQL 5.7+
- DeepSeek API密钥

### 快速开始

1. **克隆项目**
```bash
git clone <项目地址>
cd ChatBot
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置您的设置
```

4. **数据库设置**
```bash
# 创建数据库（在MySQL中执行）
CREATE DATABASE chatbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 执行数据库迁移
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户（可选）**
```bash
python manage.py createsuperuser
```

6. **启动开发服务器**
```bash
python manage.py runserver
```

7. **访问应用**
打开浏览器访问 http://127.0.0.1:8000

## 配置文件说明

### .env 文件配置

```bash
# Django配置
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DB_NAME=chatbot_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306

# DeepSeek API配置
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

### 获取DeepSeek API密钥

1. 访问 [DeepSeek官网](https://www.deepseek.com)
2. 注册账号并登录
3. 在控制台获取API密钥
4. 将API密钥填入.env文件中的DEEPSEEK_API_KEY

## 项目结构

```
ChatBot/
├── chatbot_project/          # Django项目配置
│   ├── settings.py          # 项目设置
│   ├── urls.py              # URL路由
│   └── ...
├── chatbot_app/             # 主要应用
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图函数
│   ├── urls.py              # 应用路由
│   ├── deepseek_api.py      # DeepSeek API对接
│   └── ...
├── templates/               # HTML模板
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页
│   ├── chat.html            # 聊天界面
│   └── registration/        # 认证相关模板
├── requirements.txt         # Python依赖
├── manage.py               # Django管理脚本
├── setup.py               # 安装脚本
└── README.md              # 项目说明
```

## 数据库设计

### 主要数据表

1. **conversations** - 对话会话表
   - id: 主键
   - user_id: 用户外键
   - title: 对话标题
   - created_at: 创建时间
   - updated_at: 更新时间

2. **messages** - 对话消息表
   - id: 主键
   - conversation_id: 对话外键
   - role: 消息角色（user/assistant/system）
   - content: 消息内容
   - timestamp: 时间戳
   - tokens_used: Token使用量

3. **user_profiles** - 用户扩展信息表
   - id: 主键
   - user_id: 用户外键
   - api_key: 用户自定义API密钥
   - total_tokens_used: 总Token使用量
   - created_at: 创建时间

## API接口

### 认证相关
- `GET /` - 首页
- `GET /register/` - 用户注册页面
- `POST /register/` - 用户注册
- `GET /login/` - 用户登录页面
- `POST /login/` - 用户登录
- `GET /logout/` - 用户登出

### 对话管理
- `GET /chat/` - 聊天界面
- `GET /api/conversations/` - 获取用户对话列表
- `GET /api/conversations/<id>/messages/` - 获取对话消息
- `POST /api/send_message/` - 发送消息
- `POST /api/conversations/create/` - 创建新对话
- `POST /api/conversations/<id>/delete/` - 删除对话
- `GET /api/user_stats/` - 获取用户统计信息

## 开发说明

### 自定义开发

1. **添加新功能**：在`chatbot_app/views.py`中添加新的视图函数
2. **修改界面**：编辑`templates/`目录下的HTML文件
3. **扩展模型**：在`chatbot_app/models.py`中添加新的数据模型
4. **API集成**：在`chatbot_app/deepseek_api.py`中扩展API功能

### 部署生产环境

1. 设置`DEBUG=False`
2. 配置生产环境数据库
3. 设置静态文件收集
4. 配置Web服务器（如Nginx + Gunicorn）

## 常见问题

### Q: 如何修改对话模型？
A: 在`deepseek_api.py`中的`send_message`方法修改model参数

### Q: 如何限制对话历史长度？
A: 在`views.py`中的`send_message`函数修改`previous_messages`的切片数量

### Q: 如何添加用户自定义API密钥？
A: 在UserProfile模型中已预留api_key字段，可在管理界面设置

## 许可证

本项目仅用于学习和研究目的。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题请联系项目维护者。