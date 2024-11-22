import os


def load_properties(file_path):
    properties = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                properties[key.strip()] = value.strip()
    return properties


def replace_in_file(file_path, replacements, output_path=None):
    with open(file_path, "r") as file:
        if ".git" in file.name:
            return

        content = file.read()

    for key, value in replacements.items():
        content = content.replace(key, value)

    target_path = output_path or file_path
    with open(target_path, "w") as file:
        file.write(content)


def replace_in_directory(source_props, replacement_props, target_dir, output_dir=None):
    source_values = load_properties(source_props)
    replacement_values = load_properties(replacement_props)

    replacements = {v: replacement_values.get(k, v) for k, v in source_values.items()}

    for root, _, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)

            output_path = None
            if output_dir:
                relative_path = os.path.relpath(file_path, target_dir)
                output_path = os.path.join(output_dir, relative_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

            replace_in_file(file_path, replacements, output_path=output_path)


if __name__ == "__main__":
    source = "colors/catppuccin.properties"
    replacement = "colors/catppuccin_bw.properties"
    target_dir = "sources"
    output_dir = "output"

    replace_in_directory(source, replacement, target_dir, output_dir)
