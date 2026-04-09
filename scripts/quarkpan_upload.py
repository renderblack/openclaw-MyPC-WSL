# -*- coding: utf-8 -*-
"""
夸克网盘上传脚本
"""
import os
import sys

os.system('chcp 65001 > nul 2>&1')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from quark_client import QuarkClient
from pathlib import Path

# 文件路径
FILE_PATH = r"G:\动画组共享\动画项目\2020\09-外部-上海机场线\06-成片\中铁二十四局集团上海机场联络线1标 项目介绍（20201223最终版修改）.mp4"
PARENT_FOLDER_ID = "0"  # 上传到根目录

class ProgressTracker:
    def __init__(self, total_size):
        self.total = total_size
        self.last_percent = 0
        
    def callback(self, uploaded, total):
        """上传进度回调"""
        # 处理不同的参数类型
        try:
            uploaded_mb = int(uploaded) / (1024 * 1024) if isinstance(uploaded, (int, float)) else 0
            total_mb = int(total) / (1024 * 1024) if isinstance(total, (int, float)) else self.total / (1024 * 1024)
            
            if total_mb > 0:
                percent = (uploaded_mb / total_mb) * 100
            else:
                percent = 0
                
            if percent - self.last_percent >= 5:  # 每5%报告一次
                print(f"\r上传进度: {percent:.1f}% ({uploaded_mb:.1f} MB)", end='', flush=True)
                self.last_percent = percent
        except:
            pass

def upload_with_progress():
    file_size = os.path.getsize(FILE_PATH)
    
    print("="*60)
    print("夸克网盘上传")
    print("="*60)
    print(f"文件: {Path(FILE_PATH).name}")
    print(f"大小: {file_size / (1024**3):.2f} GB")
    print()
    
    tracker = ProgressTracker(file_size)
    
    try:
        with QuarkClient() as client:
            if not client.is_logged_in():
                print("未登录!")
                return False
            
            print("已登录，开始上传...")
            print("-"*40)
            
            # 使用上传服务
            result = client.upload.upload_file(
                file_path=FILE_PATH,
                parent_folder_id=PARENT_FOLDER_ID,
                progress_callback=tracker.callback
            )
            
            print()
            print("-"*40)
            
            # 解析结果
            if result.get('status') == 200 or result.get('code') == 0:
                data = result.get('data', {})
                file_id = data.get('file_id', '')
                print(f"上传成功!")
                print(f"文件ID: {file_id}")
                
                # 生成分享链接
                print("\n正在生成分享链接...")
                share_result = client.shares.create_share(
                    file_ids=[file_id],
                    title=Path(FILE_PATH).name,
                    expire_days=7,  # 7天有效期
                    password=""  # 无密码
                )
                
                if share_result.get('status') == 200 or share_result.get('code') == 0:
                    share_data = share_result.get('data', {})
                    share_url = share_data.get('share_url', '')
                    share_pwd = share_data.get('password', '')
                    
                    print(f"\n" + "="*60)
                    print("分享链接已生成!")
                    print("="*60)
                    print(f"链接: {share_url}")
                    if share_pwd:
                        print(f"密码: {share_pwd}")
                    print("="*60)
                    
                    # 保存链接
                    with open(r'C:\Users\Administrator\.openclaw\workspace\config\last_share.txt', 'w', encoding='utf-8') as f:
                        f.write(f"文件: {Path(FILE_PATH).name}\n")
                        f.write(f"链接: {share_url}\n")
                        if share_pwd:
                            f.write(f"密码: {share_pwd}\n")
                    
                    return True
                else:
                    print("生成分享链接失败:", share_result)
                    return False
            else:
                print(f"上传失败: {result}")
                return False
                
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = upload_with_progress()
    sys.exit(0 if success else 1)
