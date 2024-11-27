#!/usr/bin/env python3

from typing import Dict, Any

from source.subs_not_ass.steps.on_library_management_file_test import on_library_management_file_test_make_from_dict
from source.subs_not_ass.steps.on_post_processor_file_movement import on_post_processor_file_movement_make_from_dict
from source.subs_not_ass.steps.on_worker_process_data import on_worker_process_data_make_from_dict


def on_library_management_file_test(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Runner function - enables additional actions during the library management file tests.
    The 'data' object argument includes:
        library_id                      - The library that the current task is associated with
        path                            - String containing the full path to the file being tested.
        issues                          - List of currently found issues for not processing the file.
        add_file_to_pending_tasks       - Boolean, is the file currently marked to be added to the queue for processing.
        priority_score                  - Integer, an additional score that can be added to set the position of the new task in the task queue.
        shared_info                     - Dictionary, information provided by previous plugin runners. This can be appended to for subsequent runners.
    :param data:
    :return:
    """
    dc = on_library_management_file_test_make_from_dict(data)
    new_data = dc.as_dict()
    data.update(new_data)
    return new_data


def on_worker_process(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runner function - enables additional configured processing jobs during the worker stages of a task.

    The 'data' object argument includes:
        worker_log              - Array, the log lines that are being tailed by the frontend. Can be left empty.
        library_id              - Number, the library that the current task is associated with.
        exec_command            - Array, a subprocess command that Unmanic should execute. Can be empty.
        command_progress_parser - Function, a function that Unmanic can use to parse the STDOUT of the command to collect progress stats. Can be empty.
        file_in                 - String, the source file to be processed by the command.
        file_out                - String, the destination that the command should output (may be the same as the file_in if necessary).
        original_file_path      - String, the absolute path to the original file.
        repeat                  - Boolean, should this runner be executed again once completed with the same variables.

    :param data:
    :return:
    """
    dc = on_worker_process_data_make_from_dict(data)
    new_data = dc.as_dict()
    data.update(new_data)
    return new_data


def on_postprocessor_file_movement(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runner function - configures additional postprocessor file movements during the postprocessor stage of a task.

    The 'data' object argument includes:
        source_data             - Dictionary containing data pertaining to the original source file.
        remove_source_file      - Boolean, should Unmanic remove the original source file after all copy operations are complete.
        copy_file               - Boolean, should Unmanic run a copy operation with the returned data variables.
        file_in                 - The converted cache file to be copied by the postprocessor.
        file_out                - The destination file that the file will be copied to.

    :param data:
    :return:
    """
    dc = on_post_processor_file_movement_make_from_dict(data)
    new_data = dc.as_dict()
    data.update(new_data)
    return new_data
