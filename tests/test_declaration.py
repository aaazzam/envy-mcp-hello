import asyncio
import unittest
from pathlib import Path

from envy import GitSource
from envy_mcp_hello import app, hello, mcp


class DeclarationTests(unittest.TestCase):
    def test_hello_environment_and_mcp_server_are_declared(self):
        self.assertEqual(app.environments, ("hello",))
        self.assertEqual(hello.workdir, "/tmp/hello")
        self.assertIsInstance(hello.source, GitSource)
        assert isinstance(hello.source, GitSource)
        self.assertEqual(
            hello.source.url,
            "https://github.com/aaazzam/envy-mcp-hello.git",
        )
        self.assertEqual(hello.source.ref, "main")
        self.assertEqual(hello.source.workdir, "/tmp/hello")

        async def names():
            return {tool.name for tool in await mcp.list_tools()}

        self.assertTrue(
            {
                "create_sandbox",
                "kill_sandbox",
                "publish_pull_request",
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
