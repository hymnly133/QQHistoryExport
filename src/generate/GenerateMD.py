import json
import time
import os
import traceback
from PIL import Image
import sys
import io


class Generator:

    def __init__(self, log):
        self.log = log
        self.paths = {
            "fontDirPath": "resources/fonts/",
            "sourceDirPath": "D:/output_QHE/",
            "outputFilename": "我与小黄",
            "outputPath": "C:/Users/13363/Documents/OB/Sets/MdgeneTest/mds/"
        }
        self.lastMonth = ""
        self.lastDay = ""
        self.lastTime = 0
        self.timeShowSpan = 180
        self.changeMsgSpan = 600
        self.lastSender = 0
        self.timeInit = True
        self.senderInit = True
        self.monthInit = True
        self.dayInit = True
        self.senderNames = ["None", "You", "Me"]
        self.senderQQs = ["None", "3536928786", "1336325450"]
        self.senderDir = "senders/"
        self.imagesDir = "images/"
        self.videoDir = "videos/"
        self.emojiDir = "emoticons/emoticon1/new/"
        self.fileInd = -1
        self.lastChangedMegInd = -1
        self.maxW = 150
        self.maxH = 300
        self.qqemojiSize = 20
        self.currentMsgInd = 0
        self.toEnter = 0
        self.enableUselessTips = True
        self.voiceDir = "voices/"

    def checkSender(self, sender):
        if sender != self.lastSender or self.senderInit:
            self.lastSender = sender
            self.writeSender()
            self.senderInit = False
        pass

    def checkInd(self):
        if int(self.currentMsgInd / self.changeMsgSpan) != self.fileInd:
            if self.fileInd != -1:
                self.file.close()
            self.fileInd += 1
            newfilename = self.paths["outputPath"] + self.paths["outputFilename"] + "_" + str(self.fileInd) + ".md"
            dir = os.path.dirname(newfilename)
            if not os.path.exists(dir):
                os.mkdir(dir)

            if os.path.exists(newfilename):
                os.remove(newfilename)

            self.file = open(newfilename, "w", encoding="UTF-8")

            self.timeInit = True
            self.dayInit = True
            self.monthInit = True
            self.senderInit = True
        pass

    def resize_image(self, original_width, original_height, maxW, maxH):
        # 计算原始图片的宽高比
        img_ratio = original_width / original_height
        max_ratio = maxW / maxH

        if max_ratio >= img_ratio:
            new_width = maxW
            new_height = maxW / img_ratio
        else:
            new_height = maxH
            new_width = maxH * img_ratio

        new_width = min(new_width, original_width)
        new_height = min(new_height, original_height)

        return int(new_width), int(new_height)

    def convertToSourcePath(self,filepath):
        return filepath.replace("output\\",self.paths["sourceDirPath"])
    def formantImgHtml(self, filepath: str, maxW, maxH):
        filepath = self.convertToSourcePath(filepath)
        w, h = Image.open(filepath).size  # 宽高
        newW, newH = self.resize_image(w, h, maxW, maxH)
        text = ("<img src=\"{path}\" width=\"{width}\" height=\"{height}\">"
                .format(path=filepath, width=newW, height=newH))
        return text

    def writeImg(self, obj, inline=False):

        filename = self.paths["sourceDirPath"] + self.imagesDir + os.path.basename(obj["path"])

        if inline:
            self.file.write(self.formantImgHtml(filename, self.maxW, self.maxH))
        else:
            self.writeHtmlBlockText(self.formantImgHtml(filename, self.maxW, self.maxH))

        pass

    def writeMonth(self, month):
        self.file.write("\n\n# " + month + "\n___\n")
        pass

    def writeDay(self, day):
        self.file.write("\n\n## " + day + "\n___\n")
        pass

    def writeTime(self, timeint):
        timeStr = time.strftime("%H:%M:%S", time.localtime(timeint))
        self.writeHtmlBlockText(timeStr, align="middle", s=True, frontEnter=1)
        pass

    def writeNormalText(self, content):
        self.writeHtmlBlockText(content["m"])

    def writeReply(self, content):
        text = content["text"]
        sender = self.senderQQs.index(str(content["uin"]))
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content["time"]))
        text = f"&ensp;&ensp;&ensp;{self.senderNames[sender]}：“{text}”<br/>&ensp;&ensp;&ensp;{timestr}"

        self.writeHtmlBlockText(text, s=True, )

    # elif type in ["err","unknown","uns"]:
    #      self.writehtmlText()
    #
    #  elif type in ["revoke","tip"]:
    #      self.writehtmlText()
    #
    #  if obj["t"] in ["uns", "err"]:
    #      if obj["c"]["type"] in ["text", "media", "unknown"]:
    #      elif obj["c"]["type"] in ["tip"]:
    #
    #  elif obj["t"] == "revoke" or obj["t"] == "tip":
    #
    #  elif obj["t"] == "img" or obj["t"] == "video":
    #
    #  elif obj["t"] == "file":

    def writeSender(self):

        text = self.formantImgHtml(
            self.paths["sourceDirPath"] + self.senderDir + self.senderQQs[self.lastSender] + ".jpg", 35, 35)
        nameText = f"<b><small>&ensp;&ensp;{self.senderNames[self.lastSender]}&ensp;&ensp;</small></b>"

        if self.lastSender == 1:
            self.writeHtmlBlockText(text + nameText, "left", frontEnter=1)
        else:
            self.writeHtmlBlockText(nameText + text, "right", frontEnter=1)

    def writeHtmlBlockText(self, text: str, align="", style="", b: bool = 0, s: bool = 0, l: bool = 0, enter: int = 1,
                           frontEnter: int = 0, inline=False):
        if text == "":
            return
        if b:
            text = "<b>" + text + "</b>"
        if s:
            text = "<small>" + text + "</small>"
        if l:
            text = "<l>" + text + "</l>"

        if align == "":
            if self.lastSender == 1:
                align = "left"
            else:
                align = "right"

        if inline:
            text = ("<span style = \"{styleflag}\" >".format(styleflag=style)
                    + text + "</span>")
        else:
            text = ("<p align = \"{alignflag}\" style = \"{styleflag}\" >".format(alignflag=align, styleflag=style)
                    + text + "</p>")

        self.toEnter += frontEnter

        if inline:
            self.toEnter = 0

        while self.toEnter >= 1:
            text = "\n" + text
            self.toEnter -= 1

        self.toEnter = enter
        self.file.write(text)

    def writeMsgorMixmsg(self, content, timestampstr):
        text = ""
        for eachContent in content:
            intype = eachContent["t"]
            if intype == "m":
                text += eachContent["c"]["m"]
            elif intype == "img":
                # try:
                text = text + "<br/>" + self.formantImgHtml(eachContent["c"]["path"], self.maxW, self.maxH) + "<br/>"
                # except Exception as e:
                #     error_info = traceback.format_exc()
                #     self.log(
                #         f"一条IMG出错time:{timestampstr}：{e}消息为：{error_info}\n")

            elif intype == "reply":
                self.writeReply(eachContent["c"])

            elif intype == "qqemoji":
                text += self.formantImgHtml(
                    self.paths["sourceDirPath"] + self.emojiDir + "s" + eachContent["c"]["index"] + ".png"
                    , self.qqemojiSize, self.qqemojiSize)
            else:
                text += f"[其中无法显示的{intype}消息，time = {timestampstr}]"

        self.writeHtmlBlockText(text)

    def writeRevoke(self, content):
        self.writeHtmlBlockText(content["text"], s=True)

    def writeUns(self, content):
        self.writeHtmlBlockText(content["text"], l=True)

    def writeErr(self, content):
        self.writeHtmlBlockText(content["text"], l=True)

    def writeTip(self, content):
        text = content["text"]
        if text == "今日点亮幸运字符的消息条数已达上限，明日再来哦～" and not self.enableUselessTips:
            return
        self.writeHtmlBlockText(text, align="middle", s=True, l=True)

    def procTime(self, thisTime, drawMonth=True):
        """时间管理，是否显示时间，添加书签等，在绘制每条消息前调用
        :param thisTime: 当前消息时间戳
        :return:
        """
        thisDate = time.strftime("%Y-%m-%d", time.localtime(thisTime))
        thisMonth = time.strftime("%Y-%m", time.localtime(thisTime))
        thisYear = time.strftime("%Y", time.localtime(thisTime))
        thisDay = time.strftime("%d", time.localtime(thisTime))
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(thisTime))
        timeInday = time.strftime("%H:%M:%S", time.localtime(thisTime))

        # 对每月绘制一级标题
        if drawMonth:
            if thisMonth != self.lastMonth or self.monthInit:
                self.writeMonth(thisMonth)
                self.lastMonth = thisMonth
                self.monthInit = False
                self.senderInit = True

        # 对每天绘制二级标题
        if thisDay != self.lastDay or self.dayInit:
            self.writeDay(thisDay)
            self.lastDay = thisDay
            self.dayInit = False
            self.senderInit = True

        # 相差n秒,添加时间标签
        diffMin = abs(self.lastTime - thisTime)
        if diffMin >= self.timeShowSpan or self.timeInit:
            self.writeTime(thisTime)
            self.lastTime = thisTime
            self.timeInit = False
            self.senderInit = True

    def run(self):
        self.log("Converting to MD started")
        with open(self.paths["sourceDirPath"] + "chatData.txt", "r") as f:
            i = 1
            total_num = sum(1 for _ in f)
            f.seek(0)
            self.log(f"开始生成：共有{total_num}条")
            last_persent = 0

            for line in f:
                try:
                    obj = json.loads(line,strict=False)
                except Exception as e:
                    error_info = traceback.format_exc()
                    self.log(
                        f"一条消息出错：{e}消息为：{obj}\n读取错误，建议检查您的设置，并看一看错误排除文档，若无法解决可以上报：{error_info}\n")

                    present = int((self.currentMsgInd + 1) / total_num * 100)
                    if present % 5 == 0 and present != last_persent:
                        last_persent = present
                        info = f"生成进度：{present}%, {self.currentMsgInd + 1}/{total_num}"
                        self.log(info)
                    self.currentMsgInd += 1
                    continue
                present = int((self.currentMsgInd + 1) / total_num * 100)
                if present % 5 == 0 and present != last_persent:
                    last_persent = present
                    info = f"生成进度：{present}%, {self.currentMsgInd + 1}/{total_num}"
                    self.log(info)
                self.currentMsgInd += 1

                try:
                    obj["t"]
                except:
                    self.log(f"一条消息出错：{obj}\n")
                    continue

                # print(obj)
                self.checkInd()
                self.procTime(obj["i"])

                type = obj["t"]
                content = obj["c"]
                timestampstr = str(obj["i"])
                sender = self.senderQQs.index(obj["s"])
                self.checkSender(sender)

                if type == "msg" or type == "mixmsg":
                    self.writeMsgorMixmsg(content, timestampstr)
                elif type == "img":
                    self.writeImg(content)
                elif type == "err":
                    self.writeErr(content)
                elif type == "revoke":
                    self.writeRevoke(content)
                elif type == "tip":
                    self.writeTip(content)
                elif type == "uns":
                    self.writeUns(content)
                elif type == "file":
                    self.writeFile(content)
                elif type == "nudge":
                    self.writeNudge(content)
                elif type == "voice":
                    self.writeVoice(content)
                elif type == "video":
                    self.writeVideo(content)


                else:
                    self.log(f"type = {type} 的一条消息")
                    self.writeHtmlBlockText(f"[无法显示的{type}消息]")
                pass

                # try:
                #     # 消息类型
                #     self.processMsg(obj)
                #
                # except Exception as e:
                #     error_info = traceback.format_exc()
                #     self.log(
                #         f"一条消息出错：{e}消息为：{obj}\n详细错误信息，建议检查您的设置，并看一看错误排除文档，若无法解决可以上报：{error_info}\n")

            self.log(f"MD生成成功\n")
            self.file.close()
        pass

    def writeFile(self, content):
        name = content["name"]
        text = f"文件[{name}]"
        if content["received"] == False:
            text += "已被接收"
        else:
            text += "未接收"

        self.writeHtmlBlockText(text, l=True)

        pass

    def writeNudge(self, content):
        self.writeHtmlBlockText("[" + content["text"] + "]")
        pass

    def writeVoice(self, content):
        filename = self.paths["sourceDirPath"] + self.voiceDir + os.path.basename(content["path"])
        text = f"[语音消息]({filename})"
        while self.toEnter >= 1:
            text = "\n" + text
            self.toEnter -= 1
        self.file.write(text)
        self.toEnter += 1
        pass

    def writeVideo(self, content):
        filename = self.paths["sourceDirPath"] + self.videoDir + os.path.basename(content["path"])
        text = f"[视频消息]({filename})"
        while self.toEnter >= 1:
            text = "\n" + text
            self.toEnter -= 1
        self.file.write(text)
        self.toEnter += 1
        pass
