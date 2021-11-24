# TodayInACGNHistory
历史上的今天二次元版，先开个坑，并不知道怎么弄到资料。

## 食用方法
json or markdown

## 如何添加内容
编辑对应日期的markdown文件，格式如下：
* 一级标题：{年份} - {事件标题}
* 接下来的内容可以像任何markdown一样书写，只是不能再使用一级标题（这恒河里）
* 标准markdown不支持的内容（例如音频、视频等等）需要**顶行**放在最后一个toml的代码块里(must start with "```toml")，但我也没想好会有些什么样的key，目前感觉一个attachment可以搞定，一个sample：
  ```toml
  [[attachment]]
  name = "Todokanai_Koi"
  description = """届かない恋
  歌：上原玲奈
  须谷尚子（作词）
  石川真也（作曲#1）
  松冈纯也（作曲#2）"""
  path = "../../static/music/Todokanai Koi.m4a"
  copyright = "F.I.X.RECORDS"

  [[attachment]]
  name = "cover:Todokanai_Koi"
  description = "cover"
  path = "../../static/img/Todokanai_koi.jpg"
  copyright = "F.I.X.RECORDS"
  ```