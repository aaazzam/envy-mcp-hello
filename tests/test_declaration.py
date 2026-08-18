import asyncio
import unittest
from pathlib import Path

import devboxes
from envy import GitSource


class DeclarationTests(unittest.TestCase):
    def test_hello_environment_and_mcp_server_are_declared(self):
        self.assertEqual(devboxes.app.environments, ("hello",))
        self.assertEqual(devboxes.hello.workdir, "/tmp/hello")
        self.assertIsInstance(devboxes.hello.source, GitSource)
        assert isinstance(devboxes.hello.source, GitSource)
        self.assertEqual(
            devboxes.hello.source.url,
            "https://github.com/aaazzam/envy-mcp-hello.git",
        )
        self.assertEqual(devboxes.hello.source.ref, "main")
        self.assertEqual(devboxes.hello.source.workdir, "/tmp/hello")

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

    def test_deploy_workflow_rebakes_environment_images(self):
        workflow = (
            Path(__file__).parents[1] / ".github/workflows/deploy.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("Rebake environment images", workflow)
        self.assertIn("runner.rebake()", workflow)


if __name__ == "__main__":
    unittest.main()
