import hou
import os
from ciohoudini import driver, frames

render_rop_options = {}

def list_current_render_rop_paths(node):
    """
    Collects all the render ROP paths from the provided node.

    Args:
        node (hou.Node): The Houdini node from which to retrieve the ROP paths.

    Returns:
        list: A list of strings representing the render ROP paths.
    """
    render_rops_list = []
    for i in range(1, node.parm("render_rops").eval() + 1):
        path = node.parm("rop_path_{}".format(i)).evalAsString()
        if path:
            render_rops_list.append(path)
    return render_rops_list

def populate_render_rop_menu(node):
    """
    Populates a list of render ROPs in the current stage and sets the default ROPs for the node.

    Args:
        node (hou.Node): The Houdini node for which the render ROP menu is being populated.

    Returns:
        list: A list of strings representing the paths of the ROPs found in the stage.
    """
    stage_render_ropes = []
    render_ropes_list = []
    try:
        # Add the driver ROP if it exists
        driver_rop = driver.get_driver_node(node)
        if driver_rop:
            key = driver_rop.path()
            stage_render_ropes.extend([key, key])
            render_ropes_list.append(key)

        # Add all render ROPs in the stage
        stage_node_list = hou.node('/stage').allSubChildren()

        if stage_node_list:
            for rop in stage_node_list:
                if rop and rop.type().name() == 'usdrender_rop' and not rop.isBypassed():
                    key = rop.path()
                    stage_render_ropes.extend([key, key])
                    render_ropes_list.append(key)

        # Set the first render rop in the list as the node's render_rop_list parameter
        key = node.parm("render_rop_list").eval()
        if key and render_ropes_list and "Connection" in key or "connection" in key:
            key = render_ropes_list[0]
            node.parm("render_rop_list").set(key)

        # Set default render ROPs for the node
        set_default_render_rops(node, render_ropes_list)
    except Exception as e:
        print(f"Error populating render rop menu: {e}")

    return stage_render_ropes

def get_default_output_folder():
    """
    Retrieves the default output folder path for the current Houdini session.

    Returns:
        str: The default output folder path.
    """
    output_folder = ""
    try:
        output_folder = driver.calculate_output_path(hou.pwd()).replace("\\", "/")
        if not output_folder:
            hip_path = os.path.expandvars("$HIP")
            output_folder = f'{hip_path}/render'
    except Exception as e:
        print(f"Error getting default output folder: {e}")

    return output_folder

def get_default_render_script():
    """
    Retrieves the default render script path based on environment variables.

    Returns:
        str: The default render script path.
    """
    render_script = ""
    try:
        ciodir = os.environ.get("CIODIR")
        render_script = f"{ciodir}/ciohoudini/scripts/chrender.py"
    except Exception as e:
        print(f"Error getting default render script: {e}")

    return render_script

def get_default_task_template():
    """
    Retrieves the default task template for rendering.

    Returns:
        str: The default task template for render jobs.
    """
    return "{hserver}hython {render_script} -f {first} {last} {step} -d {render_rop} {render_scene}"

def set_default_render_rops(node, render_ropes_list):
    """
    Sets the default ROP options (output folder, render script, task template) for a given node.

    Args:
        node (hou.Node): The Houdini node to set default ROP options for.
        render_ropes_list (list): A list of ROP paths associated with the node.
    """
    try:
        output_folder = get_default_output_folder()
        render_script = get_default_render_script()
        task_template = get_default_task_template()

        node_name = node.name()

        if node_name not in render_rop_options:
            render_rop_options[node_name] = {}

        for key in render_ropes_list:
            if key not in render_rop_options[node_name]:
                render_rop_options[node_name][key] = {
                    "output_folder": output_folder,
                    "render_script": render_script,
                    "task_template": task_template,
                }
                node.parm("render_script").set(render_script)
                node.parm("task_template").set(task_template)
    except Exception as e:
        print(f"Error setting default render rops: {e}")

def reset_render_rop_options(node):
    """
    Resets the render ROP options for the given node, clearing only the values associated
    with the provided node's name in the render_rop_options dictionary.

    Args:
        node (hou.Node): The Houdini node whose render ROP options are to be reset.
    """
    try:
        node_name = node.name()
        if node_name in render_rop_options:
            render_rop_options[node_name] = {}
            print(f"Render ROP options for node '{node_name}' have been reset.")
        # else:
        #    print(f"No render ROP options found for node '{node_name}'.")
    except Exception as e:
        print(f"Error resetting render rop options for node '{node.name()}': {e}")


