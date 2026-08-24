#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

LANGS = {
    "en": ("englishjsons", "en"),
    "nl": ("dutchjsons", "nl"),
    "tr": ("turkishjsons", "tr"),
    "ar": ("arabicjsons", "ar"),
}

TYPES = {"radio", "checkbox", "fillblank", "dragdrop", "resimsech"}


def target_path(test: int, tip: str, dil: str) -> Path:
    if tip not in TYPES:
        raise ValueError(f"Desteklenmeyen soru tipi: {tip}")
    if dil not in LANGS:
        raise ValueError(f"Desteklenmeyen dil: {dil}")
    folder, suffix = LANGS[dil]
    return Path(f"test{test}/{folder}/test{test}-{tip}{suffix}.json")


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not isinstance(data.get("sorular"), list):
        raise ValueError(f"Beklenen JSON yapısı yok: {path}")
    return data


def save_json(path: Path, data):
    # Önce bellekte serialize ederek JSON geçerliliğini garanti et.
    text = json.dumps(data, ensure_ascii=False, indent=4) + "\n"
    path.write_text(text, encoding="utf-8")


def find_index(sorular, numara):
    for i, s in enumerate(sorular):
        if s.get("numara") == numara:
            return i
    return None


def apply_operation(op):
    action = op.get("action")
    test = int(op["test"])
    tip = op["tip"]
    dil = op["dil"]
    path = target_path(test, tip, dil)
    data = load_json(path)
    sorular = data["sorular"]

    if action == "add":
        soru = op.get("soru")
        if not isinstance(soru, dict):
            raise ValueError("add işlemi için 'soru' nesnesi gerekli")
        if "numara" not in soru:
            raise ValueError("Yeni soruda 'numara' alanı gerekli")
        numara = soru["numara"]
        if find_index(sorular, numara) is not None:
            raise ValueError(f"{path}: {numara} numaralı soru zaten mevcut")
        sorular.append(soru)
        if op.get("sort", True):
            sorular.sort(key=lambda x: (x.get("numara") is None, x.get("numara", 0)))

    elif action == "update":
        numara = op.get("numara")
        patch = op.get("patch")
        if numara is None or not isinstance(patch, dict):
            raise ValueError("update işlemi için 'numara' ve 'patch' gerekli")
        idx = find_index(sorular, numara)
        if idx is None:
            raise ValueError(f"{path}: {numara} numaralı soru bulunamadı")
        # numara yanlışlıkla değişmesin; açıkça verilirse aynı kalmalı.
        if "numara" in patch and patch["numara"] != numara:
            raise ValueError("update ile soru numarası değiştirilemez")
        sorular[idx].update(patch)

    elif action == "delete":
        numara = op.get("numara")
        if numara is None:
            raise ValueError("delete işlemi için 'numara' gerekli")
        idx = find_index(sorular, numara)
        if idx is None:
            raise ValueError(f"{path}: {numara} numaralı soru bulunamadı")
        sorular.pop(idx)

    else:
        raise ValueError("action yalnızca add, update veya delete olabilir")

    save_json(path, data)
    print(f"OK: {action} -> {path}")
    return str(path)


def main():
    parser = argparse.ArgumentParser(description="Soru JSON dosyalarında güvenli tek-kayıt işlemleri")
    parser.add_argument("operation_file", help="İşlem tanımını içeren JSON dosyası")
    args = parser.parse_args()

    op_path = Path(args.operation_file)
    with op_path.open("r", encoding="utf-8") as f:
        op = json.load(f)

    # Tek işlem veya işlemler listesi desteklenir.
    operations = op if isinstance(op, list) else [op]
    changed = []
    for item in operations:
        changed.append(apply_operation(item))

    print("CHANGED=" + ",".join(changed))


if __name__ == "__main__":
    main()
