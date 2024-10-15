from typing import Optional, Any

from tq_datasets.dataset_op_interface import TraverseDatasetItems
from tq_utils import my_json


def test_default_method():
    print()
    t = TraverseDatasetItems()
    t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng\al-monitor',
                       'json')


class TraverseDOWLItems(TraverseDatasetItems):
    @staticmethod
    def item_reader(file_abs_path: str) -> str:
        print('oaushoiasdoiajsodiasoidowifoqn')
        return my_json.load_json_safe(file_abs_path)

    @staticmethod
    def item_processor(**kwargs) -> Optional[Any]:
        print('asdasda')
        print('asda')
        return kwargs['raw_item_data']


def test_override_methods():
    print()
    t = TraverseDOWLItems()
    t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng\al-monitor',
                       'json')
