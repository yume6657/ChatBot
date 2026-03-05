#!/usr/bin/env python
"""
DeepSeek智能对话系统 - 安装和配置脚本
"""

import os
import sys
import subprocess

def run_command(command, description):
    """运行命令并显示进度"""
    print(f"正在{description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✓ {description}完成")
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        sys.exit(1)

def main():
    print("=== DeepSeek智能对话系统安装向导 ===\n")
    
    # 1. 检查Python版本
    print("1. 检查Python版本...")
    if sys.version_info < (3, 8):
        print("✗ 需要Python 3.8或更高版本")
        sys.exit(1)
    print("✓ Python版本检查通过")
    
    # 2. 安装依赖
    run_command("pip install -r requirements.txt", "安装Python依赖")
    
    # 3. 创建环境配置文件
    print("3. 创建环境配置文件...")
    if not os.path.exists('.env'):
        with open('.env.example', 'r') as example_file:
            with open('.env', 'w') as env_file:
                env_file.write(example_file.read())
        print("✓ 已创建.env文件，请编辑该文件配置您的设置")
    else:
        print("✓ .env文件已存在")
    
    # 4. 数据库迁移
    run_command("python manage.py makemigrations", "创建数据库迁移文件")
    run_command("python manage.py migrate", "执行数据库迁移")
    
    # 5. 创建超级用户
    print("5. 创建超级用户（可选）...")
    create_superuser = input("是否创建超级用户？(y/n): ").lower().strip()
    if create_superuser == 'y':
        run_command("python manage.py createsuperuser", "创建超级用户")
    
    print("\n=== 安装完成 ===")
    print("\n下一步操作：")
    print("1. 编辑 .env 文件，配置您的DeepSeek API密钥和数据库设置")
    print("2. 运行 'python manage.py runserver' 启动开发服务器")
    print("3. 访问 http://127.0.0.1:8000 查看应用")

if __name__ == "__main__":
    main()