# Webhooker

简单的 Python webhook 接收服务。

## 快速开始

```bash
# 克隆并运行
git clone https://github.com/kadaliao/webhooker.git
cd webhooker
uv sync
uv run python api/app.py
```

服务运行在 `http://localhost:9000`

## 测试

```bash
# 发送测试请求
curl -X POST http://localhost:9000/webhook \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

## 部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/import/git?s=https://github.com/kadaliao/webhooker)

## API

- `POST /webhook` - 接收 webhook 数据
- `GET /webhook` - 端点状态

接收到的请求会在控制台打印详细信息。