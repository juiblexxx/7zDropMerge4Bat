# coding: utf-8

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

# 警告メッセージボックス用
root = tk.Tk()
root.withdraw()

# 7z分割ファイル(.7z.001, .7z.002, ... )を1つの7zファイルに結合する
# BATから呼ばれる必要あり、右記コマンドを記載する：python "C:\Data\DL2\Python\7zDropMerge4Bat.py" %*
# BATに複数ファイルをドロップすると、ファイル名から拡張子を除外した結合ファイルが作成される
file_paths = sys.argv[1:]   # 最初の引数はスクリプト自身が入る
file_paths.sort()   # パス名で昇順ソートする

out_path = ''
out_file = ''
command_arg = ''

# 取得したパスでループ
for p in file_paths:

    if out_path == '':
        # 出力先パスは一番最初に現れるファイルのカレントパスとする
        out_path = os.path.dirname(p) + '\\'

    # 結合用ファイル名の取得
    part_file = os.path.basename(p)

    if out_file == '':
        # 出力先ファイル名は結合用ファイル名の拡張子を無くしたものとする
        # 結合用ファイルの拡張子は なんとかかんとか.7z.001　なので、.001を削る
        z7_part_name = os.path.basename(p).split('.')

        # list.remove()は存在しない要素を指定するとValueError Exceptionが起こるのでトラップする
        # リスト最初のファイル名に拡張子001がなかったらエラーで抜ける
        try :
            z7_part_name.remove('001')
        except ValueError:
            messagebox.showinfo('エラー','分割7zの結合ではない可能性')
            sys.exit()

        # listはjoinメソッドで結合できる
        out_file = '.'.join(z7_part_name)

    # コマンドライン文字列作成
    if command_arg != '':
        command_arg = command_arg + '+'

    # Windows copyコマンドに渡す為の引数を作成する
    command_arg = command_arg + '"' + out_path + part_file + '"'

# 外部コマンド実行はsubprocess.Popenを使うらしい（PはPipeじゃなくProcessとの事）
# コマンドを作る
command_arg = 'copy /B ' + command_arg + ' ' + '"' + out_path + out_file + '"'
print(command_arg)

# Windowsのbuild inコマンドを使うにはshell=Trueを使う
res = subprocess.Popen(command_arg, shell=True)
