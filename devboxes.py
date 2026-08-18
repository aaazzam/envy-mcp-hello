"""The public hello-world MCP server."""

import modal
import envy


APP_NAME = "envy-mcp-hello"
ENVY_SOURCE = "envy[mcp] @ git+https://github.com/aaazzam/envy.git@main"

app = envy.Envy(APP_NAME)
hello = app.env(
    "hello",
    base=modal.Image.debian_slim(),
    env={"ENV": "hello"},
)

# The control plane is deliberately separate from the sandbox image. It only
# runs FastMCP and the declaration above; the hello sandbox uses its own base
# image and Envy transforms.
control_plane_image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .pip_install(ENVY_SOURCE)
    .add_local_python_source("devboxes", copy=True)
)

mcp = app.mcp(
    instructions=(
        "This is a public hello-world Envy MCP server. "
        "Create a hello sandbox, then use the file and shell tools."
    )
)
modal_app = modal.App(APP_NAME)


@modal_app.function(image=control_plane_image)
@modal.asgi_app()
def serve():
    return mcp.http_app(stateless_http=True)
