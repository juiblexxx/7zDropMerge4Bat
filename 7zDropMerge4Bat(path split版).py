# coding: utf-8
import sys
import subprocess

# 7z分割ファイル(.7z.001, .7z.002, ... )を1つの7zファイルに結合する
# BATから呼ばれる必要あり、右記コマンドを記載する：python "C:\Data\DL2\Python\7zDropMerge4Bat.py" %*
# BATに複数ファイルをドロップすると、ファイル名から拡張子を除外した結合ファイルが作成される

file_paths = sys.argv[1:]   # 最初の引数はスクリプト自身が入る
file_paths.sort()   # パス名で昇順ソートする

out_path = ''
out_file = ''
command_arg = ''

for p in file_paths:
    split_path = p.split('\\')  # ファイルパスを取得したいのでバクスラでsplit
    
    if out_path == '':
        # 出力先パスは一番最初に現れるファイルのカレントパスとする
        for sp in split_path[:len(split_path) - 1]:
            out_path = out_path + sp + '\\'
        # print(out_path)
        
    # 結合用ファイル名の取得
    part_file = split_path[len(split_path) - 1]
    # print(part_file)
    
    if out_file == '':
        # 出力先ファイル名は結合用ファイル名の拡張子を無くしたものとする
        # 結合用ファイルの拡張子は.7z.001なので、.001が削れる
        z7_part_name = part_file.split('.')
        for sp in z7_part_name[:len(z7_part_name) - 1]:
            if out_file != '':
                out_file = out_file + '.'
            out_file = out_file + sp
    
    if command_arg != '':
        command_arg = command_arg + '+'

    # Windows copyコマンドに渡す為の引数を作成する
    command_arg = command_arg + '"' + out_path + part_file + '"'

# 外部コマンド実行はsubprocess.Popenを使うらしい
# コマンドを作る
command_arg = 'copy /B ' + command_arg + ' ' + '"' + out_path + out_file + '"'
print(command_arg)

# Windowsのbuild inコマンドを使うにはshell=Trueを使う
res = subprocess.Popen(command_arg, shell=True)
