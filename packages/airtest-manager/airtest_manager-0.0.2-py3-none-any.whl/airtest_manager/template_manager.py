import os
import requests
from airtest.core.api import Template

class TemplateManager:
    def __init__(self):
        self.url_to_file_map = {}

    def get_template(self, url, **kwargs):
        # 检查 URL 是否是本地文件地址
        if os.path.isfile(url):
            local_file = url
        elif url in self.url_to_file_map:
            local_file = self.url_to_file_map[url]
        else:
            # 下载图片到本地
            local_file = self.download_image(url)
            self.url_to_file_map[url] = local_file

        return Template(local_file, **kwargs)

    def download_image(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            # 获取文件名
            file_name = os.path.basename(url)
            local_path = os.path.join(os.getcwd(), file_name)  # 保存到当前工作目录
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return local_path
        else:
            raise Exception(f"Failed to download image from {url}")

# 使用示例
# template_manager = TemplateManager()
# click_tab_all_product = template_manager.get_template('http://example.com/path/to/tab全部产品.png', rgb=True)