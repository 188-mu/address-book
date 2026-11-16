# table.py
from rich.console import Console
from rich.table import Table

# 创建控制台对象
console = Console()

# 创建表格，设置标题
table = Table(title="通讯录")

# 添加表头列
table.add_column("姓名")
table.add_column("电话")
table.add_column("备注")

# 添加数据行
table.add_row("张三", "13800138000", "同学")
table.add_row("李四", "13900139000", "家人")

# 打印表格
console.print(table)