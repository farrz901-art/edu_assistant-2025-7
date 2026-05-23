# 环境变量配置说明

## 讯飞星火API配置

在使用本项目之前，您需要配置讯飞星火API的认证信息。

### 1. 获取API凭证

1. 登录[讯飞开放平台控制台](https://console.xfyun.cn/)
2. 进入星火认知大模型服务
3. 获取以下信息：
   - **HTTP服务接口认证信息**：APIPassword（用于HTTP调用）
   - **WebSocket服务接口认证信息**：APPID、APISecret、APIKey（备用）

### 2. 创建.env文件

在项目根目录创建`.env`文件，内容如下：

```bash
# 数据库配置
DB_NAME=edu_assistant
DB_USER=postgres
DB_PASSWORD=your_database_password

# 讯飞星火API配置
# HTTP API配置 (主要使用)
SPARK_API_PASSWORD=你的APIPassword  # 例如：jtP****YLw

# WebSocket API配置 (备用)
SPARK_APP_ID=你的APPID              # 例如：7beb3477
SPARK_API_SECRET=你的APISecret      # 例如：M2IwNGRjNDUwZGNkNGI4YjlhNjJmYTc0
SPARK_API_KEY=你的APIKey            # 例如：0dabd83d959010dac3d367a83522fe03

# 其他配置
SPARK_MODEL=generalv3.5  # 使用Max版本
SPARK_API_BASE=https://spark-api-open.xf-yun.com/v1
```

### 3. 重要说明

- **SPARK_API_PASSWORD**：这是HTTP API调用所需的唯一认证信息
- 请确保将完整的APIPassword填入，不要使用带星号的版本
- `.env`文件包含敏感信息，请勿提交到版本控制系统

### 4. 验证配置

配置完成后，重启Docker容器：

```bash
docker-compose down
docker-compose up -d
```

查看后端日志确认API调用正常：

```bash
docker-compose logs -f backend
```

如果配置正确，您应该能够正常使用AI功能，而不会看到401认证错误。 