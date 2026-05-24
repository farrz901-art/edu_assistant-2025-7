# 教学实训智能体平台

一个面向教学实训场景的全栈 AI 应用，提供学生端课程问答、教师端学情分析、课程管理与大模型能力接入。项目采用 Python/Django 后端、Vue 前端、PostgreSQL 数据库，并使用 Docker Compose 编排 backend、frontend、database 与 Nginx 服务。


## 核心功能

- 学生端：基于课程内容的 AI 学习问答
- 教师端：基于练习历史的学情分析与教学建议
- 课程管理：课程查询与基础管理 API
- AI 服务：接入讯飞星火大模型
- 部署：Docker Compose 本地容器化部署
- 测试：功能测试与问题记录


## 讯飞星火大模型接入

1. 申请 API Key / App ID: https://www.xfyun.cn/doc/spark/HTTP调用文档.html
2. 在项目根目录创建 `.env`:
```
SPARK_API_KEY=xxxx
SPARK_APP_ID=xxxx
# 可选
SPARK_MODEL=generalv3.5
```
3. 启动
```
docker-compose down -v
docker-compose up --build -d
``` 
