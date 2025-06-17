# -*- coding: utf-8 -*-

import os
import argparse
import chardet
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def find_csv_files(directory: str) -> list:
    """在指定目录中查找所有的.csv文件。"""
    csv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def convert_to_utf8(file_path: str):
    """
    检测文件编码并将其转换为UTF-8 with BOM（如果需要）。
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(32 * 1024)
            result = chardet.detect(raw_data)
            
        original_encoding = result['encoding']
        confidence = result['confidence']
        
        logging.info(f"检测文件 '{os.path.basename(file_path)}' -> 编码: {original_encoding} (置信度: {confidence:.0%})")

        if original_encoding and original_encoding.lower() == 'utf-8-sig':
            logging.info(f"文件已是 UTF-8 with BOM 格式，无需转换。")
            return
        
        if original_encoding and original_encoding.lower() in ['utf-8', 'ascii']:
             logging.info(f"文件是标准UTF-8/ASCII，将为其添加BOM以增强兼容性...")
        elif confidence < 0.7:
             logging.warning(f"编码检测置信度过低，跳过文件 '{os.path.basename(file_path)}' 以防转换错误。")
             return

        logging.info(f"开始转换文件 '{os.path.basename(file_path)}' 从 {original_encoding} 到 UTF-8 with BOM...")
        
        temp_file_path = file_path + '.temp'
        
        with open(file_path, 'r', encoding=original_encoding, errors='replace') as f_in:
            with open(temp_file_path, 'w', encoding='utf-8-sig') as f_out:
                for line in f_in:
                    f_out.write(line)
        
        os.replace(temp_file_path, file_path)
        
        logging.info(f"成功将 '{os.path.basename(file_path)}' 转换为 UTF-8 with BOM。")

    except FileNotFoundError:
        logging.error(f"错误：文件未找到 '{file_path}'。")
    except Exception as e:
        logging.error(f"处理文件 '{file_path}' 时发生未知错误: {e}")
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def main():
    """主函数，用于解析参数和启动转换流程。"""
    parser = argparse.ArgumentParser(
        description="检测指定文件夹下的所有CSV文件，如果不是UTF-8 with BOM编码，则将其转换。",
        epilog="示例：\n"
               "python convert_csv_to_utf8.py \t\t(处理当前目录)\n"
               "python convert_csv_to_utf8.py -d \"C:\\Users\\YourUser\\Documents\" \t(处理指定目录)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='要扫描和转换的CSV文件所在的目录路径。'
    )
    
    args = parser.parse_args()
    target_dir = args.directory

    if not os.path.isdir(target_dir):
        logging.error(f"错误：指定的路径 '{target_dir}' 不是一个有效的目录。")
        return

    logging.info(f"开始扫描目录: '{os.path.abspath(target_dir)}'")
    
    csv_files = find_csv_files(target_dir)
    
    if not csv_files:
        logging.warning("未在该目录及其子目录中找到任何CSV文件。")
        return
        
    logging.info(f"找到 {len(csv_files)} 个CSV文件，开始检查和转换...")
    
    for file_path in csv_files:
        convert_to_utf8(file_path)
        
    logging.info("所有任务处理完毕。")

if __name__ == "__main__":
    main()