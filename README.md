# Desktop Sayon | 桌面纱夜

A cute desktop pet that periodically captures screenshots and engages in AI-powered conversations based on what you're doing.

一个可爱的桌面宠物，会定期截取屏幕截图并基于你正在做的事情进行AI对话。

![demo](assets/demo.png)

## ✨ Features | 功能特性

- **Semi-transparent avatar** stays on top, positioned at bottom-right corner
- **Auto screenshot & AI chat** at random intervals using exponential distribution
- **Click interaction** - click avatar to trigger immediate conversation
- **Drag to move** - long press (>0.3s) to drag the pet to any position
- **Smart fade effect** - avatar disappears during screenshot, then reappears
- **Conversation history** saved to local files

- **半透明头像**始终置顶显示，默认位于屏幕右下角
- **自动截图对话**按指数分布的随机间隔进行AI聊天
- **点击交互** - 点击头像立即触发对话
- **拖拽移动** - 长按(>0.3秒)可拖拽宠物到任意位置
- **智能淡出效果** - 截图时头像消失，完成后立即恢复
- **对话历史**自动保存到本地文件

## 🚀 Quick Start | 快速开始

1. **Setup environment | 环境配置**
   ```bash
   # Run setup script | 运行配置脚本
   setup.bat
   ```

2. **Configure API key | 配置API密钥**

   Copy `config/config.ini.template` to `config/config.ini` and set your `LLM_KEY`
   
   将`config/config.ini.template`复制为`config/config.ini`文件，设置你的 `LLM_KEY`

3. **Launch the pet | 启动宠物**
   ```bash
   # Start | 启动
   start.bat
   ```

4. **Create desktop shortcut | 创建桌面快捷方式**
   ```bash
   # Create desktop shortcut with custom icon | 创建带自定义图标的桌面快捷方式
   cd scripts
   shortcut.bat
   ```

## ⚙️ Configuration | 配置选项

Edit `config/config.ini`:

编辑 `config/config.ini` 文件：

```ini
[AVATAR]
AVATAR_HEIGHT=200              # Avatar height in pixels | 头像高度（像素）
AVATAR_TRANSPARENCY=0.3        # Transparency level (0.0-1.0) | 透明度（0.0-1.0）

[TIMING]
DIALOG_INTERVAL=10             # Mean auto-chat interval (minutes) | 自动对话平均间隔（分钟）
TEXT_DISPLAY_TIME=0.15         # Text display duration (minutes) | 文字显示时长（分钟）

[LLM]
LLM_URL=https://api-inference.modelscope.cn/v1
LLM_MODEL=Qwen/Qwen2.5-VL-72B-Instruct
LLM_KEY=your_api_key_here      # Your API key | 你的API密钥
```

## 🎮 Controls | 操作方式

- **Short click** (<0.3s): Trigger immediate conversation | **短按**（<0.3秒）：立即触发对话
- **Long press** (>0.3s): Drag to move position | **长按**（>0.3秒）：拖拽移动位置
- **Text box**: Click-through, won't trigger actions | **文本框**：点击无效果，不会触发操作

## 📁 File Structure (Simplified) | 文件结构（简化版）

```
desktop-sayon/
├── assets/
│   └── portrait.png          # Avatar image | 头像图片
├── config/
│   ├── config.ini           # Configuration | 配置文件
│   └── system_prompt.txt    # AI system prompt | AI系统提示
├── record/
│   ├── images/screen.png    # Latest screenshot | 最新截图
│   └── text/dialogue.txt   # Conversation history | 对话历史
├── src/main.py              # Main application | 主程序
├── setup.bat                # Setup script | 配置脚本
└── start.bat                # Launch script | 启动脚本
```

## 🛠️ Requirements | 系统要求

- **Python 3.7+**
- **Windows OS** with PowerShell
- **Internet connection** for AI API calls
- **API key** for the configured LLM service

- **Python 3.7+**
- **Windows系统**及PowerShell
- **网络连接**用于AI API调用
- 配置的LLM服务的**API密钥**

## 🎨 Customization | 自定义

- **Change avatar**: Replace `assets/portrait.png` (transparent background required)
- **Modify personality**: Edit `config/system_prompt.txt`
- **Adjust appearance**: Modify transparency and size in config file

- **更换头像**：替换 `assets/portrait.png`（需要透明背景）
- **修改个性**：编辑 `config/system_prompt.txt`
- **调整外观**：在配置文件中修改透明度和大小

## 📝 License | 许可证

[MIT License](https://opensource.org/licenses/MIT)
