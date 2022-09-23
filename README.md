<h1 align="center">Welcome to ER Diagram Generator 👋</h1>
<p>
</p>

ExcelでER図を作成することに面倒だと感じてませんか？  
テーブル定義書とテーブルの相関表をもとにER図を作成できます。

## 開発環境
OS: macOS Monterey 12.6  
Chip: Apple M1  
Memory: 16GB  
Python: 3.8.13  
pip: 22.2.2  
conda: 4.14.0  
VSCode: 1.70.1

## セットアップ
### Visual Studuo Codeのインストール
1. [Visual Studio Code](https://code.visualstudio.com "VS Code")からインストーラをダウンロードする
2. ダウンロードしたインストーラを実行する

### PlantUMLのセットアップ
### 1. Javaのインストール
PlantUMLの実行にはJavaの実行環境が必要です。
1. [Java](https://www.java.com/ja/ "Java install page")からインストーラをダウンロードする
2. インストーラを実行し、インストールする
以下のコマンドを実行してバージョンが返ってきたらインストール成功です.
```java
java -version
```

以下は出力結果の例です。
```sh
java version "1.8.0_341"
Java(TM) SE Runtime Environment (build 1.8.0_341-b10)
Java HotSpot(TM) 64-Bit Server VM (build 25.341-b10, mixed mode)
```

### 2. Graphvizのインストール
PlantUMLが描画するために使用しているソフトウェアです。  
[Graphviz](http://www.graphviz.org/download/ "Graphviz Download")から自身の環境に該当する方法でインストールする。
> インストール先を変更した場合には、環境変数`$GRAPHVIZ_DOT`を変更する必要があります。

### 3. PlantUMLのインストール
VSCodeの拡張機能からPlantUMLをインストールします。
1. VSCodeを起動し、`Ctrl+P`と入力してQuick Openを開く
2. Quick Openに`ext install plantuml`と入力して、Enterキーを押す
3. 検索結果から**PlantUML**を選択し、[インストール]を押す
4. インストール完了後に[再度読み込む]を押して、VSCodeを再起動する
> プレビュー機能を充実させるために、**Markdown Preview Enhanced**をインストールすることを推奨します。インストール方法はPlantUMLと同様に、
> ```sh
> ext install markdown preview enhanced
> ```
> で検索し、インストールできます。


### 4. インストール
Pythonに必要なライブラリをインストールします。  
**requirement.txt**を読み込めば開発環境と同じバージョンに揃えられます。
```sh
pip install -r requirement.txt
```

## 使い方
### 1. テーブル定義とテーブルの関係を記入する
テーブル定義(変数名一覧)と、テーブルの親子関係を記述します。  
以下のコマンドでエクセルフォーマットを生成できます。
```python
python ER_diagram_generator.py -g -e <filename>
```
filenameはデフォルトで**sample_format.xlsx**になってます。  
生成されたエクセルを開き、テーブル定義を編集します。  
各シートの名前をテーブル名に修正してください。  
**relation**というシートにはテーブルの関係を記入します。  
ソースとなるテーブルはParent列に、ソースを使用しているテーブルはChild列に記入してください。

### 2. テーブル定義を元にUMLを作成する
1で作成したテーブル定義を元にER図を作図するためのUMLを作成します。  
作成できるUMLは3つのモードがあります。
1. テーブルだけを作成する  
    このモードでは定義書に存在するテーブルの一覧を作成し、テーブル間の関係は作成されません。  
    次のコマンドにより作成できます(sample_format.xlsxを例に)。
    ```python
    python ER_diagram_generator.py --make_tables -f sample_format.xlsx
    ```
    正しく実行されると、**sample_format.md**という名前のファイルが**tables**ディレクトリに作成されます。tablesが存在しない場合には自動で作成されます。  
    作成されたファイルを開き、`[Ctrl]+K -> V`でプレビューが表示されます。プレビュー画面で右クリックにより様々な形式で保存することができます。  
    うまく作成できていると以下のような画像が表示されているはずです。
    ```plantuml
    @startuml
    !include uml/sample_format.md
    @enduml
    ```

2. テーブルの関係図だけを作成する  
    このモードではテーブルの関係図だけを作成し、テーブル内に変数名は入りません。テーブルの関係性を素早く理解するのに役立ちます。  
    次のコマンドにより作成できます(sample_format.xlsxを例に)。
    ```python
    python ER_diagram_generator.py --make_relations -f sample_format.xlsx
    ```
    正しく実行されると、**relation-sample_format.md**というファイルが**relation**ディレクトリに作成されます。relationが存在しない場合には自動で作成されます。  
    うまく作成できていると以下のような画像が表示されているはずです。
    ```plantuml
    @startuml
    !include uml/relation-sample_format.md
    @enduml
    ```

3. テーブルも関係図もまとめて作成する  
    このモードではテーブルの一覧と、テーブル同士の関係も作図します。  
    次のコマンドにより作成できます(sample_format.xlsxを例に)。
    ```python
    python ER_diagram_generator.py --make_all -f sample_format.xlsx
    ```
    正しく実行されると、**relation-sample_format.md**というファイルが**relation**ディレクトリに作成されます。relationが存在しない場合には自動で作成されます。  
    うまく作成できていると以下のような画像が表示されているはずです。
    ```plantuml
    @startuml
    !include uml/full_sample_format.md
    @enduml
    ```

## Author

👤 **Atsushi Mizukami**

使い方に関する質問や追加機能のリクエストがあったらこちらまで  
:email: [メールを送る](mailto:a.mizukami.0507@gmail.com)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_