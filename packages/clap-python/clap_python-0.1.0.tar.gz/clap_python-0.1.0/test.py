# Copyright (C) 2024  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from unittest import TestCase, mock

from clap_py import App, Arg, ClapPyException, MutuallyExclusiveGroup, SubCommand

complex_app = (
    App()
    .arg(
        MutuallyExclusiveGroup()
        .arg(
            SubCommand("--env", "-e")
            .arg(
                Arg("env-name")
                .choices(["maya", "nuke", "houdini"])
                .help("Recipe name.")
            )
            .arg(
                MutuallyExclusiveGroup()
                .arg(Arg("--add").help("Add packages to env").multiple_values(True))
                .arg(Arg("--rm").help("Remove packages from env").multiple_values(True))
                .arg(Arg("--del").help("delete env"))
                .arg(Arg("--list").takes_value(False).help("List packages in env"))
                .arg(
                    SubCommand("--run").arg(
                        Arg("--command", "-c")
                        .default("bash")
                        .help("Command to execute when running env")
                    )
                )
                .arg(Arg("--editor").takes_value(False).help("open code editor"))
            )
        )
        .arg(Arg("--list", "-l").help("List available envs ").takes_value(False))
        .arg(
            Arg("--generate", "-g")
            .help("Interactive tool to setup new dev env.")
            .takes_value(False)
        )
        .arg(Arg("--new").help("Create new env."))
    )
    .arg(Arg("--verbose", "-v"))
)


simple_parser = App().arg(Arg("--hello")).arg(Arg("--items").multiple_values(True))


class TestApp(TestCase):
    def test_parser_101(self):
        expected_result = {"hello": "Joy", "items": ["a", "b"]}

        self.assertEqual(
            expected_result,
            simple_parser.parse_args(["--items", "a", "b", "--hello", "Joy"]),
        )

    def test_parser_102(self):
        with self.assertRaises(ClapPyException) as contex:
            simple_parser.private.parse(["--hello", "a", "b"], [], False)
            self.assertEquals(contex.exception.msg, "unrecognized arguments: b")

    def test_validate_multiple_values(self):
        def validate(value) -> str:
            try:
                int(value)
                return ""
            except ValueError:
                return f"Not able to convert '{value}' to int"

        app = App().arg(Arg("--add").multiple_values(True).validate(validate))

        expected_result = {"add": ["1", "100"]}

        self.assertEqual(expected_result, app.parse_args(["--add", "1", "100"]))

        with self.assertRaises(ClapPyException) as context:
            app.private.parse(["--add", "1", "0.1"], [], False)
            self.assertEqual(context.exception.msg, "Not able to convert '0.8' to int")

    def test_positional_args101(self):
        app = App().arg(Arg("data")).arg(Arg("value")).arg(Arg("--test"))

        expected_result = {"data": "a", "value": "bbbbbbbbb", "test": "yes"}
        self.assertEqual(
            expected_result, app.parse_args(["a", "bbbbbbbbb", "--test", "yes"])
        )

    def test_positional_args102(self):
        app = (
            App()
            .arg(Arg("files").multiple_values(True))
            .arg(Arg("--test").required(True))
        )
        expected_result = {
            "files": ["/path/to/file1.txt", "/path/to/file2.exr"],
            "test": "yes",
        }
        self.assertEqual(
            expected_result,
            app.parse_args(
                ["/path/to/file1.txt", "/path/to/file2.exr", "--test", "yes"]
            ),
        )

    def test_unknown_args(self):
        expected_result = {
            "list": False,
            "generate": False,
            "env": {
                "list": False,
                "editor": False,
                "env_name": "maya",
                "run": {"command": "mayapy", "unknown": ["/file/path"]},
            },
        }
        self.assertEqual(
            expected_result,
            complex_app.parse_known_args(
                ["--env", "maya", "--run", "-c", "mayapy", "--", "/file/path"]
            ),
        )

    def test_parse_args_with_unknown_not_enabled(self):
        with self.assertRaises(ClapPyException) as context:
            complex_app.private.parse(
                ["-e", "maya", "--run", "-c", "mayapy", "--", "/file/path"], [], False
            )
        self.assertEqual(context.exception.msg, "unrecognized arguments: --")

    @mock.patch("clap_py.sys.stdout.write")
    def test_missing_argument(self, std_out_write):
        with self.assertRaises(SystemExit):
            complex_app.parse_args(["--env", "maya", "-h"])

    def test_multiple_values(self):
        expected_result = {
            "list": False,
            "generate": False,
            "env": {
                "list": False,
                "editor": False,
                "env_name": "maya",
                "rm": ["package-a", "package-b"],
            },
        }
        self.assertEqual(
            expected_result,
            complex_app.parse_args(["-e", "maya", "--rm", "package-a", "package-b"]),
        )

    def test_required_args(self):
        app = App().arg(Arg("--test")).arg(Arg("--abc").required(True))
        with self.assertRaises(ClapPyException) as context:
            app.private.parse(["--test", "hello"], [], False)
        self.assertEqual(
            context.exception.msg, "the following arguments are required: --abc"
        )

    def test_mutually_exclusive_group101(self):
        with self.assertRaises(ClapPyException) as context:
            visited = []
            (complex_app.private.parse(["-g", "--list"], visited, False),)
        self.assertEqual(
            context.exception.msg,
            "argument --list not allowed with argument --generate",
        )

    def test_value_parser_int(self):
        app = App().arg(Arg("--number").value_parser(int))
        expected_result = {"number": 101}
        self.assertEqual(expected_result, app.parse_args(["--number", "101"]))

        app = App().arg(Arg("--number").value_parser(float))
        expected_result = {"number": 101.0}
        self.assertEqual(expected_result, app.parse_args(["--number", "101"]))

    def test_value_parser_datetime(self):
        def to_datetime(value: str) -> datetime:
            return datetime.strptime(value, "%Y-%m-%d:%H:%M:%S")

        app = App().arg(Arg("--date-time").value_parser(to_datetime))
        expected_result = {"date_time": datetime(2024, 1, 1, 19, 0, 1)}
        self.assertEqual(
            expected_result, app.parse_args(["--date-time", "2024-01-01:19:00:01"])
        )
