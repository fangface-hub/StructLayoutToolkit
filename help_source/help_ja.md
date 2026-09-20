# StructLayoutToolkit ユーザーガイド

StructLayoutToolkit は、バイナリファイルおよび再構成されたパケットペイロードを
表示・編集するためのツールです。最初はドキュメントフォルダーからファイルを
開きます。ファイルを開くか保存すると、ファイルの種類ごとに最後に使用した
フォルダーが記憶されます。

## Launcher Window

ランチャーは各エディターを別のプロセスで開きます。ランチャーを閉じても、すでに
開いているエディターは閉じません。

- **Binary Editor** は Binary Viewer を開きます。
- **Packet Data Editor** は Packet Data Editor を開きます。

複数のエディターを同時に開くこともできます。

## Binary Viewer Window

Binary Viewer では、バイナリファイルを生のバイト列として、または StructLayout
定義でデコードしたフィールドとして表示・編集できます。

### バイナリ編集の手順

1. 構造化データを扱う場合は、**Type Definition > Open StructLayout...** を
   選択します。または **Type Definition > Load Resource** から組み込みの PCAP
   または PCAPNG レイアウトを読み込みます。
2. **File > Open Binary...** を選択してバイナリファイルを開きます。必要に応じて、
   デコードに使用するルート構造体を選択します。
3. 表の値を編集します。
4. **File > Save Binary** または **Save Binary As...** を選択し、現在のデータを
   エンコードして保存します。

**File > New Binary...** を選択すると、ゼロで埋められた新しいバイナリデータを
作成できます。構造体を選択した場合は、その構造体に必要な最小サイズになります。
構造体を選択しなかった場合は、生バイナリモードで開きます。

### データ表

表には、オフセット、16 進数のバイト列、フィールド名、型、値、サイズが表示されます。
ネストした構造体は展開または折りたたむことができます。

- 生バイナリモードでは **hex** セルを編集します。その行に表示されているバイト数と
  同じ長さの 16 進数を入力します。バイト間の空白は省略できます。
- 構造化モードでは **value** セルを編集します。Enter キーを押すか、セルから
  フォーカスを移動すると値が反映されます。
- `bytearray` フィールドの **hex** セルを右クリックし、
  **Open BinaryEditorWindow** を選択すると、そのフィールドを別の Binary Viewer
  で編集できます。変更を反映するには **Return with saving**、破棄するには
  **Return without saving** を選択します。
- **Bytes/row** では、生バイトを一行にまとめて表示するバイト数を変更できます。
- 定義を変更した後に **Re-decode** を選択すると、現在のバイト列を再度デコードします。

値をフィールド型へ変換できない場合や構造体をエンコードできない場合は、エラー
ダイアログが表示され、ファイルは保存されません。

### File メニュー

- **Save Binary** は現在のバイナリファイルへ変更を書き込みます。
- **Save Binary As...** はエンコードしたデータを別のファイルへ保存します。
- **Export to CSV...** は、各フィールドのネストレベルとパスを含む平坦な一覧を
  CSV として出力します。
- **Export to JSON...** は、表示中のフィールドツリーをネストした JSON として
  出力します。
- **Exit** は Binary Viewer を閉じます。

### Type Definition メニュー

- **Open StructLayout...** は構造体定義と列挙型定義を JSON から読み込みます。
- **Load Resource > PCAP** と **PCAPNG** は組み込みレイアウトを読み込みます。
- **Save StructLayout** と **Save StructLayout As...** は使用中のレイアウトを
  保存します。
- **Select Struct...** はルート構造体を選択し、データを再度デコードします。
- **Struct Definitions...** は StructDef Dict Editor を開きます。
- **Enum Definitions...** は EnumDef Dict Editor を開きます。

## Packet Data Editor Window

Packet Data Editor では、PCAP または PCAPNG キャプチャを開き、IP フラグメントを
再構成し、パケットペイロードを表示・編集して保存できます。

### パケット編集の手順

1. **File > Open Capture...** を選択し、`.pcap` または `.pcapng` ファイルを
   開きます。
2. **Reassembled packets** からパケットを選択します。
3. ペイロードのフィールドをデコードするには、**Packet Definition > Payload Struct
   Definitions...** を開き、一つ以上の照合定義を設定します。
4. パケットの 16 進データまたはデコードされたフィールド値を編集します。
5. **File > Save Capture** または **Save Capture As...** を選択します。

### Reassembled packets ペイン

