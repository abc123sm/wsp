import logging
import re
from pathlib import Path

from .events import Dialog, Events
from .types import Timecode, Position, Color
from ..config import OutputSettings
from ..constants import ASS_HEADER

__all__ = [
    "Subtitle",
    "load",
    "from_ass_text",
]

logger = logging.getLogger("Tap")

OVERRIDE_BLOCK_PATTERN = re.compile(r"(?<!\\){([^}]*)}")


class Subtitle:
    def __init__(self):
        self.res_x = 960
        self.res_y = 540
        self.events = Events()

    @classmethod
    def load(cls, path: Path | str, encoding: str = "utf-8") -> "Subtitle":
        path = Path(path)
        with path.open("r", encoding=encoding) as f:
            if path.suffix.lower() == ".ass":
                return cls.from_ass_text(f.read())
            elif path.suffix.lower() == ".srt":
                return cls.from_srt_text(f.read())
            else:
                raise ValueError(f"Unsupported format: {path.suffix}")

    @classmethod
    def from_srt_text(cls, srt_text: str) -> "Subtitle":
        doc = cls()
        blocks = re.split(r"\n{2,}", srt_text.strip())
        for block in blocks:
            lines = block.split("\n")
            if len(lines) < 3:
                continue
            timing = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", lines[1])
            if timing:
                start = Timecode(timing.group(1).replace(",", "."))
                end = Timecode(timing.group(2).replace(",", "."))
                text = " ".join(lines[2:]).strip()
                doc.events.append(Dialog(start, end, "Default", text))
        return doc

    @classmethod
    def from_ass_text(cls, ass_text: str) -> "Subtitle":
        def parse_ass_dialog(line: str) -> "Dialog":
            splits = line.split(",", 9)

            start = Timecode(splits[1].strip())
            end = Timecode(splits[2].strip())
            style = splits[3].strip()
            name = splits[4].strip()
            text = splits[9].strip().removesuffix("\\N")


            pos_match = re.search(r"\\pos\((\d+),(\d+)\)", text)
            if pos_match:
                pos = Position(*map(int, pos_match.groups()))
            else:
                pos = Position(0, 0)
                logger.warning(f"No position found in line: {text}")

            text = re.sub(r"{([^}]*)\\c&[0-9a-fhA-FH]([^}]*)}(\s*{\\c&[0-9a-fhA-FH][^}]*})", r"{\1\2}\3", text)
            color_match = re.search(r"\\c([&hH0-9a-fA-F]+?)(?=[\\}])", text)
            color = Color.parse(color_match.group(1)) if color_match else Color(255, 255, 255)

            text = OVERRIDE_BLOCK_PATTERN.sub("", text)

            return Dialog(start, end, style, text, name, pos, color)

        doc = cls()
        lines = ass_text.splitlines()
        for line in lines:
            if line.startswith("Dialogue:"):
                doc.events.append(parse_ass_dialog(line))
            elif "ResX:" in line:
                try:
                    doc.res_x = int(re.search(r"ResX: ?(\d+)", line).group(1))
                except ValueError:
                    logger.warning("PlayResX is not a number")
            elif "ResY:" in line:
                try:
                    doc.res_y = int(re.search(r"ResY: ?(\d+)", line).group(1))
                except ValueError:
                    logger.warning("PlayResY is not a number")
        return doc

    def to_ass(self, show_speaker: bool = False, ending_char: str = "") -> str:
        return ASS_HEADER + self.events.to_ass_string(show_speaker, ending_char)

    def to_srt(self, show_speaker: bool = False, ending_char: str = "") -> str:
        return self.events.to_srt_string(show_speaker, ending_char)

    def to_txt(self, show_speaker: bool = False, ending_char: str = "", show_pause_tip: int = 0) -> str:
        result = []
        last_end = 0
        for event in self.events:
            if event.start - last_end >= show_pause_tip * 1000 > 0:
                result.append(f"({(event.start - last_end) // 1000}-second pause)")
            last_end = event.end
            text = event.text.replace("\n", "\u3000")
            result.append(
                f"[{event.name}]\t{text}{ending_char}"
                if show_speaker
                else f"{text}{ending_char}"
            )
        return "\n".join(result)

    def save(self, path: Path | str) -> None:  # 移除config参数
        text = self.to_srt(show_speaker=False, ending_char="")  # 固定参数
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def __repr__(self) -> str:
        return f"Subtitle(with {len(self.events)} events)"


load = Subtitle.load
from_ass_text = Subtitle.from_ass_text
