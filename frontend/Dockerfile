# 构建阶段
FROM node:18 as build-stage

# 设置工作目录
WORKDIR /app

# 复制所有前端文件
COPY . .

# 安装依赖
RUN npm ci --silent

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:1.21-alpine as production-stage

# 复制构建产物到Nginx默认目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx/nginx.conf /etc/nginx/conf.d/app.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]

## 构建阶段
#FROM node:18 as build-stage
#
## 设置工作目录
#WORKDIR /app
#
## 复制所有前端文件
#COPY . .
#
## 安装依赖
#RUN npm ci --silent
#
## 构建应用
#RUN npm run build -- --mode production
#
## 生产阶段
#FROM nginx:1.21-alpine as production-stage
#
## 复制构建产物
#COPY --from=build-stage /app/dist /usr/share/nginx/html
#
## 复制Nginx配置 - 直接从构建阶段复制
#COPY --from=build-stage /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
#
## 设置时区
#RUN apk add --no-cache tzdata && \
#    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
#    echo "Asia/Shanghai" > /etc/timezone
#
## 暴露端口
#EXPOSE 80
#
## 启动Nginx
#CMD ["nginx", "-g", "daemon off;"]