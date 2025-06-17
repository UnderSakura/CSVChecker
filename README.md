# CSVChecker

## 编译打包

**运行编译指令**： 在打开的命令提示符窗口中，执行以下指令。我们使用 `--onefile` 参数，它会将所有依赖项打包成一个独立的 `.exe` 文件，方便分发和使用。

Bash

```bash
pyinstaller --onefile convert_csv_to_utf8.py
```



## 运行程序

#### 场景1：处理 EXE 文件所在目录的 CSV

这是最简单的方法。

1. 将 `dist` 文件夹中的 `convert_csv_to_utf8.exe` 文件**复制或移动**到你想要处理的、存放着CSV文件的文件夹里。

2. 在该文件夹中打开命令提示符（重复之前的操作，在地址栏输入 `cmd`）。

3. 运行以下指令：

   Bash

   ```bash
   # 直接执行程序名即可
   convert_csv_to_utf8.exe
   ```

   - 在 PowerShell 中，你可能需要使用 

     ```powershell
     .\
     ```

      来指明当前目录：

     ```powershell
     .\convert_csv_to_utf8.exe
     ```

程序会开始扫描并转换它所在的整个文件夹（包括子文件夹）里的所有 CSV 文件。

#### 场景2：处理任意指定目录的 CSV

你可以把 `.exe` 文件放在任何地方（比如桌面），然后远程处理其他文件夹里的文件。

1. 打开命令提示符。
2. 使用 `-d` 或 `--directory` 参数来指定目标路径。

**指令格式**： `"你的EXE文件完整路径" -d "你要处理的目标文件夹路径"`

**示例**： 假设你的 `.exe` 文件在 `C:\MyTools` 目录下，而你想要处理的 CSV 文件在 `D:\Data\Reports` 文件夹中。

Bash

```bash
# 注意路径中的空格，所以要用双引号括起来
"C:\MyTools\convert_csv_to_utf8.exe" -d "D:\Data\Reports"
```

这样，程序就会去扫描并转换 `D:\Data\Reports` 里的文件。