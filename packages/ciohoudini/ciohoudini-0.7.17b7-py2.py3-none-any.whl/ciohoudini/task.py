import re
import os
from ciohoudini import frames, context, advanced_render_rops


def create_task_template(node, **kwargs):
    """Get the task template from the node and format it based on input_template."""

    rop_path = kwargs.get("rop_path", None)
    input_template = advanced_render_rops.query_task_template(node, rop_path)

    first = kwargs.get("first", 1)
    last = kwargs.get("last", 1)
    step = kwargs.get("step", 1)
    render_script = advanced_render_rops.query_render_script(node, rop_path)
    render_scene = node.parm("render_scene").eval()
    host_version = node.parm("host_version").eval()

    # Expand variables for rop_path and render_scene
    try:
        rop_path = os.path.expandvars(rop_path) if rop_path else None
    except Exception as e:
        print("Error expanding rop path {}: {}".format(rop_path, e))

    try:
        render_scene = os.path.expandvars(render_scene)
    except Exception as e:
        print("Error expanding render scene {}: {}".format(render_scene, e))

    # Prepare data for formatting the input template
    data = {
        "hserver": "",
        "hython": "hython",
        "render_script": re.sub("^[a-zA-Z]:", "", render_script).replace("\\", "/"),
        "first": first,
        "last": last,
        "step": step,
        "render_rop": rop_path,
        "render_scene": render_scene
    }

    # Determine the host version and set hserver if needed
    try:
        host_version = int(host_version.split()[1].split(".")[0])
    except:
        host_version = 19

    if host_version < 19:
        data["hserver"] = "/opt/sidefx/houdini/19/houdini-19.0.561/bin/hserver --logfile /tmp/hserver.log -C -D; "

    # Format the input template with the actual values
    try:
        task_command = input_template.format(**data)
    except Exception as e:
        print(f"Missing key in data for template: {e}")

    return task_command


def default_task_template(node, **kwargs):
    """Get the task template from the node."""
    first = kwargs.get("first", 1)
    last = kwargs.get("last", 1)
    step = kwargs.get("step", 1)
    rop_path = kwargs.get("rop_path", None)

    render_script = advanced_render_rops.query_render_script(node, rop_path)
    # Use the rop path instead of the driver path.
    # driver_path = node.parm("driver_path").eval()
    render_scene = node.parm("render_scene").eval()
    host_version = node.parm("host_version").eval()
    try:
        rop_path = os.path.expandvars(rop_path)
    except Exception as e:
        print("Error expanding rop path {}: {}".format(rop_path, e))

    try:
        render_scene = os.path.expandvars(render_scene)
    except Exception as e:
        print("Error expanding render scene {}: {}".format(render_scene, e))



    data = {
        "script": re.sub("^[a-zA-Z]:", "", render_script).replace("\\", "/"),
        "first": first,
        "last": last,
        "step": step,
        # "driver": driver_path,
        "driver": rop_path, # Use the rop path instead of the driver path.
        "hipfile": render_scene,
        "hserver": ""
    }

    try:
        host_version = int(host_version.split()[1].split(".")[0])
    except:
        host_version = 19

    if host_version < 19:
        data["hserver"] = "/opt/sidefx/houdini/19/houdini-19.0.561/bin/hserver --logfile /tmp/hserver.log -C -D; "

    return "{hserver}hython \"{script}\" -f {first} {last} {step} -d {driver} \"{hipfile}\"".format(**data)

def import_task_template(node, **kwargs):
    task_template = node.parm("task_template").eval()
    task_template = os.path.expandvars(task_template)
    print("Task template: {}".format(task_template))
    return task_template

def resolve_payload(node, **kwargs):
    """
    Resolve the task_data field for the payload.

    If we are in sim mode, we emit one task.
    """
    task_limit = kwargs.get("task_limit", -1)
    frame_range = kwargs.get("frame_range", None)
    if node.parm("is_sim").eval():
        cmd = node.parm("task_template").eval()
        tasks = [{"command": cmd, "frames": "0"}] 
        return {"tasks_data": tasks}
    tasks = []
    resolved_chunk_size = frames.get_resolved_chunk_size(node, frame_range=frame_range)
    sequence = frames.main_frame_sequence(node, frame_range=frame_range, resolved_chunk_size=resolved_chunk_size)
    chunks = sequence.chunks()
    # Get the scout sequence, if any.
    for i, chunk in enumerate(chunks):
        if task_limit > -1 and i >= task_limit:
            break
        # Get the frame range for this chunk.
        #
        kwargs["first"] = chunk.start
        kwargs["last"] = chunk.end
        kwargs["step"] = chunk.step
        # Get the task template.
        cmd = create_task_template(node, **kwargs)
        # Set the context for this chunk.
        context.set_for_task(first=chunk.start, last=chunk.end, step=chunk.step)
        # cmd = node.parm("task_template").eval()

        tasks.append({"command": cmd, "frames": str(chunk)})


    return {"tasks_data": tasks}
