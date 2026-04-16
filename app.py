from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
import base64
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showcase')
def showcase():
    return render_template('showcase.html')

@app.route('/restore')
def restore():
    return render_template('restore.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': '文件上传成功'
        })
    
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/api/restore', methods=['POST'])
def restore_image():
    try:
        data = request.json
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': '缺少文件名'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': '文件不存在'}), 404
        
        # 确保 uploads 目录存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        with open(filepath, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        try:
            # 使用 Hugging Face Inference API
            hf_api_key = os.environ.get('HUGGING_FACE_API_KEY')
            hf_model = "stabilityai/stable-diffusion-2-upscale"
            
            if not hf_api_key:
                print("Hugging Face API 密钥未设置，使用本地修复")
                raise Exception("API 密钥未设置")
            
            print(f"开始调用 Hugging Face API，文件：{filename}")
            
            # 读取图片并编码为 base64
            with open(filepath, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{hf_model}",
                headers={
                    'Authorization': f'Bearer {hf_api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'inputs': image_data
                },
                timeout=60  # 增加超时时间
            )
            
            print(f"Hugging Face API 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                restored_filename = f"restored_{filename}"
                restored_filepath = os.path.join(app.config['UPLOAD_FOLDER'], restored_filename)
                
                print(f"保存修复后图片：{restored_filepath}")
                
                with open(restored_filepath, 'wb') as f:
                    f.write(response.content)
                
                return jsonify({
                    'success': True,
                    'restored_filename': restored_filename,
                    'message': '图片修复成功（Hugging Face）'
                })
            
            # 处理 API 错误，直接使用本地模拟修复
            print(f"API 调用失败，状态码: {response.status_code}，使用本地模拟修复")
            
        except Exception as e:
            print(f"API调用失败，使用本地模拟修复: {str(e)}")
        
        # 执行本地图片修复
        try:
            from PIL import Image, ImageEnhance, ImageFilter
            
            restored_filename = f"restored_{filename}"
            restored_filepath = os.path.join(app.config['UPLOAD_FOLDER'], restored_filename)
            
            # 确保 uploads 目录存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            print(f"开始本地图片修复，目标路径：{restored_filepath}")
            
            # 打开原始图片
            with Image.open(filepath) as img:
                # 转换为 RGB 模式
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 1. 降噪处理 - 使用中值滤波
                img = img.filter(ImageFilter.MedianFilter(size=3))
                
                # 2. 调整亮度和对比度
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.2)  # 增加20%亮度
                
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.3)  # 增加30%对比度
                
                # 3. 颜色平衡 - 调整色阶
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.1)  # 轻微增强色彩
                
                # 4. 锐化处理 - 更强烈的锐化
                img = img.filter(ImageFilter.SHARPEN)
                img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=200, threshold=2))
                
                # 5. 细节增强 - 使用边缘增强
                img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
                
                # 保存修复后的图片
                img.save(restored_filepath, quality=95)
            
            print(f"本地图片修复成功：{restored_filename}")
            
            return jsonify({
                'success': True,
                'restored_filename': restored_filename,
                'message': '图片修复成功（本地修复）'
            })
        except Exception as local_error:
            print(f"本地修复失败: {str(local_error)}")
            # 如果修复失败，退回到简单复制
            try:
                import shutil
                shutil.copy(filepath, restored_filepath)
                return jsonify({
                    'success': True,
                    'restored_filename': restored_filename,
                    'message': '图片修复成功（简单复制）'
                })
            except:
                return jsonify({'error': f'本地修复失败: {str(local_error)}'}), 500
            
    except Exception as e:
        print(f"服务器错误: {str(e)}")
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        try:
            api_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
            api_key = os.environ.get('DASHSCOPE_API_KEY', 'sk-03df816b15a64616ad000795cf30afce')
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "qwen-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一位专业的中国非物质文化遗产专家，精通剪纸、昆曲、皮影、木雕等传统艺术。请用专业、准确、生动的语言回答用户关于非遗文化的问题。"
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                
                return jsonify({
                    'success': True,
                    'reply': reply
                })
            else:
                return jsonify({'error': f'API调用失败: {response.status_code}'}), 500
                
        except Exception as e:
            return jsonify({'error': f'问答服务异常: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/heritage-data', methods=['GET'])
def get_heritage_data():
    heritage_data = {
        "剪纸": {
            "name": "剪纸艺术",
            "description": "中国剪纸是一种用剪刀或刻刀在纸上剪刻花纹，用于装点生活或配合其他民俗活动的民间艺术。2009年入选联合国教科文组织非物质文化遗产名录。",
            "history": "剪纸艺术起源于汉代，至今已有2000多年历史。唐代剪纸已用于装饰，宋代达到鼎盛，明清时期更加普及。",
            "techniques": ["折叠剪法", "阴刻阳刻", "套色剪纸", "立体剪纸"],
            "regions": ["河北蔚县", "山西广灵", "江苏扬州", "浙江乐清"],
            "images": [
                {"title": "传统窗花", "description": "春节贴窗花是传统习俗", "image_url": "/static/images/paper-cutting/window-decoration.jpg"},
                {"title": "生肖剪纸", "description": "十二生肖主题剪纸", "image_url": "/static/images/paper-cutting/zodiac.jpg"},
                {"title": "婚庆剪纸", "description": "婚礼装饰用剪纸", "image_url": "/static/images/paper-cutting/wedding.jpg"}
            ]
        },
        "昆曲": {
            "name": "昆曲艺术",
            "description": "昆曲是中国最古老的剧种之一，被称为'百戏之祖'。2001年入选联合国教科文组织首批非物质文化遗产名录。",
            "history": "昆曲发源于14世纪的苏州昆山，明代魏良辅改良后形成昆腔，清代达到鼎盛。",
            "techniques": ["唱腔艺术", "身段表演", "脸谱化妆", "服饰道具"],
            "regions": ["江苏苏州", "浙江杭州", "上海", "北京"],
            "images": [
                {"title": "牡丹亭", "description": "昆曲经典剧目", "image_url": "/static/images/kunqu/peony-pavilion.jpg"},
                {"title": "长生殿", "description": "历史题材名剧", "image_url": "/static/images/kunqu/longevity-hall.jpg"},
                {"title": "桃花扇", "description": "爱情悲剧代表作", "image_url": "/static/images/kunqu/peach-blossom-fan.jpg"}
            ]
        },
        "皮影": {
            "name": "皮影戏",
            "description": "皮影戏是中国民间古老的传统艺术，老北京人都叫它'驴皮影'。2011年入选联合国教科文组织非物质文化遗产名录。",
            "history": "皮影戏始于西汉，兴于唐宋，盛于明清，元代传入西亚，18世纪传入欧洲。",
            "techniques": ["皮影制作", "操纵表演", "唱腔艺术", "灯光效果"],
            "regions": ["陕西华县", "河北唐山", "山西孝义", "四川成都"],
            "images": [
                {"title": "传统皮影", "description": "精美的皮影人物造型", "image_url": "/static/images/shadow-puppet/traditional.jpg"},
                {"title": "皮影舞台", "description": "传统皮影戏台", "image_url": "/static/images/shadow-puppet/stage.jpg"},
                {"title": "皮影道具", "description": "各种皮影道具", "image_url": "/static/images/shadow-puppet/props.jpg"}
            ]
        },
        "木雕": {
            "name": "木雕艺术",
            "description": "木雕是雕塑的一种，在我们国家常常被称为'民间工艺'。2006年入选第一批国家级非物质文化遗产名录。",
            "history": "木雕艺术起源于新石器时代，商周时期已有精湛工艺，明清达到艺术高峰。",
            "techniques": ["浮雕", "圆雕", "镂空雕", "透雕"],
            "regions": ["浙江东阳", "福建莆田", "广东潮州", "江苏苏州"],
            "images": [
                {"title": "东阳木雕", "description": "浙江东阳传统木雕", "image_url": "/static/images/wood-carving/dongyang.jpg"},
                {"title": "建筑木雕", "description": "古建筑木雕装饰", "image_url": "/static/images/wood-carving/architecture.jpg"},
                {"title": "家具木雕", "description": "传统家具雕刻", "image_url": "/static/images/wood-carving/furniture.jpg"}
            ]
        }
    }
    
    return jsonify(heritage_data)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000,host='0.0.0.0')
