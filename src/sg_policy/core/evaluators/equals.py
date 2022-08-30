import logging

from .base_evaluator import BaseEvaluator

# TODO: Use __name__ for the logger name instead of using the root logger
logger = logging.getLogger()

# Checks if :attr:`value` is equal to :attr:`other`. Automatically casts values to the same type if possible.

# Args:
#     value (mixed): Value to compare.
#     other (mixed): Other value to compare.

# Returns:
#     bool: Whether :attr:`value` is equal to :attr:`other`.

# Example:

#     >>> eq(None, None)
#     True
#     >>> eq(None, '')
#     False
#     >>> eq('a', 'a')
#     True
#     >>> eq(1, str(1))
#     False

# .. versionadded:: 1.0.0-alpha.1


class Equals(BaseEvaluator):
    def sort_lists_in_dicts(self, input):
        if isinstance(input, str) or isinstance(input, float) or isinstance(input, int):
            return input
        try:
            for key in input:
                if isinstance(input[key], list):
                    if isinstance(input[key][0], dict) and isinstance(input[key][0], list):
                        sorted_array = []
                        for index, _ in enumerate(input[key]):
                            sorted_array.append(self.sort_lists_in_dicts(input[key][index]))
                        input[key] = sorted_array
                    else:
                        input[key] = sorted(input[key])
                if isinstance(input[key], dict):
                    self.sort_lists_in_dicts(input[key])
            return input
        except Exception as e:
            logger.exception(str(e))
            return input

    def evaluate(self, evaluator_input, evaluator_data):
        evaluation_result = {"passed": False, "message": "Not evaluated"}
        try:
            value1 = evaluator_input
            value2 = evaluator_data
            # if (
            #         isinstance(evaluator_input, str)
            #         or isinstance(evaluator_input, dict)
            #         or isinstance(evaluator_input, list)
            # ):
            #     value1 = evaluator_input
            # else:
            #     value1 = str(evaluator_data)
            # if (
            #         isinstance(evaluator_data, str)
            #         or isinstance(evaluator_data, dict)
            #         or isinstance(evaluator_data, list)
            # ):
            #     value2 = evaluator_data
            # else:
            #     value2 = str(evaluator_data)
            if isinstance(value1, dict):
                value1 = self.sort_lists_in_dicts(value1)
            if isinstance(value2, dict):
                value2 = self.sort_lists_in_dicts(value2)
            result = value1 == value2
            evaluation_result["passed"] = result
            if result:
                evaluation_result["message"] = "{} is equal to {}".format(value1, value2)
            else:
                evaluation_result["message"] = "{} is not equal to {}".format(value1, value2)
            return evaluation_result
        except Exception as e:
            evaluation_result["message"] = str(e)
            return evaluation_result
