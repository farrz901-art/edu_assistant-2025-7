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