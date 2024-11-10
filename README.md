<div align="center">

# Mio 澪
_✨ 基于 Nonebot2 的超可爱QBot ✨_
</div>

## 简介
澪(Mio) 基于Nonebot2 开发，用于群聊的机器人

## 功能简介
- 插件管理
- 插件帮助
- AI聊天（基于百度api）
- 扫雷
- 猜单词
- ...其他功能待更新

## 使用指南
Mio基于OneBot协议通信，需要使用其他项目作为NTQQ客户端进行使用，本人使用的是[NapCatQQ](https://github.com/NapNeko/NapCatQQ)，也可以使用其他支持OneBot协议的项目，例如[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

关于NapCatQQ的部署可以前往github的项目页进行查看，待NapCatQQ部署完成后，可以参考以下步骤部署本项目

### 部署步骤

> 这里提供一个基础的部署步骤，具体的操作需要根据不同系统与不同环境进行更改
>
> 建议提前准备环境 Python 3.10（建议使用conda进行管理）、Git

1. 输入以下命令克隆本仓库并安装依赖

```
git clone https://github.com/EienSakura/mio.git
cd mio
pip install -r requirements.txt
```

2. 进入`env.dev`，本文件为参考配置文件，具体参数可查看配置文件中注释，在启动mio前需要对本文件进行所需要的修改，如端口号等。如果有需要可以将本文件复制成`env.prod`（生产环境配置文件）再进行修改，同时需要修改文件`env`中的`ENVIRONMENT`为`prod`

3. 在完成以上步骤后，既可以通过以下命令直接启动mio

   ```
   python bot.py
   ```

   > 项目启动时为出现MIO图标，待看到`🚀 澪Mio 已启动...  `及`Uvicorn running on http://127.0.0.1:7000`，说明Mio已经启动，您可以忽略启动时的WARNING信息，但若出现ERROR，则可能代表部分插件加载失败，日志中会现实加载成功的插件和未加载成功的插件，您可以通过日志查询问题所在。

4. 如果一切无误，此时应该已经可以使用mio了

   您可以在群聊中尝试@mio，若机器人进行回复，则说明您已基本成功搭建了mio。

## 鸣谢
感谢以下 开发者 和 Github 项目对 Mio 作出的贡献，Mio在编写中使用或参考以下项目：
- [`nonebot/nonebot2`](https://github.com/nonebot/nonebot2)：跨平台Python异步机器人框架
- [`netsora/SoraBot`](https://github.com/netsora/SoraBot)：基于 Nonebot2 开发，互通多平台，超可爱的林汐酱
- [`MeetWq/mybot`](https://github.com/MeetWq/mybot)：基于 NoneBot 的QQ机器人，实现了一些乱七八糟的功能
- [`nonebot_plugin_saa`](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere)：多适配器消息发送支持
- [`nonebot_plugin_alconna`](https://github.com/nonebot/plugin-alconna)：强大的 Nonebot2 命令匹配拓展

...其他内容待书写