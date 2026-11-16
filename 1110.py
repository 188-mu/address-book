import csv
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
JSON_PATH = BASE_DIR / "contacts.json"
BAK_PATH = BASE_DIR / "contacts.bak.json"   # 仅给主流程做默认值展示用
CSV_PATH = BASE_DIR / "contacts.csv"
FIELDS = ["name", "phone", "note"]


# ---------- 数据层：读写文件 ----------
def backup_path_of(path: Path) -> Path:
    """由数据文件推导备份文件名：contacts.json → contacts.bak.json
    关键修正：备份路径必须跟着传入的 path 走，不能写死全局常量。"""
    return path.with_name(path.stem + ".bak" + path.suffix)


def load_contacts(path: Path = JSON_PATH) -> list[dict]:
    """从 JSON 读通讯录。文件不存在返回空列表；文件损坏给提示并返回空列表。"""
    if not path.exists():
        print(f"[提示] 还没有 {path.name}，从空通讯录开始。")
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("顶层不是列表")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[警告] {path.name} 内容坏了（{e}），本次按空通讯录启动。")
        print("[警告] 原文件没有被动过，你可以手动检查它。")
        return []
    # 修正4：脏数据过滤——列表里混进字符串/数字也不会让整个程序崩
    clean = []
    for item in data:
        if isinstance(item, dict) and str(item.get("name", "")).strip():
            clean.append({k: str(item.get(k, "") or "") for k in FIELDS})
    if len(clean) != len(data):
        print(f"[提示] 跳过 {len(data) - len(clean)} 条格式不对的记录。")
    return clean


def save_contacts(contacts: list[dict], path: Path = JSON_PATH) -> None:
    """保存通讯录。先备份旧文件，再写临时文件，最后原子替换，防止中途崩溃清空原数据。"""
    bak = backup_path_of(path)
    if path.exists():
        os.replace(path, bak)
        print(f"[备份] 旧数据已存为 {bak.name}")

    tmp = path.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)      # 原子替换：写成功了才顶替原文件
    except OSError as e:
        # 修正4：写失败把半成品临时文件删掉，别留垃圾；原数据还在 bak 里
        print(f"[错误] 写入失败：{e}")
        if tmp.exists():
            tmp.unlink()
        return
    print(f"[保存] {len(contacts)} 位联系人已写入 {path.name}")


def export_csv(contacts: list[dict], path: Path = CSV_PATH) -> None:
    """导出 CSV，Excel 可直接打开。utf-8-sig 带 BOM，避免 Excel 中文乱码。"""
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")  # 修正3
        writer.writeheader()
        # 缺字段自动补空字符串，不会因为 note 缺失而写坏
        writer.writerows({k: c.get(k, "") for k in FIELDS} for c in contacts)
    print(f"[导出] {len(contacts)} 位联系人已写入 {path.name}")


# ---------- 业务层：W005 的 5 个函数原样保留 ----------
def add_contact(contacts: list[dict], name: str, phone: str, note: str = "") -> bool:
    for c in contacts:
        if c["name"] == name:
            print(f"[跳过]「{name}」已在通讯录里，电话是 {c['phone']}，不重复添加。")
            return False
    contacts.append({"name": name, "phone": phone, "note": note})
    print(f"[添加]「{name}」已加入通讯录。")
    return True


def find_contact(contacts: list[dict], name: str) -> dict | None:
    for c in contacts:
        if c["name"] == name:
            return c
    return None


def show_contact(contacts: list[dict], name: str) -> None:
    hit = find_contact(contacts, name)
    if hit is None:
        print(f"[没找到] 通讯录里没有「{name}」，要不要先添加？")
        return
    note = hit["note"] or "（无备注）"
    print(f"[找到] {hit['name']}｜{hit['phone']}｜{note}")


def delete_contact(contacts: list[dict], name: str) -> bool:
    target = find_contact(contacts, name)
    if target is None:
        print(f"[没找到]「{name}」不在通讯录里，删不了。")
        return False
    contacts.remove(target)
    print(f"[删除]「{name}」已从通讯录移除。")
    return True


def list_contacts(contacts: list[dict]) -> None:
    if not contacts:
        print("[空] 通讯录里还没有人。")
        return
    print(f"--- 共 {len(contacts)} 位联系人 ---")
    for i, c in enumerate(contacts, start=1):
        note = c["note"] or "（无备注）"
        print(f"{i}. {c['name']:<6} {c['phone']:<12} {note}")


def first_letters(contacts: list[dict]) -> set[str]:
    letters: set[str] = set()
    for c in contacts:
        if c["name"]:
            letters.add(c["name"][0])
    return letters


# ---------- 主流程：启动读、操作、退出存 ----------
def main() -> None:
    contacts = load_contacts()
    print(f"[启动] 当前有 {len(contacts)} 位联系人。")
    while True:
        print("\n--- 通讯录 v2（数据会保存）---")
        print("1 添加  2 查找  3 列出  4 删除  5 首字母  6 保存  7 导出CSV  0 退出")
        choice = input("选一个：").strip()
        if choice == "1":
            name = input("姓名：").strip()
            if not name:
                print("[提示] 姓名不能为空。")
                continue
            phone = input("电话：").strip()
            note = input("备注（可空）：").strip()
            add_contact(contacts, name, phone, note)
        elif choice == "2":
            show_contact(contacts, input("要找谁：").strip())
        elif choice == "3":
            list_contacts(contacts)
        elif choice == "4":
            delete_contact(contacts, input("要删谁：").strip())
        elif choice == "5":
            print(f"首字母集合：{first_letters(contacts)}")
        elif choice == "6":
            save_contacts(contacts)
        elif choice == "7":
            export_csv(contacts)
        elif choice == "0":
            save_contacts(contacts)
            print("已保存，再见。")
            break
        else:
            print("[提示] 输入 0–7。")


def _self_test() -> None:
    """自测：用临时目录跑，绝对不碰真实数据文件。"""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        jp, cp = d / "c.json", d / "c.csv"
        bp = backup_path_of(jp)          # 修正1：备份路径由 jp 推导 = d/c.bak.json

        # 1) 文件不存在 → 空列表
        assert load_contacts(jp) == []

        # 2) 存 → 读回，中文不转义
        cs = [{"name": "张三", "phone": "1", "note": "室友"}]
        save_contacts(cs, jp)
        assert jp.exists()
        assert "张三" in jp.read_text(encoding="utf-8")      # ensure_ascii=False 生效
        assert load_contacts(jp) == cs

        # 3) 再存一次 → 生成备份，且备份就在临时目录里
        save_contacts(cs, jp)
        assert bp.exists(), "备份文件没生成"

        # 4) 坏文件 → 不崩、返回空、原文件还在
        jp.write_text("{这不是JSON", encoding="utf-8")
        assert load_contacts(jp) == []
        assert jp.read_text(encoding="utf-8") == "{这不是JSON"

        # 5) 脏数据 → 被过滤不崩
        jp.write_text('[{"name":"李四","phone":"2"}, "垃圾", 123]', encoding="utf-8")
        assert load_contacts(jp) == [{"name": "李四", "phone": "2", "note": ""}]

        # 6) CSV 导出 + 多余字段不报错
        export_csv([{"name": "张三", "phone": "1", "note": "室友", "wechat": "abc"}], cp)
        assert cp.exists()
        assert "张三" in cp.read_text(encoding="utf-8-sig")

    print("[自测] 全部通过")


if __name__ == "__main__":
    # 修正2：自测与主程序分离，加 --test 就只跑自测
    if "--test" in sys.argv:
        _self_test()
    else:
        main()
