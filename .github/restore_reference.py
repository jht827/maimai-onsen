from hashlib import sha256
from pathlib import Path
import os

target = Path("参考资料/MaimaiDX-D.pdf")
expected = "a69fd54057c2135490fdb54a2b8b98a71baa64e31a4955e271a075e184e12af1"
expected_size = 53618283
parts = [target.with_name(target.name + suffix) for suffix in (".part01", ".part02")]

if target.exists():
    if target.stat().st_size == expected_size and sha256(target.read_bytes()).hexdigest() == expected:
        print("Original PDF already verified.")
        raise SystemExit(0)
    raise SystemExit("Refusing to overwrite an unexpected existing PDF.")

temporary = target.with_name(target.name + ".uploading")
digest = sha256()
size = 0
try:
    with temporary.open("xb") as output:
        for part in parts:
            with part.open("rb") as source:
                while data := source.read(1024 * 1024):
                    output.write(data)
                    digest.update(data)
                    size += len(data)
    if size != expected_size or digest.hexdigest() != expected:
        raise ValueError("Original PDF size or SHA-256 mismatch.")
    os.replace(temporary, target)
except Exception:
    temporary.unlink(missing_ok=True)
    raise
print(f"Verified original PDF: {size} bytes; SHA-256 {expected}")
