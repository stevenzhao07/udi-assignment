#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
udi_assign.py — UDI 赋码工具
=============================
GS1 GTIN 校验位（mod-10）+ DI/PI 拆分 + carrierHRF 生成 +
FDA GUDID / NMPA 器械 UDI / EUDAMED 三侧数据库字段对照。

诚实边界：校验位算法为公开数学（可本地验证）；各辖区数据库字段口径
以官方最新指南为准（GUDID/NMPA 填报口径可能更新，TO_BE_VERIFIED 占位）。
"""
from __future__ import annotations
import argparse
import sys


def gs1_check_digit(digits: str) -> int:
    """GS1 mod-10：从右起奇数位×3 + 偶数位×1，校验位 = (10 - 和%10) % 10。"""
    if not digits.isdigit():
        raise ValueError("须为纯数字")
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        total += n * 3 if i % 2 == 0 else n
    return (10 - total % 10) % 10


def validate_gtin(gtin: str) -> dict:
    body, check = gtin[:-1], int(gtin[-1])
    calc = gs1_check_digit(body)
    return {"gtin": gtin, "长度": len(gtin), "校验位": check,
            "计算校验位": calc, "判据": "PASS" if check == calc else "BLOCK（校验位不符）"}


def build_carrier(di: str, lot: str = "", exp: str = "", serial: str = "",
                  mfg: str = "") -> dict:
    """carrierHRF：(01)DI (10)批号 (17)有效期 (21)序列号 (11)生产日期。"""
    parts = [f"(01){di}"]
    if mfg:
        parts.append(f"(11){mfg}")
    if lot:
        parts.append(f"(10){lot}")
    if exp:
        parts.append(f"(17){exp}")
    if serial:
        parts.append(f"(21){serial}")
    return {"DI": di, "PI": {"批号": lot, "有效期": exp, "序列号": serial, "生产日期": mfg},
            "carrierHRF": "".join(parts)}


UDI_DB_FIELDS = [
    # (字段, FDA GUDID, NMPA UDI, EUDAMED)
    # EU 列注意：Basic UDI-DI 是 EUDAMED 主标识（MDR Art.27/Annex VI C，
    # 一组器械共用），≠ 载体上承载的 UDI-DI（GS1 GTIN 等），不可混为一谈。
    ("Device Identifier (DI)", "Primary DI", "产品标识（DI）", "Basic UDI-DI（EUDAMED 主标识，非 UDI-DI）"),
    ("版本/型号", "Version or Model", "型号规格", "Device reference/number"),
    ("批号/序列号（PI）", "Production Identifier(s)", "生产标识（PI）", "PI (as applicable)"),
    ("生产日期/有效期", "Expiration Date / Mfg Date", "生产日期/失效日期", "Expiry date"),
    ("UDI 赋码载体类型", "Carrier Type (AIDC/HRF)", "载体类型", "Carrier"),
    ("GMDN/器械术语", "FDA Product Code + GMDN", "分类目录编号", "EUDAMED nomenclature"),
    ("无菌/灭菌方式", "Sterility / Single Use", "无菌状态/灭菌方式", "Sterile / Sterilization"),
    ("存储与搬运", "Storage & Handling", "储存条件", "Storage/handling"),
]


def _demo() -> int:
    print("UDI 赋码工具 · 演示\n")
    print(_r := f"GTIN 校验位: 0987654321098 → {gs1_check_digit('0987654321098')}"
          f"（完整 GTIN-14 = 0987654321098{gs1_check_digit('0987654321098')}）")
    print(validate_gtin(f"0987654321098{gs1_check_digit('0987654321098')}"))
    c = build_carrier("09876543210987", lot="A1", exp="20280101", serial="SN001", mfg="260101")
    print(f"carrierHRF: {c['carrierHRF']}")
    print("\n### 三侧 UDI 数据库字段对照（口径以官方指南为准，TO_BE_VERIFIED 占位）")
    for row in UDI_DB_FIELDS:
        print("  " + " | ".join(row))
    print("\n[demo] 校验位可离线验证；字段口径须按 GUDID/NMPA/EUDAMED 最新填报指南复核。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="UDI 赋码工具")
    ap.add_argument("--demo", action="store_true", help="跑内置演示")
    ap.add_argument("--gtin", help="GTIN-13/14，计算或验证校验位")
    ap.add_argument("--carrier", action="store_true", help="生成 carrierHRF")
    ap.add_argument("--di", help="Device Identifier（14 位 GTIN）")
    ap.add_argument("--lot", default="")
    ap.add_argument("--exp", default="")
    ap.add_argument("--serial", default="")
    ap.add_argument("--mfg", default="")
    ap.add_argument("--fields", action="store_true", help="打印三侧数据库字段对照")
    args = ap.parse_args()

    if args.demo:
        return _demo()
    if args.fields:
        for row in UDI_DB_FIELDS:
            print(" | ".join(row))
        return 0
    if args.gtin:
        if len(args.gtin) in (13, 14):
            if len(args.gtin) == 14:
                d = validate_gtin(args.gtin)
                print(f"校验位: {d['校验位']} 计算: {d['计算校验位']} → {d['判据']}")
            else:
                print(f"GTIN-13 {args.gtin} 的校验位 = {gs1_check_digit(args.gtin)}")
            return 0
        print("[err] GTIN 须 13 或 14 位")
        return 2
    if args.carrier:
        if not args.di:
            print("[err] --carrier 须配 --di")
            return 2
        c = build_carrier(args.di, args.lot, args.exp, args.serial, args.mfg)
        print(f"carrierHRF: {c['carrierHRF']}")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
