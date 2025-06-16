from pathlib import Path

from ci.praktika.info import Info
from ci.praktika.result import Result
from ci.praktika.utils import Utils


def main():
    info = Info().job_name

    fuzzer_name = (
        "BuzzHouse" if info.job_name.lower().startswith("buzzhouse") else "AST Fuzzer"
    )

    temp_path = Path("./ci/tmp")
    assert (temp_path / "clickhouse").exists(), f"Binary not found in {temp_path}"
    Utils.add_to_PATH(temp_path)

    commands = [
        f"chmod +x {temp_path}/clickhouse",
        f"ln -sf {temp_path}/clickhouse {temp_path}/clickhouse-server",
        f"ln -sf {temp_path}/clickhouse {temp_path}/clickhouse-client",
        f"ln -sf {temp_path}/clickhouse {temp_path}/clickhouse-local",
        f"FUZZER_TO_RUN={fuzzer_name} ci/docker/fuzzer/run-fuzzer.sh",
    ]

    run_result = Result.from_commands_run(name="run", command=commands)
    run_result.complete_job()
    # paths = {
    #     "report.html": workspace_path / "report.html",
    #     "core.zst": workspace_path / "core.zst",
    #     "dmesg.log": workspace_path / "dmesg.log",
    #     "fatal.log": workspace_path / "fatal.log",
    #     "stderr.log": workspace_path / "stderr.log",
    # }
    #
    # compressed_server_log_path = workspace_path / "server.log.zst"
    # if compressed_server_log_path.exists():
    #     paths["server.log.zst"] = compressed_server_log_path
    # else:
    #     # The script can fail before the invocation of `zstd`, but we are still interested in its log:
    #     not_compressed_server_log_path = workspace_path / "server.log"
    #     if not_compressed_server_log_path.exists():
    #         paths["server.log"] = not_compressed_server_log_path
    #
    # # Same idea but with the fuzzer log
    # compressed_fuzzer_log_path = workspace_path / "fuzzer.log.zst"
    # if compressed_fuzzer_log_path.exists():
    #     paths["fuzzer.log.zst"] = compressed_fuzzer_log_path
    # else:
    #     not_compressed_fuzzer_log_path = workspace_path / "fuzzer.log"
    #     if not_compressed_fuzzer_log_path.exists():
    #         paths["fuzzer.log"] = not_compressed_fuzzer_log_path
    #
    # # Same idea but with the fuzzer output SQL
    # compressed_fuzzer_output_sql_path = workspace_path / "fuzzer_out.sql.zst"
    # if compressed_fuzzer_output_sql_path.exists():
    #     paths["fuzzer_out.sql.zst"] = compressed_fuzzer_output_sql_path
    # else:
    #     not_compressed_fuzzer_output_sql_path = workspace_path / "fuzzer_out.sql"
    #     if not_compressed_fuzzer_output_sql_path.exists():
    #         paths["fuzzer_out.sql"] = not_compressed_fuzzer_output_sql_path
    #
    # # Try to get status message saved by the fuzzer
    # try:
    #     with open(workspace_path / "status.txt", "r", encoding="utf-8") as status_f:
    #         status = status_f.readline().rstrip("\n")
    #
    #     with open(workspace_path / "description.txt", "r", encoding="utf-8") as desc_f:
    #         description = desc_f.readline().rstrip("\n")
    # except:
    #     status = FAILURE
    #     description = "Task failed: $?=" + str(retcode)
    #
    # test_result = TestResult(description, OK)
    # if "fail" in status:
    #     test_result.status = FAIL
    #
    # JobReport(
    #     description=description,
    #     test_results=[test_result],
    #     status=status,
    #     start_time=stopwatch.start_time_str,
    #     duration=stopwatch.duration_seconds,
    #     # test generates its own report.html
    #     additional_files=[v for _, v in paths.items() if Path(v).is_file()],
    # ).dump()
    #
    # logging.info("Result: '%s', '%s'", status, description)
    # if status != SUCCESS:
    #     sys.exit(1)


if __name__ == "__main__":
    main()
