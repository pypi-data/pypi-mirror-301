from argparse import ArgumentParser
import sys

import yaml


def _disable_inout_layer(quant_list):
    for _, quantizers in quant_list.items():
        for _, descriptor in quantizers.items():
            if 'input_layer' in descriptor["etc_for_MCLab"].keys():
                descriptor["etc_for_MCLab"]["do_quant"] = False
            if 'output_layer' in descriptor["etc_for_MCLab"].keys():
                descriptor["etc_for_MCLab"]["do_quant"] = False

    modified_quant_list = quant_list

    return modified_quant_list


# 위에 함수 구현하고, 여기에 추가
_EDIT_FN_MAP = {'disable_inout': _disable_inout_layer}


class Qformat:
    """Abstract base class of qformat modification"""

    edit = None
    qformat_path = None

    def __init__(self, edit_cmd, qformat_path):
        __class__.edit = _EDIT_FN_MAP[edit_cmd]
        __class__.qformat_path = qformat_path

    def _read_qformat(self):
        qformat_path = self.qformat_path

        with open(qformat_path, encoding="utf-8") as f:
            header = f.readline()
            data = yaml.load(f, Loader=yaml.FullLoader)

        quant_list = data["quantized op list"]
        if not quant_list or len(quant_list) == 0:
            return None

        return quant_list, header

    def _save_qformat(self, quant_list, edit_cmd, header):
        qformat_path = self.qformat_path
        yaml_out = {"quantized op list": quant_list}
        with open(qformat_path, "w", encoding="utf-8") as fw:
            fw.write(f"# this qformat has been edited with --edit_cmd {edit_cmd} {header}")
            yaml.dump(yaml_out, fw, sort_keys=False)
            print(f'Save updated qformat file: {qformat_path}')

    @classmethod
    def update(cls, edit_cmd, qformat_path, overwrite=False):
        cls(edit_cmd, qformat_path)

        quant_list, header = cls._read_qformat(cls)
        modified_quant_list = cls.edit(quant_list)
        if not overwrite:
            cls.qformat_path = cls.qformat_path.split('.yaml')[0] + '.1.yaml'
        cls._save_qformat(cls, modified_quant_list, edit_cmd, header)


def build_argument_parser():
    """Build a parser for command-line arguments."""
    parser = ArgumentParser()
    parser.add_argument("--edit_cmd", default=None)
    parser.add_argument("--qformat_path", default=None)
    parser.add_argument("--overwrite", default=False, action='store_true')
    return parser


if __name__ == '__main__':
    arguments = build_argument_parser()
    args = arguments.parse_args(sys.argv[1:])

    Qformat.update(args.edit_cmd, args.qformat_path, overwrite=args.overwrite)
