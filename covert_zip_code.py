import zipfile
import os
import shutil
import argparse

def sanitize_filename(filename):
    # 替换Windows不允许的文件名字符
    return filename.replace('/', '\\')

def convert_zip_gbk_to_utf8(zip_path, output_zip_path):
    # 创建一个临时目录来提取文件
    temp_dir = "temp_extract"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 提取所有文件到临时目录
        for info in zip_ref.infolist():
            # 将 GBK 文件名转换为 UTF-8
            filename = info.filename.encode('cp437').decode('gbk')
            # 清理文件名，移除不合法字符
            filename = sanitize_filename(filename)
            # 创建文件的完整路径
            extracted_path = os.path.join(temp_dir, filename)
            
            # 检查当前路径是目录还是文件
            if info.is_dir():
                # 如果是目录，则只创建目录，不创建文件
                os.makedirs(extracted_path, exist_ok=True)
            else:
                # 如果是文件，确保其目录存在，然后写入文件
                os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                # 将文件提取到该路径
                with open(extracted_path, 'wb') as f:
                    f.write(zip_ref.read(info.filename))

    # 创建一个新的 ZIP 文件，并使用 UTF-8 编码文件名
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 将文件添加到新 ZIP 中，并保持相对路径
                arcname = os.path.relpath(file_path, temp_dir)
                zip_out.write(file_path, arcname.encode('utf-8').decode('utf-8'))

    # 清理临时目录
    shutil.rmtree(temp_dir)
    print(f"转换完成，新ZIP文件保存为: {output_zip_path}")

def main():
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="Convert ZIP file names from GBK to UTF-8 encoding")
    parser.add_argument('input_zip', help='The input ZIP file with GBK encoded file names')
    parser.add_argument('output_zip', help='The output ZIP file with UTF-8 encoded file names')

    # 解析命令行参数
    args = parser.parse_args()

    # 调用转换函数
    convert_zip_gbk_to_utf8(args.input_zip, args.output_zip)

if __name__ == "__main__":
    main()
