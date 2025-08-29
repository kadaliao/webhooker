from flask import Flask, request, jsonify, render_template_string
import json
import requests
from datetime import datetime

app = Flask(__name__)


def send_notification(message: str) -> bool:
    """
    发送通知消息到指定API

    Args:
        message (str): 要发送的消息内容

    Returns:
        bool: 发送成功返回True，失败返回False
    """
    api_url = f"https://api.day.app/tDr56uFdtFWFHpWmUaKtAZ/LSP-Warning/{message}"
    try:
        response = requests.get(api_url)
        print(f"已发送通知到API: {api_url}")
        print(f"API响应状态: {response.status_code}")
        return True
    except Exception as api_error:
        print(f"发送API请求失败: {str(api_error)}")
        return False


@app.route("/")
def index():
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webhooker - 粒子特效</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #0c0c0c, #1a1a2e, #16213e);
            overflow: hidden;
            height: 100vh;
            font-family: 'Arial', sans-serif;
        }

        #particles {
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: 1;
        }

        .content {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            color: #fff;
        }

        .title {
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
            animation: glow 2s ease-in-out infinite alternate;
        }

        .subtitle {
            font-size: 1.5rem;
            opacity: 0.8;
            margin-bottom: 2rem;
            color: #00ccff;
        }

        .info-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem;
            min-width: 300px;
        }

        .endpoint {
            color: #00ff88;
            font-family: monospace;
            font-size: 1.2rem;
            margin: 0.5rem 0;
        }

        @keyframes glow {
            from {
                text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
            }
            to {
                text-shadow: 0 0 30px rgba(0, 255, 255, 1), 0 0 40px rgba(0, 255, 255, 1);
            }
        }

        .particle {
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <canvas id="particles"></canvas>
    
    <div class="content">
        <h1 class="title">Webhooker</h1>
        <p class="subtitle">酷炫粒子特效 Webhook 服务</p>
        
        <div class="info-card">
            <h3>API 端点</h3>
            <div class="endpoint">POST /webhook</div>
            <div class="endpoint">GET /webhook</div>
            <p style="margin-top: 1rem; opacity: 0.7;">
                准备接收您的 webhook 请求！
            </p>
        </div>
    </div>

    <script>
        class ParticleSystem {
            constructor() {
                this.canvas = document.getElementById('particles');
                this.ctx = this.canvas.getContext('2d');
                this.particles = [];
                this.mousePos = { x: 0, y: 0 };
                
                this.resize();
                this.init();
                this.animate();
                
                window.addEventListener('resize', () => this.resize());
                window.addEventListener('mousemove', (e) => {
                    this.mousePos.x = e.clientX;
                    this.mousePos.y = e.clientY;
                });
            }
            
            resize() {
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
            }
            
            init() {
                const particleCount = Math.min(150, Math.floor(window.innerWidth * window.innerHeight / 8000));
                for (let i = 0; i < particleCount; i++) {
                    this.particles.push({
                        x: Math.random() * this.canvas.width,
                        y: Math.random() * this.canvas.height,
                        vx: (Math.random() - 0.5) * 2,
                        vy: (Math.random() - 0.5) * 2,
                        size: Math.random() * 3 + 1,
                        color: this.getRandomColor(),
                        opacity: Math.random() * 0.8 + 0.2,
                        trail: []
                    });
                }
            }
            
            getRandomColor() {
                const colors = [
                    '0, 255, 255',    // 青色
                    '0, 255, 136',    // 绿色
                    '255, 0, 255',    // 紫色
                    '255, 255, 0',    // 黄色
                    '0, 136, 255'     // 蓝色
                ];
                return colors[Math.floor(Math.random() * colors.length)];
            }
            
            updateParticle(particle) {
                // 鼠标吸引效果
                const dx = this.mousePos.x - particle.x;
                const dy = this.mousePos.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    const force = (150 - distance) / 150 * 0.5;
                    particle.vx += (dx / distance) * force * 0.1;
                    particle.vy += (dy / distance) * force * 0.1;
                }
                
                // 添加轨迹点
                particle.trail.push({ x: particle.x, y: particle.y });
                if (particle.trail.length > 10) {
                    particle.trail.shift();
                }
                
                // 更新位置
                particle.x += particle.vx;
                particle.y += particle.vy;
                
                // 边界检测
                if (particle.x < 0) {
                    particle.x = this.canvas.width;
                } else if (particle.x > this.canvas.width) {
                    particle.x = 0;
                }
                
                if (particle.y < 0) {
                    particle.y = this.canvas.height;
                } else if (particle.y > this.canvas.height) {
                    particle.y = 0;
                }
                
                // 速度衰减
                particle.vx *= 0.99;
                particle.vy *= 0.99;
            }
            
            drawParticle(particle) {
                // 绘制轨迹
                if (particle.trail.length > 1) {
                    for (let i = 1; i < particle.trail.length; i++) {
                        const alpha = (i / particle.trail.length) * particle.opacity * 0.5;
                        this.ctx.strokeStyle = `rgba(${particle.color}, ${alpha})`;
                        this.ctx.lineWidth = particle.size * 0.5;
                        this.ctx.beginPath();
                        this.ctx.moveTo(particle.trail[i - 1].x, particle.trail[i - 1].y);
                        this.ctx.lineTo(particle.trail[i].x, particle.trail[i].y);
                        this.ctx.stroke();
                    }
                }
                
                // 绘制粒子
                const gradient = this.ctx.createRadialGradient(
                    particle.x, particle.y, 0,
                    particle.x, particle.y, particle.size * 2
                );
                gradient.addColorStop(0, `rgba(${particle.color}, ${particle.opacity})`);
                gradient.addColorStop(1, `rgba(${particle.color}, 0)`);
                
                this.ctx.fillStyle = gradient;
                this.ctx.beginPath();
                this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                this.ctx.fill();
            }
            
            drawConnections() {
                for (let i = 0; i < this.particles.length; i++) {
                    for (let j = i + 1; j < this.particles.length; j++) {
                        const dx = this.particles[i].x - this.particles[j].x;
                        const dy = this.particles[i].y - this.particles[j].y;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance < 100) {
                            const opacity = (100 - distance) / 100 * 0.2;
                            this.ctx.strokeStyle = `rgba(0, 255, 255, ${opacity})`;
                            this.ctx.lineWidth = 0.5;
                            this.ctx.beginPath();
                            this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                            this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                            this.ctx.stroke();
                        }
                    }
                }
            }
            
            animate() {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                // 绘制连接线
                this.drawConnections();
                
                // 更新和绘制粒子
                for (const particle of this.particles) {
                    this.updateParticle(particle);
                    this.drawParticle(particle);
                }
                
                requestAnimationFrame(() => this.animate());
            }
        }
        
        // 等待页面加载完成后初始化粒子系统
        window.addEventListener('DOMContentLoaded', () => {
            new ParticleSystem();
        });
    </script>
