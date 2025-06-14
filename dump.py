#!/usr/bin/env python3

import pathlib
import json

exts = dict()

SHOW_EXTENSION = True
SHOW_ISA_SET = True
SHOW_CATEGORY = True
SHOW_ICLASS = True

def read_cfg_file(file_path):
    parent_path = file_path.parent
    instr_files = []
    with open(file_path, 'r') as file:
        # find all dec-instructions
        for line in file:
            if line.strip().startswith("dec-instruction"):
                instr_files.append(line.split(':')[1].strip())
    in_desc = False
    cur_desc = dict()
    for instr_file in instr_files:
        instr_path = parent_path / instr_file
        with open(instr_path, 'r') as instr_file_handle:
            for instr_line in instr_file_handle:
                if instr_line.strip().startswith("{"):
                    in_desc = True
                elif instr_line.strip().startswith("}"):
                    assert 'ICLASS' in cur_desc, f"Missing 'iclass' in {instr_file}"
                    assert 'EXTENSION' in cur_desc, f"Missing 'extension' in {instr_file}"
                    assert 'CATEGORY' in cur_desc, f"Missing 'category' in {instr_file}"
                    next_level = exts
                    if SHOW_EXTENSION:
                        ext = cur_desc['EXTENSION']
                        if ext not in next_level:
                            next_level[ext] = dict()
                        next_level = next_level[ext]
                    if SHOW_ISA_SET:
                        isa_set = cur_desc.get('ISA_SET', 'default')
                        if isa_set not in next_level:
                            next_level[isa_set] = dict()
                        next_level = next_level[isa_set]
                    if SHOW_CATEGORY:
                        cat = cur_desc['CATEGORY']
                        if cat not in next_level:
                            next_level[cat] = dict()
                        next_level = next_level[cat]
                    if SHOW_ICLASS:
                        iclass = cur_desc['ICLASS']
                        if iclass not in next_level:
                            next_level[iclass] = dict()
                        next_level = next_level[iclass]
                    in_desc = False
                    cur_desc = dict()
                elif in_desc:
                    key = instr_line[:instr_line.find(":")].strip()
                    value = instr_line[instr_line.find(":") + 1:].strip()
                    cur_desc[key] = value

if __name__ == "__main__":
    # find all files.cfg in ext/xed/datafiles
    for path in pathlib.Path("ext/xed/datafiles").rglob("*.cfg"):
        read_cfg_file(path)
    # write the exts dict to a json file
    print(json.dumps(exts, indent=4, sort_keys=True))
