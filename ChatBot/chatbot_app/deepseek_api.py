import requests
import json
from django.conf import settings
from django.core.cache import cache


class DeepSeekAPI:
    """DeepSeek API 对接类"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def send_message(self, messages, model="deepseek-chat", max_tokens=2048, temperature=0.7):
        """发送消息到DeepSeek API"""
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'content': result['choices'][0]['message']['content'],
                    'tokens_used': result['usage']['total_tokens'],
                    'response': result
                }
            else:
                return {
                    'success': False,
                    'error': f"API请求失败: {response.status_code} - {response.text}",
                    'status_code': response.status_code
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'API请求超时'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'网络请求错误: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'未知错误: {str(e)}'
            }
    
    def estimate_tokens(self, text):
        """估算文本的token数量（简单估算）"""
        return len(text) // 4
    
    def get_models(self):
        """获取可用的模型列表"""
        cache_key = 'deepseek_models'
        models = cache.get(cache_key)
        
        if models is None:
            try:
                response = requests.get(
                    'https://api.deepseek.com/v1/models',
                    headers=self.headers,
                    timeout=10
                )
                if response.status_code == 200:
                    models_data = response.json()
                    models = [model['id'] for model in models_data.get('data', [])]
                    cache.set(cache_key, models, 3600)  # 缓存1小时
                else:
                    models = ['deepseek-chat', 'deepseek-coder']
            except:
                models = ['deepseek-chat', 'deepseek-coder']
        
        return models