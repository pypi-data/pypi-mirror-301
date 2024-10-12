import json
from pycoze import utils
import json
import inspect


params_file = utils.read_arg("params_file", True)
params = None
try:
    with open(params_file, "r", encoding="utf-8") as f:
        params = json.load(f)
except Exception as e:
    print(e)


def get_ui():
    if params is None:
        return {}
    stack = inspect.stack()
    stack_files = list(reversed([s.filename.replace("\\", "/") for s in stack]))
    match_ui_file = None
    for f in stack_files:
        for v in params["uiData"]["uiRecord"]:
            if v == f:
                match_ui_file = v
                break
        if match_ui_file is not None:
            break

    if match_ui_file is None:
        raise Exception("uiData not found for file")

    by = params["uiData"]["by"]

    for i in range(10):
        try:
            if by == "file":
                json_file = params["uiData"][match_ui_file]
                with open(json_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                assert by == "workflow"
                workflow_file = params["uiData"]["workflowFile"]
                node_id = params["uiData"]["nodeId"]
                with open(workflow_file, "r", encoding="utf-8") as f:
                    cells = json.load(f)["graph"]["cells"]
                    node = [cell for cell in cells if cell["id"] == node_id][0]
                    return json.loads(node["data"]["ui"])
        except Exception as e:
            if i == 9:
                raise e
