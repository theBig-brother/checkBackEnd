# checkBackEnd
快排的后端

警告：有小概率图片会在同一秒上传导致文件名错乱，以后记得优化
# 启动:

```bash
python .\manage.py runserver 0.0.0.0:8000
```

## 简介
快排后端是一个基于 Django 开发的后端服务，支持前端上传图片并存储，同时使用数据库管理图片的路径。

## 功能
- [x] 前端上传图片
- [x] 后端存储图片
- [x] 数据库管理图片路径（使用 SQLite，未来可能更换）
- [x] 后台读取上传的所有图片
- [ ] 账户管理（暂未实现）

## 技术栈
- **后端框架**: Django
- **数据库**: SQLite（未来可能更换）

## 安装与运行

### 1. 克隆项目
```bash
git clone https://github.com/theBig-brother/checkBackEnd.git
cd checkBackEnd
```

### 2. 创建虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. 数据库迁移
```bash
python manage.py migrate
```

### 4. 启动 Django 服务器
```bash
python manage.py runserver
```

## API 说明
| 端点 | 方法 | 描述 |
|------|------|------|
| `/upload/` | POST | 上传图片 |
| `/images/` | GET、DELETE | 获取所有上传的图片 |
| `/accounts/` | - | 账户管理相关 API（待实现） |

## 未来计划
- [ ] 增加账户管理，支持用户登录、注册
- [ ] 可能更换 SQLite 为更强大的数据库（如 PostgreSQL、MySQL）

## 贡献
欢迎提交 Issue 或 Pull Request 来改进本项目。

## 许可
本项目使用 Apache License 许可证。

