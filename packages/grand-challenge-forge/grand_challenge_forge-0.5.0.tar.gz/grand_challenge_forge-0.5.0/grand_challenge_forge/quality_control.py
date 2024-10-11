import glob
import logging
import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

from grand_challenge_forge import RESOURCES_PATH
from grand_challenge_forge.exceptions import QualityFailureError
from grand_challenge_forge.utils import (
    change_directory,
    directly_import_module,
)

logger = logging.getLogger(__name__)


def upload_to_archive_script(script_dir):
    """Checks if the upload to archive script works as intended"""
    logger.debug(f"Quality check over script in {script_dir}")

    try:
        with change_directory(script_dir):
            gcapi = MagicMock()
            with patch.dict("sys.modules", gcapi=gcapi):
                try:
                    # Load the script as a module
                    upload_files = directly_import_module(
                        name="upload_files",
                        path=script_dir / "upload_files.py",
                    )

                    # Run the script, but noop print
                    def debug_print(arg):
                        logger.debug(arg)

                    with patch("builtins.print", debug_print):
                        upload_files.main()
                except Exception as e:
                    raise QualityFailureError(
                        f"Upload script could not be loaded or run. {e}"
                    ) from e

            # Assert that it reaches out via gcapi
            try:
                gcapi.Client.assert_called()
                gcapi.Client().archive_items.create.assert_called()
                gcapi.Client().update_archive_item.assert_called()
            except AssertionError as e:
                raise QualityFailureError(
                    f"Upload script does not contact grand-challenge. {e}"
                ) from e
    except (FileNotFoundError, SyntaxError) as e:
        raise QualityFailureError(
            f"Upload script does not seem to exist or is not valid: {e}"
        ) from e
    logger.debug("💚 Quality OK!")


def example_algorithm(phase_context, algorithm_dir):
    """Checks if the example algorithm works as intended"""
    logger.debug(f"Quality check over algorithm in: {algorithm_dir}")

    # Run it twice to ensure all permissions are correctly handled
    runs = 2
    for n in range(0, runs):
        logger.debug(
            f"Staring quality check run [{n+1}/{runs}] over example algorithm"
        )
        _test_example_algorithm(phase_context, algorithm_dir, number_run=n + 1)

    _test_example_algorithm_save(phase_context, algorithm_dir)

    logger.debug("💚 Quality OK!")


def _test_example_algorithm(phase_context, algorithm_dir, number_run):
    output_dir = algorithm_dir / "test" / "output"

    _test_subprocess(
        script_dir=algorithm_dir,
        number_run=number_run,
        script_name="test_run.sh",
    )

    # Check if output is generated (ignore content)
    for output in phase_context["phase"]["algorithm_outputs"]:
        expected_file = output_dir / output["relative_path"]
        if not expected_file.exists():
            raise QualityFailureError(
                f"Example algorithm does not generate output on run {number_run}: "
                f"{output['relative_path']}"
            )


def _test_save(pattern, script_dir):
    logger.debug(
        "Testing container save, using a mock save function for efficiency"
    )

    matching_files = glob.glob(pattern)

    assert len(matching_files) == 0

    mocks_bin = RESOURCES_PATH / "mocks" / "bin"
    current_path = os.environ.get("PATH", "")
    extended_path = f"{mocks_bin}:{current_path}"

    with patch.dict("os.environ", PATH=extended_path):
        _test_subprocess(
            script_dir=script_dir,
            number_run=1,
            script_name="save.sh",
        )

    # Check if saved image exists
    matching_files = glob.glob(pattern)
    if not len(matching_files) == 1:
        raise QualityFailureError(
            f"Example save.sh does not generate the exported image matching: "
            f"{pattern}"
        )

    for filename in matching_files:
        os.remove(filename)


def _test_example_algorithm_save(phase_context, algorithm_dir):
    pattern = str(
        algorithm_dir
        / f"example-algorithm-{phase_context['phase']['slug']}_*.tar.gz"
    )
    _test_save(pattern, script_dir=algorithm_dir)


def example_evaluation(phase_context, evaluation_dir):
    """Checks if the example evaluation works as intended"""
    logger.debug(f"Quality check over evaluation in: {evaluation_dir}")

    # Run it twice to ensure all permissions are correctly handled
    runs = 2
    for n in range(0, runs):
        logger.debug(
            f"Staring quality check run [{n+1}/{runs}] over example evaluation"
        )
        _test_example_evaluation(
            phase_context, evaluation_dir, number_run=n + 1
        )

    _test_example_evaluation_save(phase_context, evaluation_dir)

    logger.debug("💚 Quality OK!")


def _test_example_evaluation(phase_context, evaluation_dir, number_run):
    output_dir = evaluation_dir / "test" / "output"

    _test_subprocess(
        script_dir=evaluation_dir,
        number_run=number_run,
        script_name="test_run.sh",
    )

    # Check if output is generated (ignore content)
    expected_file = output_dir / "metrics.json"
    if not expected_file.exists():
        raise QualityFailureError(
            f"Example evaluation does not generate output on run {number_run}: "
            f"{expected_file}"
        )


def _test_example_evaluation_save(phase_context, evaluation_dir):
    pattern = str(
        evaluation_dir
        / f"example-evaluation-{phase_context['phase']['slug']}_*.tar.gz"
    )
    _test_save(pattern, script_dir=evaluation_dir)


def _test_subprocess(script_dir, number_run, script_name):
    if logger.getEffectiveLevel() is logging.DEBUG:
        kwargs = {
            "stdout": sys.stdout.buffer,
            "stderr": sys.stderr.buffer,
        }
    else:
        kwargs = {
            "capture_output": True,
        }

    result = subprocess.run(
        [script_dir / script_name],
        **kwargs,
    )

    if result.stdout or result.stderr:
        report_output = (
            f"StdOut Log:\n"
            f"{result.stdout.decode(sys.getfilesystemencoding())}"
            f"StdErr Log:\n"
            f"{result.stderr.decode(sys.getfilesystemencoding())}"
        )
        logger.debug(report_output)
    else:
        report_output = None

    if result.returncode != 0:  # Not a clean exit
        raise QualityFailureError(
            f"Script in {script_dir!r} does not exit with 0 "
            f"on run {number_run}" + report_output
            and f":\n {report_output}"
        )
    elif result.stderr:
        raise QualityFailureError(
            f"Example algorithm in {script_dir!r} produces errors "
            f"on run {number_run}" + report_output
            and f":\n {report_output}"
        )

    return result
