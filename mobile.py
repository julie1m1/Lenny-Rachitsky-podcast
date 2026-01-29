from pathlib import Path
import re

# ========== 设置文件夹路径 ==========
html_folder = Path("E:\99\lenny rachitsky transcripts\pages")  # ← 改成你的文件夹路径

# ========== 要插入的 CSS 代码 ==========
css_to_insert = """/* 针对屏幕宽度小于 768px 的设备（手机、部分平板） */
@media (max-width: 768px) {
    /* 1. 将 body 的 display 改为 block，解除桌面端的 flex 布局 */
    body {
        display: block;
        height: auto; /* 允许纵向滚动 */
        overflow-y: visible; /* 恢复滚动条 */
    }

    /* 2. 隐藏左侧和右侧栏 */
    .sidebar-left, .sidebar-right {
        display: none;
    }

    /* 3. 调整主内容区，充满屏幕并移除固定宽度/边距限制 */
    .main {
        padding: 20px; /* 缩小移动端的内边距 */
        width: 100%;
        box-sizing: border-box; /* 确保 padding 不撑破屏幕 */
        overflow-y: visible; /* 让整体 body 滚动，而不是单独区域 */
    }

    /* 4. 优化：让内部卡片宽度自适应 */
    .paragraph-wrap, details.summary-box {
        padding: 15px; /* 适当减少内边距 */
        margin-bottom: 20px;
        width: 100%;
        box-sizing: border-box;
    }

    /* 5. 优化：调整文字大小（可选） */
    .paragraph, .sum-point {
        font-size: 17px; /* 移动端稍细的文字感观更好 */
    }
}"""

# ========== 查找所有 HTML 文件 ==========
html_files = list(html_folder.glob("*.html"))

print(f"📁 找到 {len(html_files)} 个 HTML 文件")

# ========== 批量处理每个文件 ==========
for i, html_file in enumerate(html_files, 1):
    print(f"\n🔄 正在处理 ({i}/{len(html_files)}): {html_file.name}")
    
    # 步骤1：读取文件内容
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 步骤2：在 <head> 后面添加 viewport meta 标签
    content = re.sub(
        r'(<head[^>]*>)',
        r'\1\n<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        content,
        count=1,
        flags=re.IGNORECASE
    )
    
    # 步骤3：在 </style> 前面添加 CSS 媒体查询
    # 使用 re.escape 处理 CSS 中的特殊字符，但这里用字符串替换更稳妥
    content = re.sub(
        r'(</style>)',
        lambda m: css_to_insert + '\n' + m.group(1),
        content,
        count=1,
        flags=re.IGNORECASE
    )
    
    # 步骤4：直接保存回源文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ 完成")

print(f"\n🎉 全部完成！共处理 {len(html_files)} 个文件")