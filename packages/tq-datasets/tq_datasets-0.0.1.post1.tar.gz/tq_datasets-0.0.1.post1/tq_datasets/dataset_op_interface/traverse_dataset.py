"""
Traverse every script file in the dataset.
You can specify the method how program read, process and filter the scripts.
"""
import os
from typing import Callable, Any, List, Optional, Dict
from utils import FileManager


def traverse_dataset(traverse_dir: str, item_file_type: str,
                     item_reader: Callable[[str], Any] = None,
                     item_processor: Callable[[Dict[str, Any]], Optional[Any]] = None,
                     item_filter: Callable[[Dict[str, Any]], bool] = None) -> List[tuple]:
    """
    遍历给定数据集目录下的元素，并对其进行处理，最终返回处理的结果。
    :param traverse_dir: 遍历数据集的目录的绝对路径
    :param item_file_type: 数据集中元素的文件类型
    :param item_reader: 读取数据集元素的方法。
                        若为 None，默认读取 UFT8 编码的文本数据。
                        <param file_abs_path> 文件的绝对路径
                        <returns> raw data from file.
    :param item_processor: 根据元素的绝对路径和 item_reader 获取的原始数据，处理数据返回 processed_item_data。
                           若为 None，默认打印 file_abs_path 和 raw_item_data，并直接返回 raw_item_data。
                           <param traverse_dir> 遍历数据集的目录的绝对路径
                           <param file_abs_path> 数据集元素文件的绝对路径
                           <param raw_item_data> item_reader 获取的原始数据
                           <returns> processed_item_data 处理过的元素数据 or None
    :param item_filter: 根据元素的绝对路径、 item_reader 获取的原始数据 和 已经收集元素数据的数量，判断是否保留数据。
                        若为 None，默认直接返回 True，保留所有数据。
                        <param traverse_dir> 遍历数据集的目录的绝对路径
                        <param file_abs_path> 数据集元素文件的绝对路径
                        <param processed_item_data> item_processor 处理过的元素数据
                        <param length_of_result> 已经收集了元素数据的数量
                        <returns> True，保留数据；False，反之。
    :returns: list of the tuple(item_absolute_path, return result of item_processor)
    """

    def default_item_reader(file_path: str) -> str:
        with FileManager(file_path, 'r') as f:
            return f.read()

    def default_item_processor(**kwargs) -> Any:
        print(
            f"processing:\ntraverse_dir: {kwargs['traverse_dir']}, \nfile_path: {kwargs['file_abs_path']},\nraw_data:\n{kwargs['raw_item_data']}",
            end='\n\n')
        return kwargs['raw_item_data']

    def default_item_filter(**kwargs) -> bool:
        print(
            f"filtering:\ntraverse_dir: {kwargs['traverse_dir']}, \nfile_path: {kwargs['file_abs_path']},\nprocessed_data:\n{kwargs['processed_item_data']},\nlength_of_result: {kwargs['length_of_result']}",
            end='\n\n')
        return True

    if not os.path.exists(traverse_dir):
        raise FileNotFoundError(f'Dataset not found at {traverse_dir}.')

    item_reader = item_reader if item_reader else default_item_reader
    item_processor = item_processor if item_processor else default_item_processor
    item_filter = item_filter if item_filter else default_item_filter

    result = []
    for root, dirs, files in os.walk(traverse_dir):
        for file in files:
            file_type = os.path.splitext(file)[1]
            if file_type == '' or file_type[1:] != item_file_type:
                continue
            file_abs_path = os.path.join(root, file)
            raw_item_data = item_reader(file_abs_path)

            processed_item_data = item_processor(traverse_dir=traverse_dir, file_abs_path=file_abs_path,
                                                 raw_item_data=raw_item_data)

            if item_filter(traverse_dir=traverse_dir, file_abs_path=file_abs_path,
                           processed_item_data=processed_item_data, length_of_result=len(result)):
                result.append((file_abs_path, processed_item_data))
    return result


if __name__ == '__main__':
    traverse_dataset(r'E:\Workspace\DOWL\eng', 'json')
