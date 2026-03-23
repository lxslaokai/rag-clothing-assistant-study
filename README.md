# RAG 服装客服问答助手学习复现项目

这是我为了准备复试、系统学习 RAG 与大模型应用开发而完成的一个学习复现项目。

## 项目说明 Project Overview

本仓库记录了我在学习过程中对黑马程序员 B 站课程《黑马程序员大模型 RAG 与 Agent 智能体项目实战教程》的复现过程。
- 视频链接（bilibili）：[点击查看](https://www.bilibili.com/video/BV1yjs2SBLEx)  
- 本项目仅用于学习和复现，不用于商业用途

复现目标：复习复试知识 + 掌握 RAG + 大模型应用实战

## 项目目录结构
rag-clothing-assistant-study/
├─ rag-clothing-customer-service/ # Streamlit 页面代码
├─ data/ # 知识库文件
├─ assets/ # 界面截图与示例图片
├─ requirements_fixed.txt # 项目依赖
├─ README.md # 项目说明
├─ docs/interview-notes.md # 面试笔记


## 环境与运行

### 环境要求
- Python >= 3.10  
- 建议使用虚拟环境（venv 或 conda）

### 安装依赖
```bash
pip install -r requirements_fixed.txt
启动项目
streamlit run app_qa.py

浏览器打开 http://localhost:8501
 即可访问问答助手界面。
![系统界面](assets/Home_Page.png)

示例问题与系统回答

用户可以尝试以下问题（示例）：

衣服尺码问题
我身高180cm，体重70kg，适合穿多大码？
![示例1](assets/ex_1.png)

学习复现说明
所有代码均为本人复现
不代表官方版本
复现过程记录了运行步骤、问题与解决方案
主要目的是为了复试知识掌握和实践 RAG + 大模型应用
注意事项
本仓库仅作学习和复习用途，请勿用于商业用途
使用前请配置 .env 文件（API Key）