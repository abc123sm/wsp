import argparse
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

# tap/Tap.py 需要添加的导入
from tv_ass_process.config import (
    ProcessingConfig,
    OutputSettings,
    FullHalfConversion,
    CJKSpacing,
    RepetitionHandling,
    Mapping,
    MergeStrategy,
    ConversionStrategy,
    OutputFormat
)

from tv_ass_process.processor import Processor

logger = logging.getLogger("Tap")


def main():
    parser = argparse.ArgumentParser(description="Process subtitle files")
    parser.add_argument("path", nargs="+", type=Path, help="Input files/directories")
    args = parser.parse_args()

    # 硬编码配置
    config = ProcessingConfig(
        merge_strategy=MergeStrategy.AUTO,
        filter_interjections=True,
        output=OutputSettings(
            dir=None,
            format=OutputFormat.SRT,
            ending="",
            show_speaker=False,
            show_pause_tip=0
        ),
        full_half_conversion=FullHalfConversion(
            numbers=ConversionStrategy.HALF,
            letters=ConversionStrategy.HALF,
            convert_half_katakana=True
        ),
        cjk_spacing=CJKSpacing(
            enabled=False,
            space_char="\u2006"
        ),
        repetition_adjustment=RepetitionHandling(
            enabled=True,
            connector="… "
        ),
        mapping=Mapping(
            text={"！！": "!!", "！？": "!?"},
            regex={}
        )
    )

    process_paths(args.path, config)



# tap/Tap.py 修改process_paths函数
def process_paths(paths: list[Path], config: ProcessingConfig):
    processor = Processor(config)
    # 修改文件类型过滤逻辑
    srt_files = sorted(
        p for path in paths
        for p in (path.glob("*.srt") if path.is_dir() else [path])
        if p.is_file() and "_out.srt" not in p.name
    )
    
    for file in srt_files:
        output_path = file.with_name(f"{file.stem}_out.srt")
        processor.process_and_save(file, output_path)  # 需要修改Processor类


if __name__ == "__main__":
    main()
