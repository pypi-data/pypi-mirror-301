"""
Traverse every script file in the dataset.
You can specify the method how program read, process and filter the scripts.
"""
import os
from typing import Any, List, Optional, Dict

from ..utils import FileManager


class TraverseDatasetItems:
    @staticmethod
    def item_reader(file_abs_path: str) -> Any:
        """
        读取数据集元素的方法。
        默认通过文本的方式读取数据集文件。如需重写，请不要改动参数。
        :param file_abs_path: 文件的绝对路径
        :return: raw data from file.
        """
        with FileManager(file_abs_path, 'r') as f:
            return f.read()

    @staticmethod
    def item_processor(**kwargs) -> Optional[Any]:
        """
        根据元素的绝对路径和 item_reader 获取的原始数据，处理数据返回 processed_item_data。
        默认打印 file_abs_path 和 raw_item_data，并直接返回 raw_item_data。如需重写，请不要改动参数。
        <param traverse_dir> 遍历数据集的目录的绝对路径
        <param file_abs_path> 数据集元素文件的绝对路径
        <param raw_item_data> item_reader 获取的原始数据
        <param external_raw_data> 向 item_process 中传入的额外的数据
        <returns> processed_item_data 处理过的元素数据 or None
        """
        print(
            f"processing:\ntraverse_dir: {kwargs['traverse_dir']}, \nfile_path: {kwargs['file_abs_path']},\nraw_data:\n{kwargs['raw_item_data']}",
            end='\n\n')
        return kwargs['raw_item_data']

    @staticmethod
    def item_filter(**kwargs) -> bool:
        """
        根据元素的绝对路径、item_reader 获取的原始数据 和 已经收集元素数据的数量，判断是否保留数据。
        默认直接返回 True，保留所有数据。如需重写，请不要改动参数。
        <param traverse_dir> 遍历数据集的目录的绝对路径
        <param file_abs_path> 数据集元素文件的绝对路径
        <param processed_item_data> item_processor 处理过的元素数据
        <param length_of_result> 已经收集了元素数据的数量
        <returns> True，保留数据；False，反之。
        """
        return True

    @classmethod
    def traverse_dataset(cls, traverse_dir: str, item_file_type: str, external_raw_data: Dict[str, Any] = None) -> List[
        tuple]:
        """
        遍历给定数据集目录下的元素，并对其进行处理，最终返回处理的结果。如果需要自定义数据集元素的读取、处理和过滤函数，请重写对应方法。
        :param traverse_dir: 遍历数据集的目录的绝对路径
        :param item_file_type: 数据集中元素的文件类型
        :param external_raw_data: 向 item_process 中传入的额外的数据
        :returns: list of the tuple(item_absolute_path, return result of item_processor)
        """
        if not os.path.exists(traverse_dir):
            raise FileNotFoundError(f'Dataset not found at {traverse_dir}.')

        result = []
        for root, dirs, files in os.walk(traverse_dir):
            for file in files:
                file_type = os.path.splitext(file)[1]
                if file_type == '' or file_type[1:] != item_file_type:
                    continue
                file_abs_path = os.path.join(root, file)
                raw_item_data = cls.item_reader(file_abs_path)

                processed_item_data = cls.item_processor(traverse_dir=traverse_dir,
                                                         file_abs_path=file_abs_path,
                                                         raw_item_data=raw_item_data,
                                                         external_raw_data=external_raw_data)

                if cls.item_filter(traverse_dir=traverse_dir, file_abs_path=file_abs_path,
                                   processed_item_data=processed_item_data,
                                   length_of_result=len(result)):
                    result.append((file_abs_path, processed_item_data))
        return result
