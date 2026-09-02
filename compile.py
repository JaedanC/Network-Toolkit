import sys
import os
import json
import textwrap


def create_file_if_not_exist(path, contents=""):
    if os.path.exists(path):
        return

    with open(path, "a", encoding="utf-8") as f:
        f.write(contents)


def main():
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


    base_absolute = os.path.dirname(os.path.realpath(__file__))
    binary_dir = os.path.join(base_absolute, "bin")

    bin_details = [{
        "exe": "mping.exe",
        "dir": "MultiPing",
        "bat": "mping.bat",
        "py":  "mping.py",
        "wd":  ".",
    },
    {
        "exe": "lping.exe",
        "dir": "LoudPing",
        "bat": "lping.bat",
        "py":  "lping.py",
        "wd":  ".",
    },
    {
        "exe": "app.exe",
        "dir": "Meraki-App",
        "bat": "mapp.bat",
        "py":  "app.py",
        "wd":  ".",
    },
    {
        "exe": "app.exe",
        "dir": "Ping-App",
        "bat": "pping.bat",
        "py":  "app.py",
        "wd":  "app",
    },
    {
        "exe": "app.exe",
        "dir": "Catalyst-Switch-App",
        "bat": "capp.bat",
        "py":  "app.py",
        "wd":  ".",
    }]

    if "-exe" in sys.argv:
        bat_src = \
        textwrap.dedent("""
        @echo off

        setlocal
        cd "{working_dir}"
        {exe_name} %*
        endlocal
        """).strip()

        for bin_detail in bin_details:
            creating_file = os.path.join(binary_dir, bin_detail["bat"])
            working_dir = bin_detail["wd"]
            print("Creating", creating_file)
            with open(creating_file, "w", encoding="utf-8") as f:
                f.write(bat_src.format(
                    working_dir=os.path.join(base_absolute, "tools", bin_detail["dir"], "dist", working_dir),
                    exe_name=bin_detail["exe"]
                ))
    else:
        bat_src = \
        textwrap.dedent("""
        @echo off

        setlocal
        cd "{working_dir}"
        powershell -Command "./venv/scripts/activate;"^
         "python {starting_file} %*"
        @REM exit
        endlocal
        """).strip()

        for bin_detail in bin_details:
            creating_file = os.path.join(binary_dir, bin_detail["bat"])
            print("Creating", creating_file)
            with open(creating_file, "w", encoding="utf-8") as f:
                f.write(bat_src.format(
                    working_dir=os.path.join(base_absolute, "tools", bin_detail["dir"]),
                    starting_file=bin_detail["py"]
                ))


if __name__ == "__main__":
    main()
