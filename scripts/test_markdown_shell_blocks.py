#!/usr/bin/env python3

import logging
import os
import re
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def _get_shell_blocks(markdown_file_path: Path) -> list[str]:
    with open(markdown_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.findall(r"```(?:sh|bash|shell)\n(.*?)```", content, re.DOTALL)
    return blocks


def run_shell_blocks(blocks: list[str]):
    for i, block in enumerate(blocks, start=1):
        cleaned_block = block.strip()
        current_working_dir = Path.cwd()
        logger.info("Running block #%i:" % i)
        logger.info(block)
        logger.info("-" * 40)

        try:
            subprocess.run(
                cleaned_block,
                shell=True,
                check=True,
                text=True,
                capture_output=True
            )
            logger.info("OK")
        except subprocess.CalledProcessError as e:
            _log_called_process_error(e)
            sys.exit(e.returncode)

        _update_working_dir(current_working_dir, cleaned_block)

    logger.info("All shell blocks executed successfully!")


def _log_called_process_error(error: subprocess.CalledProcessError):
    logger.error("Error running code block!")
    logger.error("Command: %s\n" % error.cmd)
    logger.error("Exit Code: %i" % error.returncode)
    logger.error("Stderr:\n%s" % error.stderr.strip())


def _update_working_dir(working_dir: Path, code_block: str):
    lines = code_block.split('\n')
    for line in lines:
        if "cd " in line:
            target_dir = re.search(r"\bcd\s+([^\s;&|]+)", line).group(1)
            new_working_dir = (
                Path(target_dir) if target_dir.startswith("/")
                else (Path(working_dir) / target_dir).resolve()
            )
            try:
                os.chdir(new_working_dir)
                logger.info("Changed directory to: %s" % new_working_dir)
            except Exception as e:
                logger.error("Failed to change directory: %s" % e)
                sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.warning("Usage: python3 test_markdown_shell_blocks.py <markdown_file>")
        sys.exit(1)

    markdown_file = Path(sys.argv[1])
    if not markdown_file.exists():
        logger.error("File not found: %s" % markdown_file)
        sys.exit(1)

    shell_blocks = _get_shell_blocks(markdown_file)
    logger.info("Found %i shell code block(s) in %s\n" % (len(shell_blocks), markdown_file))
    if not shell_blocks:
        sys.exit(0)

    run_shell_blocks(shell_blocks)
