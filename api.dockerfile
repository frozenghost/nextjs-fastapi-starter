# 设置基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 复制到工作目录
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录复制到工作目录
COPY . .

# 暴露端口
EXPOSE 8000

# 运行应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]