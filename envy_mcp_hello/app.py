"""Envy and Modal declarations for the public hello-world server."""

import modal
import envy


APP_NAME = "envy-mcp-hello"
ENVY_SOURCE = "envy[mcp] @ git+https://github.com/aaazzam/envy.git@main"
FASTMCP_VERSION = "fastmcp==4.0.0b3"
GITHUB_SECRET_NAME = "envy-github"

app = envy.Envy(APP_NAME)
hello = app.env(
    "hello",
    base=modal.Image.debian_slim(),
    source=envy.GitSource.github(
        "aaazzam/envy-mcp-hello",
        ref="main",
        workdir="/tmp/hello",
    ),
    env={"ENV": "hello"},
)

# The control plane is deliberately separate from the sandbox image. It only
# runs FastMCP and Envy; the hello sandbox uses its own base image and source.
control_plane_image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .uv_pip_install(ENVY_SOURCE, FASTMCP_VERSION)
    .add_local_python_source("envy_mcp_hello", copy=True)
)
github_secret = modal.Secret.from_name(GITHUB_SECRET_NAME)

mcp = app.mcp(
    instructions=(
        "This is a public hello-world Envy MCP server. "
        "Create a hello sandbox, then use the file and shell tools."
    ),
    git_secret=github_secret,
)
modal_app = modal.App(APP_NAME)


@modal_app.function(image=control_plane_image, secrets=[github_secret])
@modal.asgi_app()
def serve():
    return mcp.http_app(stateless_http=True)
