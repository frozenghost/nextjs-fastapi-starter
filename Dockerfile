#设置基础镜像
FROM node:20-alpine AS frontend

# 设置工作目录
WORKDIR /frontend

COPY . /frontend

# 安装前端依赖并构建前端应用
RUN npm install && npm run build

EXPOSE 3000

CMD ["yarn", "start", "-p", "3000"]