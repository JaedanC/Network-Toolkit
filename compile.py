import sys
import os
import shutil
import json
import textwrap
import zipfile
from extra.api import APIRequest, Method, safe_open_wb


def create_file_if_not_exist(path, contents=""):
    if os.path.exists(path):
        return

    with open(path, "a", encoding="utf-8") as f:
        f.write(contents)


def main():
    if len(sys.argv) < 2:
        print("Usage: python compile.py [-d] | [pygui_directory]")
        return

    if "-d" in sys.argv:
        # https://docs.github.com/en/rest/releases/releases
        print("Querying Github API for latest pygui release")
        res = APIRequest("https://api.github.com/repos/JaedanC/pygui/releases/latest") \
            .set_method(Method.Get) \
            .execute()

        asset = res.json_dict()["assets"][0]
        filename: str = asset["name"]
        download_url: str = asset["browser_download_url"]

        print(f"Downloading {filename}")
        raw_res = APIRequest(download_url) \
            .set_method(Method.Get) \
            .execute() \
            .raw()

        zip_name = "downloads/" + filename
        folder_name = zip_name.removesuffix(".zip")

        with safe_open_wb(zip_name) as f:
            f.write(raw_res.content)

        print(f"Unzipping to {folder_name}")
        with zipfile.ZipFile(zip_name) as zip_f:
            zip_f.extractall(folder_name)

        pygui_release_dir = folder_name
        print(pygui_release_dir)
    else:
        pygui_release_dir = sys.argv[1]

    pygui_folder = os.path.join(pygui_release_dir, "pygui")
    pygui_demo = os.path.join(pygui_release_dir, "pygui_demo.py")

    catalyst_switch_app_dir = os.path.join("tools", "Catalyst-Switch-App")
    meraki_app_dir          = os.path.join("tools", "Meraki-App")
    ping_app_dir            = os.path.join("tools", "Ping-App")
    loud_ping_dir           = os.path.join("tools", "LoudPing")
    multi_ping_dir          = os.path.join("tools", "MultiPing")

    all_app_dirs = [
        catalyst_switch_app_dir,
        meraki_app_dir,
        ping_app_dir,
        loud_ping_dir,
        multi_ping_dir,
    ]

    pygui_app_dirs = [
        catalyst_switch_app_dir,
        meraki_app_dir,
        ping_app_dir,
    ]

    # Copy pygui
    for pygui_app_dir in pygui_app_dirs:
        shutil.copytree(pygui_folder, os.path.join(pygui_app_dir, "pygui"), dirs_exist_ok=True)
        shutil.copy(pygui_demo, pygui_app_dir)

    # Initialise any other files
    example_switches_json = {
        "sydney-site": [
            "10.0.0.1",
            "10.0.0.2",
            "10.0.0.3",
        ],
        "melbourne-site": [
            "10.0.1.1",
            "10.0.1.2",
            "10.0.1.3",
            "10.0.1.4",
        ],
    }
    create_file_if_not_exist(
        os.path.join(catalyst_switch_app_dir, "switches.py"),
        "switches = " + json.dumps(example_switches_json, indent=4)
    )
    create_file_if_not_exist(os.path.join(catalyst_switch_app_dir, "password.txt"))

    create_file_if_not_exist(os.path.join(meraki_app_dir, "meraki_api_key.txt"))


    requirements_files = [os.path.join(app_dir, "requirements.txt") for app_dir in all_app_dirs]
    dependencies = []
    for requirements_file in requirements_files:
        if not os.path.exists(requirements_file):
            continue

        with open(requirements_file, encoding="utf-8") as f:
            dependencies += f.readlines()

    dependencies = list(map(lambda x: x.strip(), dependencies))
    dependencies = list(set(dependencies))
    dependencies.sort()

    with open("requirements_gen.txt", "w", encoding="utf-8") as f:
        for dependency in dependencies:
            dependency = dependency.strip()
            if dependency == "":
                continue

            f.write(dependency)
            f.write("\n")

    print("Creating binary folder")
    if not os.path.exists("bin"):
        os.mkdir("bin")

    bat_src = \
    textwrap.dedent("""
    @echo off

    setlocal
    cd "{working_dir}"
    {exe_name} %*
    endlocal
    """).strip()

    base_absolute = os.path.dirname(os.path.realpath(__file__))
    binary_dir = os.path.join(base_absolute, "bin")

    bin_details = [{
        "exe": "mping.exe",
        "dir": "MultiPing",
        "bat": "mping.bat",
    },
    {
        "exe": "lping.exe",
        "dir": "LoudPing",
        "bat": "lping.bat",
    },
    {
        "exe": "app.exe",
        "dir": "Meraki-App",
        "bat": "mapp.bat",
    },
    {
        "exe": "app.exe",
        "dir": "Ping-App",
        "bat": "pping.bat",
    },
    {
        "exe": "app.exe",
        "dir": "Catalyst-Switch-App",
        "bat": "capp.bat",
    }]

    for bin_detail in bin_details:
        with open(os.path.join(binary_dir, bin_detail["bat"]), "w", encoding="utf-8") as f:
            f.write(bat_src.format(
                working_dir=os.path.join(base_absolute, "tools", bin_detail["dir"], "dist"),
                exe_name=bin_detail["exe"]
            ))


if __name__ == "__main__":
    main()