</body>
</html>
    """
    return render_template_string(html_content)


@app.route("/webhook", methods=["POST"])
def handle_webhook():
    try:
        # 获取请求时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 获取客户端IP
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        # 记录基本请求信息
        print("=" * 50)
        print(f"Webhook接收时间: {timestamp}")
        print(f"客户端IP: {client_ip}")
        print(f"请求方法: {request.method}")
        print(f"请求URL: {request.url}")

        # 记录请求头
        print("请求头:")
        for header, value in request.headers:
            print(f"{header}: {value}")

        # 获取请求体
        try:
            if request.is_json:
                data = request.get_json()
                print("JSON数据:")
                print(json.dumps(data, indent=2, ensure_ascii=False))

                message = data.get("data", {}).get("message")
                if message:
                    send_notification(message)
                else:
                    print("JSON数据中没有message字段")
            else:
                raw_data = request.get_data(as_text=True)
                print("原始数据:")
                print(raw_data)
        except Exception as e:
            print(f"数据解析错误: {str(e)}")
            raw_data = request.get_data(as_text=True)
            print(f"原始数据: {raw_data}")

        print("=" * 50)

        # 返回成功响应
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Webhook received successfully",
                    "timestamp": timestamp,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"处理webhook时发生错误: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@app.route("/webhook", methods=["GET"])
def webhook_info():
    return jsonify(
        {
            "message": "Webhook endpoint is ready",
            "methods": ["POST"],
            "endpoint": "/webhook",
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=9000)
