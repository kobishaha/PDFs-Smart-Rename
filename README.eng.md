# PDFSmartRename

PDFSmartRename 是一个利用OCR和 AI 技术自动重命名 PDF 文件的工具。

## 功能

- 使用 PyMuPDF 从 PDF 的第一页提取文本。
- 如有必要，使用 Tesseract OCR 从图像中提取文本。
- 使用 Gemini API 根据提取的文本生成新文件名。
- 使用生成的标题重命名 PDF 文件。

## 安装

1. 安装所需的 Python 库：
   ```bash
   pip install fitz pillow pytesseract requests
   ```

2. 在您的系统上安装 Tesseract-OCR。如果它没有安装在默认路径中，您可能需要在脚本中指定其路径：
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
   ```

3. 获取 Gemini API 的 API 密钥。

## 使用

1. 在脚本中将 `directory_path` 变量设置为包含您的 PDF 文件的目录。
2. 将 `your_api_key` 变量设置为您的 Gemini API 密钥。
3. 运行脚本以重命名指定目录中的所有 PDF 文件。

## 许可证

此项目根据 MIT 许可证获得许可。有关更多信息，请参阅 `LICENSE` 文件。
