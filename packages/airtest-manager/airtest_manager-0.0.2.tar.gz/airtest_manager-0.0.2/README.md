# airtest_manager

## 安装

使用pip安装：

```bash
pip install airtest_manager
```

## 使用 

```bash
from airtest_manager import TemplateManager

template_manager = TemplateManager()
click_tab_all_product = template_manager.get_template('http://example.com/path/to/tab.png', rgb=True)
```