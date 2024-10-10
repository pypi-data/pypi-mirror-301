from .grader import *
from .utils import construct_prompt
from .parser import *
from .trajectory import *
from .python_executor import PythonExecutor


def basic_check(pred, answer):
    """
    This function compares the prediction and the ground truth (answer),
    and returns True if they are the same, otherwise returns False.

    Args:
    pred: The predicted value or output from a model or function.
    answer: The ground truth to compare against.

    Returns:
    bool: True if the prediction is correct, otherwise False.
    """
    return math_equal(pred, answer, timeout=True)


def check(data_name, target, pred, execute=False, vis=False):
    gt_cot, gt_ans = parse_ground_truth(target, data_name)
    pred = strip_string(extract_answer(pred.strip(), data_name))

    if vis:
        print("Extracted answer:", pred)

    if execute:
        try:
            result = math_equal_process((0, pred, gt_ans))
            return result
        except TimeoutError as error:
            print(error)
            return False
        except Exception as error:
            print(error)
            exit()

    else:
        return pred == gt_ans

def extract(data_name, pred):
    pred = strip_string(extract_answer(pred.strip(), data_name))
    return pred
