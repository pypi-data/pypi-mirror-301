import argparse
import os
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="CrcCheckCopy helper")
    parser.add_argument(
        "request",
        metavar="Request",
        type=str,
        nargs="?",
        help="Supported requests: (scan), (verify)",
    )
    parser.add_argument(
        "-l",
        "--location",
        metavar="Location",
        type=Path,
        nargs="?",
        help="The dir to scan/verify against",
        default=Path(),
    )
    parser.add_argument(
        "-hl",
        "--hash_location",
        metavar="Hash Location",
        type=Path,
        nargs="?",
        help="The path to the hash as txt file, e.g /path/to/hash.txt",
        default=Path(),
    )

    args = parser.parse_args()
    request = args.request
    location = args.location
    hash_location = args.hash_location
    exe_location = Path(__file__).parent / "lib"

    if not str(hash_location).lower().endswith(".txt"):
        description = "Expected hash location to be a .txt file"
        raise SystemExit(description, 1)
    if not hash_location.parent.exists():
        description = (
            "Expected the dir to hash_location to exist: "
            f"{hash_location.parent!s}"
        )
        raise SystemExit(description, 1)
    if not location.exists():
        description = f"Expected the location to exist: {location!s}"
        raise SystemExit(description, 1)

    # Move to crccheckcopyutil.exe in order to invoke
    os.chdir(exe_location)

    # Copy the hash file temporarily in the same folder as exe for it to read
    if request == "verify":
        shutil.copy(hash_location, "CRCstamps.txt")

    proc = subprocess.Popen(
        ["cmd", f"/c CrcCheckCopy /{request} {location}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.stdout is not None:
        for line in proc.stdout:
            print(line.decode(errors="ignore").rstrip())

    if proc.stderr is not None:
        for line in proc.stderr:
            print(f"Error: {line.decode(errors='ignore').rstrip()}")

    # Move the resulting hash into specified file location
    if request == "scan":
        shutil.move(str(exe_location / "CRCstamps.txt"), hash_location)

    # Move verification report out of exe location
    # and into same folder where hash is
    if request == "verify":
        shutil.move(
            exe_location / "CrcCheckCopy-verification-report.txt",
            hash_location.parent / "CrcCheckCopy-verification-report.txt",
        )
        # Remove the temp hash
        (exe_location / "CRCstamps.txt").unlink()


if __name__ == "__main__":
    main()
