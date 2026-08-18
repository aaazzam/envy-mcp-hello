# envy-mcp-hello

A tiny public MCP server backed by an Envy-managed Modal sandbox. It exposes
one `hello` environment and the standard Envy MCP tools:

`create_sandbox` · `kill_sandbox` · `bash` · `read` · `write` · `edit` · `glob` · `grep`

## Deploy it

1. Create a Modal token in the `modal-labs` workspace.
2. In this GitHub repository, add these Actions secrets under **Settings →
   Secrets and variables → Actions**:

   - `MODAL_TOKEN_ID`
   - `MODAL_TOKEN_SECRET`

3. Push to `main`, or run **Deploy MCP server** manually from the Actions tab.

The workflow installs Envy from the public [`aaazzam/envy`](https://github.com/aaazzam/envy)
repository, runs the declaration test, and deploys the `modal_app` in
`devboxes.py` to Modal.

After the first deployment, Modal prints the web endpoint in the deploy output.
Your MCP URL is that endpoint with `/mcp` appended:

```text
https://<modal-web-endpoint>/mcp
```

The endpoint is intentionally public for experimentation. Do not put secrets
or private source code in the hello sandbox.

## Try it

Point an MCP client at the URL and call:

1. `create_sandbox` with `environment: "hello"`
2. `write` `/tmp/hello/message.txt` with `hello from MCP`
3. `read`, `edit`, `bash`, `glob`, or `grep` against that file
4. `kill_sandbox` when finished

The sandbox is ephemeral and uses `/tmp/hello` as its working directory.

## Local validation

With Python and the MCP extra installed:

```bash
python -m unittest discover -s tests
```

Live Modal integration is deliberately not part of the GitHub Action. The
Action deploys the public control plane; sandbox creation happens when an MCP
client calls `create_sandbox`.
