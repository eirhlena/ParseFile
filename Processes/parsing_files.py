from Processes.Query_execution_summary_file import QuerySummary
from Processes.Task_execution_summary_file import TaskSummary
from Processes.Detailed_metrics_per_task_file import TaskMetricsDetails
import logging


class ParseInputFile:
    def parse_file(self, filepath):
        with open(filepath) as input_file:
            line = input_file.readline()
            while line:  # The EOF char is an empty string
                # 'Query Execution Summary' in line:
                if 'OPERATION' in line:
                    query_summary = QuerySummary()
                    query_summary.create_summary_file(input_file)
                # 'Task Execution Summary' in line:
                elif 'VERTICES' in line:
                    task_summary = TaskSummary()
                    task_summary.create_summary_file(line, input_file)
                elif 'org.apache.tez.common.counters.DAGCounter' in line:
                    detailed_metrics = TaskMetricsDetails()
                    detailed_metrics.generate_metrics_file(line, input_file)

                line = input_file.readline()
        logging.info("Input file parsing completed successfully")