def update_render_rop_options(node, **kwargs):
    """
    Updates the render ROP options for a given node based on the current parameter values.
    Ensures that all Houdini parameters are evaluated to their resolved values (e.g., $HIP).

    Args:
        node (hou.Node): The Houdini node whose render ROP options are to be updated.
        **kwargs: Additional keyword arguments for flexibility in the future.
    """
    try:
        node_name = node.name()
        key = node.parm("render_rop_list").eval()
        # print(f"Updating render rop options for node '{node_name}' and key '{key}'")

        # Check if the key exists before updating
        if key not in render_rop_options.get(node_name, {}):
            # print(f"ROP path '{key}' not initialized for node '{node_name}'. Initializing defaults.")
            # Reinitialize if the key is missing
            set_default_render_rops(node, [key])


        # Now proceed with the update
        output_folder = node.parm("output_folder").evalAsString()
        render_script = node.parm("render_script").evalAsString()
        task_template = node.parm("task_template").evalAsString()

        # print(f"output_folder: {output_folder}")
        # print(f"render_script: {render_script}")
        # print(f"task_template: {task_template}")

        render_rop_options[node_name][key]["output_folder"] = output_folder
        render_rop_options[node_name][key]["render_script"] = render_script
        render_rop_options[node_name][key]["task_template"] = task_template

        # print(f"render_rop_options: {render_rop_options[node_name][key]}")
    except Exception as e:
        print(f"Error updating render rop options: {e}")

def get_render_rop_options(node, **kwargs):
    """
    Retrieves the render ROP options for a given node and applies them to the node's parameters.
    Ensures that all Houdini parameters are evaluated to their resolved values (e.g., $HIP).

    Args:
        node (hou.Node): The Houdini node whose render ROP options are to be retrieved.
        **kwargs: Additional keyword arguments for flexibility in the future.
    """
    try:
        node_name = node.name()
        key = node.parm("render_rop_list").evalAsString()

        if key not in render_rop_options.get(node_name, {}):
            output_folder = get_default_output_folder()
            render_script = get_default_render_script()
            task_template = get_default_task_template()

            render_rop_options.setdefault(node_name, {})[key] = {
                "output_folder": output_folder,
                "render_script": render_script,
                "task_template": task_template,
            }

        options = render_rop_options[node_name][key]

        node.parm("output_folder").set(options["output_folder"])
        node.parm("render_script").set(options["render_script"])
        node.parm("task_template").set(options["task_template"])

    except Exception as e:
        print(f"Error getting render rop options: {e}")

def query_output_folder(node, key):
    """
    Queries the output folder path for a given node and ROP path.
    Ensures that all Houdini parameters are evaluated to their resolved values (e.g., $HIP).

    Args:
        node (hou.Node): The Houdini node to query.
        key (str): The specific ROP path key to look up.

    Returns:
        str: The output folder path if available, otherwise an empty string.
    """
    output_folder = ""
    try:
        node_name = node.name()
        if key in render_rop_options.get(node_name, {}):
            output_folder = render_rop_options[node_name][key]["output_folder"]
        #else:
        #    print(f"render rop {key} is unavailable for node {node_name}")
    except Exception as e:
        print(f"Error querying output folder: {e}")

    return output_folder

def query_render_script(node, key):
    """
    Queries the render script path for a given node and ROP path.
    Ensures that all Houdini parameters are evaluated to their resolved values (e.g., $HIP).

    Args:
        node (hou.Node): The Houdini node to query.
        key (str): The specific ROP path key to look up.

    Returns:
        str: The render script path if available, otherwise the default render script.
    """
    render_script = ""
    try:
        node_name = node.name()
        if key in render_rop_options.get(node_name, {}):
            render_script = render_rop_options[node_name][key]["render_script"]
            if not render_script:
                render_script = get_default_render_script()
                # print(f"Render script not available. Defaulting to {render_script}")
        else:
            render_script = get_default_render_script()
            # print(f"Render rop {key} is unavailable for node {node_name}. Defaulting to {render_script}")
    except Exception as e:
        print(f"Error querying render script: {e}")

    return render_script

def query_task_template(node, key):
    """
    Queries the task template for a given node and ROP path.
    Ensures that all Houdini parameters are evaluated to their resolved values (e.g., $HIP).

    Args:
        node (hou.Node): The Houdini node to query.
        key (str): The specific ROP path key to look up.

    Returns:
        str: The task template if available, otherwise the default task template.
    """
    task_template = ""
    try:
        node_name = node.name()
        if key in render_rop_options.get(node_name, {}):
            task_template = render_rop_options[node_name][key]["task_template"]
            if not task_template:
                task_template = get_default_task_template()
                # print(f"Task template not available. Defaulting to {task_template}")
        else:
            task_template = get_default_task_template()
            # print(f"Render rop {key} is unavailable for node {node_name}. Defaulting to {task_template}")
    except Exception as e:
        print(f"Error querying task template: {e}")

    return task_template
