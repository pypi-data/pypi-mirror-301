#import
from .scratchattachplus import *

#ver
__version__ = '0.4.0'
__name__ = "scratchattachplus"
__url__ = "https://github.com/kakeruzoku/scratchattachplus"
__changelog__ = """[https://github.com/kakeruzoku/scratchattachplus/blob/main/changelog.md]
v0.4.0 ユーザーのコメントに対応 関数の追加
v0.3.0 user_okの追加 scratchattach_requestsの引数追加 そのたもろもろ
v0.2.1 0.3.0で共有しようとしたらみすった
v0.2.0 プロジェクトの作成の追加
v0.1.3 きにすんな
v0.1.2 エラーの修正
v0.1.1 エラーの修正
v0.1.0 エラーの修正+ScratchAttachクラウドリクエストのクライアント機能の追加
v0.0.1 共有
"""

if __name__ == "__main__":
    print("""
Welcome to scratchattachplus!
Read https://github.com/kakeruzoku/scratchattachplus
Thanks to timmccool for scratchattach
by kakeruzoku""")


# ScratchAttach:https://github.com/timmccool/scratchattach
# python setup.py sdist
# python setup.py bdist_wheel
# twine upload --repository pypi dist/*

