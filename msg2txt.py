#!/usr/bin/env python3
# coding:utf-8
"""
msgファイルを元に扱いやすい様にデータを取得します。

Usage:
    $ python msg2txt.py foo.msg bar.msg ...  # => Dump to foo.txt, bar.txt
    $ python msg2txt.py *.msg -  # => Concat whole msg and dump to STDOUT
"""
import sys
import re
from pathlib import Path
import extract_msg
import traceback

VERSION = "msg2txt v1.0.0"


class MsgParser:
    """
    メールファイルのパスを受け取り、それを解析するクラス
    """

    def __init__(self, mail_file_path):
        self.mail_file_path = mail_file_path
        self.msg = extract_msg.openMsg(mail_file_path)
        self.subject = None
        self.to_address = None
        self.cc_address = None
        self.from_address = None
        self.date = None
        self.body = ""
        self.attach_file_list = []
        self._parse()

    def get_attr_data(self):
        """
        メールデータの取得
        """
        result = """\
DATE: {}
FROM: {}
TO: {}
CC: {}
-----------------------
SUBJECT: {}
BODY:
{}
-----------------------
ATTACH_FILE_NAME:
{}
""".format(self.date, self.from_address, self.to_address, self.cc_address,
           self.subject, self.body,
           ",".join([x["name"] for x in self.attach_file_list]))
        return result

    def _parse(self):
        """
        メールファイルの解析
        __init__内で呼び出している
        """
        self.subject = self.msg.subject or ""
        self.to_address = self.msg.to or ""
        self.cc_address = self.msg.cc or ""
        self.from_address = self.msg.sender or ""
        # dateをISO形式に変換
        if self.msg.date:
            self.date = self.msg.date.isoformat()
        else:
            self.date = ""

        # メッセージ本文
        self.body = self.msg.body or ""

        # 添付ファイル
        for attachment in self.msg.attachments:
            self.attach_file_list.append({
                "name":
                attachment.longFilename or attachment.shortFilename
                or "unknown",
                "data":
                attachment.data
            })

    @staticmethod
    def help(exitcode):
        """Show help"""
        print(__doc__)
        sys.exit(exitcode)

    @staticmethod
    def version():
        """Show version"""
        print(VERSION)
        sys.exit(0)

    @classmethod
    def dump2stdout(cls, argv):
        """Dump messages to STDOUT"""
        argv.remove('-')
        for filename in argv[1:]:
            result = cls(filename).get_attr_data()
            print(result)

    @classmethod
    def dump2txt(cls, argv):
        """Dump messages to TEXT"""
        try:
            for filename in argv[1:]:
                parser = cls(filename)
                invalid_str = r"[\\/:*?\"<>|]"
                subject = re.sub(invalid_str, "", parser.subject)
                title_date = parser.date[:-len("+09:00")].replace(
                    "-", "") if parser.date else "nodate"
                date = re.sub(invalid_str, "", title_date)
                result = parser.get_attr_data()
                with open(f'{date}_{subject}.txt', 'w',
                          encoding='utf-8') as _f:
                    _f.write(result)
        except BaseException as e:
            with open('msg2txt_error.txt', 'a', encoding='utf-8') as _f:
                print('error:', e)
                for i in [
                        traceback.format_exc() + '\n',
                        '\n',
                        filename + '\n',
                        parser.subject + '\n',
                        parser.date + '\n',
                        parser.get_attr_data() + '\n',
                ]:
                    _f.write(i)
                sys.exit(1)


def main():
    """Entry point"""
    if len(sys.argv) < 2:
        MsgParser.help(1)
    elif sys.argv[1] == '-v' or sys.argv[1] == '--version':
        MsgParser.version()
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        MsgParser.help(0)
    elif '-' in sys.argv:
        MsgParser.dump2stdout(sys.argv)
    else:
        MsgParser.dump2txt(sys.argv)


if __name__ == "__main__":
    main()
