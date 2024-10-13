"""Example for configuration.

Cd to the folder containing this file and run this example with the following command:
python . -c ./config.toml
"""

from pathlib import Path

from config import MyExampleConfig, MyExampleConfigSection


def main1() -> None:
    """example how to use the module application_settings"""
    # You can access parameters via get()
    # If you get() MyExampleConfig before load(), it will be loaded automatically
    # using the filepath that has been set via the command line
    a_variable = MyExampleConfig.get().section1.field1
    print(f"{a_variable =}")  # a_variable = -0.5
    # You can also directly get() a section; but remember that the config should
    # be loaded already then (get() on a section does not automatically load())
    another_variable = MyExampleConfigSection.get().field2
    print(f"{another_variable =}")  # another_variable = 22


def main2() -> None:
    """continued example how to use the module application_settings"""
    # The only way to modify a config parameter is by editing the config file
    # or by changing the default value in the definition
    # Suppose that we edited the config file, changed the value for name to "new name"
    # and removed field2

    # You can reload a config
    MyExampleConfig.load()
    new_variable = MyExampleConfig.get().name
    print(f"new_variable = '{new_variable}'")  # new_variable == 'new name'
    another_new_variable = MyExampleConfigSection.get().field2
    print(f"{another_new_variable =}")  # another_new_variable = 2


if __name__ == "__main__":
    main1()

    # Edit the config file
    local_filepath = (
        Path(__file__).parent.absolute() / MyExampleConfig.default_filename()
    )
    with local_filepath.open("r") as file:
        filedata = file.read()
    filedata = filedata.replace('"the real thing"', '"new name"')
    filedata = filedata.replace("field2 = 22", "# field2 = 22")
    with local_filepath.open("w") as file:
        file.write(filedata)

    main2()

    # Restore the original config file
    with local_filepath.open("r") as file:
        filedata = file.read()
    filedata = filedata.replace('"new name"', '"the real thing"')
    filedata = filedata.replace("# field2 = 22", "field2 = 22")
    with local_filepath.open("w") as file:
        file.write(filedata)
