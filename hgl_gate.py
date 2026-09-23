"""Fail-closed CI gate. A candidate must end with an unchecked Development."""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

GATE = "hegelese-gate/0.2.0"
SOURCE_LIMIT = 128 * 1024
REQUEST_LIMIT = 256 * 1024
OUTPUT_LIMIT = 1024 * 1024
EXIT = {"ExhaustivelyChecked": 0, "Refuted": 1, "Invalid": 2, "Unknown": 3, "InternalError": 4}


def failure(status, message):
    return {"gate": GATE, "status": status, "accepted": False,
            "diagnostics": [{"message": message}]}


def read_regular(path, limit):
    # Do not let a candidate path turn into a pipe or follow a symlink.
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("Input must be a regular file.")
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Input exceeds its byte limit.")
    return data.decode("utf-8")


def worker(payload):
    # This directory is the installed/reviewed engine, never the candidate checkout.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import hegelese as finite
    import hgl
    evaluator = hgl.Evaluator(payload["filename"], payload["fuel"], payload["budget"])
    try:
        request = finite.loads_json(payload["request"])
        value = evaluator.program(hgl.Parser(payload["source"]).program())
        if not isinstance(value, hgl.Development):
            return failure("Invalid", "Candidate must return an unchecked Upheaval, not data or an evidence report.")
        # Use the caller's request, never the candidate's embedded request as authority.
        report = finite.check(request, value.proposal, payload["budget"])
        report.update(gate=GATE, source_location=evaluator.location(value.token))
        return report
    except hgl.Diagnostic as error:
        result = failure(error.status, error.message)
        result["diagnostics"][0]["location"] = evaluator.location(error.token)
        return result
    except (finite.Invalid, ValueError, TypeError, KeyError) as error:
        return failure("Invalid", str(error))
    except (RecursionError, MemoryError):
        return failure("Unknown", "Worker resource limit reached; no acceptance.")


def worker_main():
    try:
        # Linux production profile. macOS local checks retain the parent deadline.
        payload = json.loads(sys.stdin.buffer.read(6 * (SOURCE_LIMIT + REQUEST_LIMIT) + 65536))
        if sys.platform.startswith("linux"):
            import resource
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024,) * 2)
            resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(payload["timeout"]),) * 2)
            resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_LIMIT,) * 2)
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        report = worker(payload)
        encoded = json.dumps(report, ensure_ascii=True).encode("utf-8")
        if len(encoded) > OUTPUT_LIMIT:
            encoded = json.dumps(failure("Unknown", "Evidence exceeds the output limit.")).encode()
        sys.stdout.buffer.write(encoded)
        return 0
    except Exception:
        sys.stdout.write(json.dumps(failure("InternalError", "Worker failed; no acceptance.")))
        return 4


def gate(source, request, filename="candidate.hgl", fuel=100000, budget=100000, timeout=5.0):
    if (type(fuel) is not int or not 0 <= fuel <= 1_000_000 or
            type(budget) is not int or not 0 <= budget <= 1_000_000 or
            type(timeout) not in (int, float) or not math.isfinite(timeout) or not 0 < timeout <= 30):
        return failure("Invalid", "Fuel/budget must be 0..1000000; timeout must be greater than 0 and at most 30 seconds.")
    try:
        source_bytes, request_bytes = source.encode("utf-8"), request.encode("utf-8")
    except (AttributeError, UnicodeError):
        return failure("Invalid", "Source and request must be valid Unicode strings.")
    if len(source_bytes) > SOURCE_LIMIT or len(request_bytes) > REQUEST_LIMIT:
        return failure("Invalid", "Source or request exceeds the gate byte limit.")
    payload = json.dumps(dict(source=source, request=request, filename=filename,
                              fuel=fuel, budget=budget, timeout=timeout), ensure_ascii=False).encode()
    # Temp files keep child output out of an unbounded communicate() memory buffer.
    with tempfile.TemporaryDirectory(prefix="hegelese-gate-") as directory:
        with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
            try:
                child = subprocess.Popen([sys.executable, "-I", str(Path(__file__).resolve()), "--worker"],
                                         stdin=subprocess.PIPE, stdout=output, stderr=errors,
                                         cwd=directory, env={"PATH": os.defpath})
                try:
                    child.communicate(payload, timeout=timeout)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.communicate()
                    report = failure("Unknown", "Worker wall-clock deadline exceeded.")
                else:
                    output.seek(0)
                    data = output.read(OUTPUT_LIMIT + 1)
                    if child.returncode < 0:
                        report = failure("Unknown", "Worker terminated before completing its checks.")
                    elif child.returncode != 0:
                        report = failure("InternalError", "Worker failed; no acceptance.")
                    elif len(data) > OUTPUT_LIMIT:
                        report = failure("Unknown", "Worker output limit exceeded.")
                    else:
                        report = json.loads(data)
                finally:
                    if child.stdin:
                        try:
                            child.stdin.close()
                        except BrokenPipeError:
                            pass
            except (OSError, ValueError):
                report = failure("InternalError", "Unable to execute or decode checker worker.")
    if type(report) is not dict or report.get("status") not in EXIT or type(report.get("accepted")) is not bool:
        report = failure("InternalError", "Worker returned an invalid report.")
    elif report["accepted"] != (report["status"] == "ExhaustivelyChecked"):
        report = failure("InternalError", "Worker returned inconsistent evidence.")
    report["gate"] = GATE
    report["candidate_sha256"] = hashlib.sha256(source_bytes).hexdigest()
    report["request_file_sha256"] = hashlib.sha256(request_bytes).hexdigest()
    report["execution_limits"] = {"fuel": fuel, "check_budget": budget, "timeout_seconds": timeout,
                                  "linux_resource_limits": sys.platform.startswith("linux")}
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=GATE)
    parser.add_argument("source")
    parser.add_argument("--request", required=True)
    parser.add_argument("--report", help="Atomically save the JSON report at this path.")
    parser.add_argument("--fuel", type=int, default=100000)
    parser.add_argument("--budget", type=int, default=100000)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args(argv)
    try:
        source = read_regular(args.source, SOURCE_LIMIT)
        request = read_regular(args.request, REQUEST_LIMIT)
        report = gate(source, request, str(args.source), args.fuel, args.budget, args.timeout)
    except (OSError, ValueError) as error:
        report = failure("Invalid", str(error))
    text = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    if args.report:
        temporary = None
        try:
            destination = Path(args.report)
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent, delete=False) as stream:
                temporary = stream.name
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, destination)
        except OSError:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
            print(json.dumps(failure("InternalError", "Could not save the required report.")))
            return 4
    print(text, end="")
    return EXIT[report["status"]]


if __name__ == "__main__":
    sys.exit(worker_main() if sys.argv[1:] == ["--worker"] else main())