上側のペインには、パケット番号、タイムスタンプ、IP バージョン、送信元、宛先、
プロトコル、識別子、ペイロード長、再構成状態、ペイロードのバイト列が表示されます。

- **Complete** のパケットは **Hex** 列で編集できます。
- **Incomplete** のパケットは一部のフラグメントがないため、読み取り専用です。
- パケットに複数のフラグメントがある場合は、展開すると各フラグメントを確認できます。
  フラグメント行は読み取り専用です。
- 再構成されたペイロードを編集すると、キャプチャ内の対応するバイト列が更新されます。

### Decoded packet data ペイン

下側のペインには、選択した完全なパケットが、最初に条件と一致したペイロード構造体
定義を使って表示されます。一致する定義がない場合、ヘッダーには
**Payload: Hex only** と表示されます。

**value** 列のフィールドを編集し、Enter キーを押すかフォーカスを移動すると値が
反映されます。ペイロードが再エンコードされ、キャプチャのバイト列が更新された後、
パケットが再度デコードされます。ほかの列とネストした構造体の行は読み取り専用です。

### ファイルと定義のメニュー

- **Open Capture...** は PCAP または PCAPNG ファイルを開きます。
- **Save Capture** は現在のキャプチャを上書きします。
- **Save Capture As...** は別の PCAP または PCAPNG ファイルとして保存します。
- **Payload Struct Definitions...** は順序付きのペイロード照合ルールを開きます。
- **Exit** は Packet Data Editor を閉じます。

## Payload Struct Definition Editor Window

このウィンドウでは、パケットの条件を StructLayout 定義に対応付けます。ルールは
上から順に評価され、最初に一致したルールが使用されます。

### ルールの管理

- **Add** は条件が `True` のルールを作成します。
- **Remove** は選択したルールを削除します。
- **Move Up** と **Move Down** は照合の優先順位を変更します。
- 行を選択して条件とルート構造体を編集し、**Update** を選択して行へ反映します。
- **Load StructLayout...** は選択中のルールへ JSON レイアウトを読み込みます。

条件では `key`、`payload`、`ip_version`、`source`、`destination`、`protocol`、
`identification` を参照できます。条件には、レイアウトの式評価機能が対応している
有効な式を指定する必要があります。

**Type Definition** メニューでは、ルート構造体の選択や、選択中のルールに対する
StructDef および EnumDef エディターの表示ができます。**File** メニューでは、順序を
含むルール一覧全体を JSON として開いたり保存したりできます。ウィンドウを閉じても
現在のルールは Packet Data Editor に保持されます。ルールをファイルにも保存する
場合は **Save** を使用してください。

## StructDef Dict Editor Window

このウィンドウでは、使用中の StructLayout に含まれる構造体を編集します。

### 構造体

- **Add Struct** と **Remove Struct** は構造体の一覧を管理します。
- 構造体を選択すると、その名前と説明を編集できます。
- **Update Meta** を選択すると、名前または説明の変更が反映されます。

### フィールド

- **Add Field**、**Insert Field**、**Remove Field** はフィールドを管理します。
- **Shift Offset** は、選択したフィールドのオフセットを指定したバイト数とビット数だけ
  移動します。
- **Update Multi-line Size** は、選択したすべてのフィールドへサイズを設定します。
- **Initial Size** と隣の型セレクターは、新しいフィールドの初期値を設定します。
- セルを直接編集すると、`name`、`offset`、`size`、`type`、`scale`、`repeat`、
  `description`、`range_expression`、`enum_def_name`、`byte_swap` を変更できます。

オフセットとサイズには、`1,3` のような `byte,bit` 形式を使用できます。対応する
項目ではレイアウト式も使用できます。すべての定義を親レイアウトへ反映するには
**Update**、このウィンドウで行った変更を破棄するには **Cancel** を選択します。

## EnumDef Dict Editor Window

このウィンドウでは、使用中の StructLayout のフィールドから参照される、名前付きの
整数値を編集します。

- **Add Enum** と **Remove Enum** は列挙型定義を管理します。
- 選択した列挙型の名前と説明を編集し、**Update Meta** を選択します。
- **Add Value** は **Start Value** の値を開始値として項目を末尾へ追加します。
- **Insert Value** は選択した行の前へ項目を挿入します。
- **Shift Value** は選択した値に指定量を加算または減算します。
- **Remove Value** は選択した行を削除します。
- 表の値名と整数値は直接編集できます。

すべての列挙型定義を親レイアウトへ反映するには **Update**、このウィンドウで行った
変更を破棄するには **Cancel** を選択します。
