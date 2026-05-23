# 使用官方Python运行时作为基础镜像
FROM python:3.10-slim-buster

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 创建工作目录
WORKDIR /app


# 确保日志目录存在
RUN mkdir -p /app/logs

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 复制项目文件
COPY . .

# 在 collectstatic 之前添加权限设置
RUN mkdir -p /app/static
RUN chown -R www-data:www-data /app/static

# 收集静态文件
RUN python manage.py collectstatic --noinput --clear
RUN chmod -R 755 /app/static

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]