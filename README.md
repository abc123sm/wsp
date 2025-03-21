# wsp（WEB SRT Processor）

处理web提取的日文srt字幕

通过AI+一点人工修改[tap（处理ass字幕的）](https://github.com/MingYSub/Tap)而成，因为主要是自用，所以把一些config都去了，然后加了几条正则

## 功能

- ⭐ 合并时间重复行
- 🔊 去除语气词
- ⚙️ 输出设置
  - 支持格式： `txt` `ass` `srt`
  - 行尾追加字符
  - 输出说话人
  - 停顿提示
- 🔄 全半角转换
  - 全角英数转为半角
  - 半角片假名转为全角
- 📏 日文和西文之间添加空格
- 🧹 删除多余信息
  - 去除位置、颜色等信息
  - 删除未识别的外字
- ✅ 整理重复音节
- 📂 批量转换
- 去除汉字假名标注

## 样例

### 原文（节选）

```
17
00:02:45,415 --> 00:02:47,458
うん… ん？

18
00:02:48,459 --> 00:02:53,464
～♪

19
00:03:02,265 --> 00:03:03,391
（エリス）フフッ

20
00:03:04,392 --> 00:03:06,686
（魔族）だから
なんで俺たちの通行料だけ⸺

21
00:03:06,769 --> 00:03:09,564
こんなに高いんだ おかしいだろ！

22
00:03:09,647 --> 00:03:12,442
（役人）そんなこと言われてもなあ

23
00:03:13,318 --> 00:03:14,944
（魔族）んぐぐぐ…

24
00:03:18,948 --> 00:03:21,910
（神殿騎士）そこの魔族
武器を捨てろ
```

### 处理后文本

```
8
00:02:28,523 --> 00:02:31,109
うっ！　ふん！

9
00:02:45,415 --> 00:02:47,458
うん…

10
00:03:04,392 --> 00:03:06,686
だから　なんで俺たちの通行料だけ⸺

11
00:03:06,769 --> 00:03:09,564
こんなに高いんだ　おかしいだろ！

12
00:03:09,647 --> 00:03:12,442
そんなこと言われてもなあ

13
00:03:13,318 --> 00:03:14,944
んぐぐぐ…

14
00:03:18,948 --> 00:03:21,910
そこの魔族　武器を捨てろ
```
