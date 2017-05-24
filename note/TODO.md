# v1.2.0
## New function
* File selection function (using `tkinter`)
    * 求められるユーザー入力
        * ファイル絶対パス(複数指定)
        * 実行時刻
* Sending mail function
    * 捨てアカウントのgmailを送信用にする
    * logファイルを記録するようにする
    * logファイルの中身を送信する
    > 受信用アドレスは後付できるようにする
    > インターフェースとして送受信アドレスを引数にするクラスを作成


## USAGE
1. `./runfeko`とタイプする or `rufeko.bat`をクリック
2. file選択を施される
    fileを選択するとファイルリストが作成される
3. runfekoの実行
    ファイルリストから逐次ファイルを取り出しコマンド生成
    生成されたコマンドをイテレータとして実行
4. 正常終了？異常終了？ログ？結果？などを`<datetime>.log`に書き込み
5. mailを送信


## コマンドをイテレータとするべきか、リストとするべきか
リストであればqueuingでプライオリティを付けて割り込み処理ができそう
イテレートするとv1.3.0で実装予定のスーパークラスいらないか？
せっかくファイルの複数選択をしている意味を考えろ



## subprocess
逐次処理なので、subshellにfeko コマンド実行させて、処理が終わったらタスクを命令したshellに戻る

```python
import subprocess as sp
sp.call('myshell', shell=True)
```


---
# v1.3.0
## New function
* Queuing function
    基本的に、あとから命令された実行コマンドをためておいて、一個ずつ逐次処理を行う
    例外として、処理の中断を行うインターフェースつける...のか？
    runfekoというインスタンスをためておく仕組み

    以下の処理を子クラス(class Queue)として実装
        task=runfeko.Runfeko()
        のインスタンス変数: `task.command_list`
        に対して、後から処理を追加・削除する時のメソッド。
        基本は`task.command_list.append`
        割り込み処理するときは`task.command_list.insert`
        処理の中断は`task.command_list.pop`, `task.command_list.remove`, `task.command_list.clear`
        python標準のリスト型のメソッドを参考にした。

    ```python
    """例えば
    tasks listにRunfekoインスタンスを追加していく
    処理が終了次第次の処理へ進む
    エラーが発生したらログファイル書き込み
    """
    import runfeko
    first_task = runfeko.Runfeko()
    second_task = runfeko.Runfeko()
    tasks = [first_task, second_task]

    def queuing(tasks):
        for i in tasks:
            do
            exit 0が返されたら、正常終了なので次へ進む
            exit 1が返されたら、異常終了なので、ログに記録して次へ進む
            exit 2が返されたら、異常終了(中断レベル)なので、ログに記録して終了する
    ```

    ```python
    class
    ```

並列処理ではなく逐次処理するからタスク管理クラスが必要


# v1.4.0
## functions
* 割り込み処理
* タスクキル
