# 设置基础镜像
FROM node:14-alpine

# 设置工作目录
WORKDIR /app

# 将 package.json 和 package-lock.json 复制到工作目录
COPY package*.json ./

# 安装依赖
RUN npm install

# 将其他文件复制到工作目录
COPY . .

# 构建生产应用
RUN npm run build

# 暴露端口
EXPOSE 3000

# 运行应用
CMD ["npm", "start"]