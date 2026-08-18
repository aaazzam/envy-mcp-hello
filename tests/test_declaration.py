import asyncio
import unittest

import devboxes


class DeclarationTests(unittest.TestCase):
    def test_hello_environment_and_mcp_server_are_declared(self):
        self.assertEqual(devboxes.app.environments, ("hello",))
        self.assertEqual(devboxes.hello.workdir, "/tmp/hello")
        setup_commands = tuple(
            command
            for step in devboxes.hello.setup_steps
            for command in step.commands
        )
        self.assertIn("README.md", setup_commands[0])
        self.assertIn("hello.py", setup_commands[1])

        async def names():
            return {tool.name for tool in await devboxes.mcp.list_tools()}

        self.assertTrue(
            {
                "create_sandbox",
                "kill_sandbox",
                "bash",
                "read",
                "write",
                "edit",
                "glob",
                "grep",
            }.issubset(asyncio.run(names()))
        )


if __name__ == "__main__":
    unittest.main()
