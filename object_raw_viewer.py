#!/usr/bin/env python3
import sys
import os
import zlib
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print(f"사용법: {sys.argv[0]} <40자리 커밋(객체) id>")
        sys.exit(1)

    obj_id = sys.argv[1].strip()

    if len(obj_id) != 40:
        print("에러: SHA-1 해시 길이는 40자리여야 합니다.")
        sys.exit(1)

    # 앞 두 자리는 디렉터리, 나머지는 파일 이름
    dir_name = obj_id[:2]
    file_name = obj_id[2:]

    obj_path = Path(".git") / "objects" / dir_name / file_name

    if not obj_path.exists():
        print(f"에러: 객체 파일이 없습니다: {obj_path}")
        sys.exit(1)

    # zlib 압축된 git 객체 읽기
    compressed = obj_path.read_bytes()

    # zlib 해제
    raw = zlib.decompress(compressed)

    # raw 형식: b"타입 크기\\0데이터..."
    header, body = raw.split(b"\x00", 1)

    print("=== 헤더(raw) ===")
    print(header.decode("ascii", errors="replace"))  # 예: "commit 193"

    print("\n=== 전체(raw, repr) ===")
    # 헤더 + \0 + 데이터까지 그대로 보여주고 싶다면
    print(repr(raw))

    print("\n=== 데이터(본문) ===")
    # 커밋/트리/태그/블롭 내용(UTF-8 가정)
    try:
        print(body.decode("utf-8", errors="replace"))
    except UnicodeDecodeError:
        print("[텍스트가 아닌 바이너리 데이터일 수 있습니다]")

if __name__ == "__main__":
    main()
