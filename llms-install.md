# Installing Jean (for AI agents)

Jean is a **remote** MCP server. There is nothing to download, build or run, and no API key.

1. Add a remote MCP server named `jean` with the URL `https://jeanpm.vercel.app/mcp`
   (transport: Streamable HTTP; authentication: none).
2. For clients configured by JSON, the entry is:

   ```json
   { "mcpServers": { "jean": { "url": "https://jeanpm.vercel.app/mcp" } } }
   ```

3. Verify: call `find_restriction_sites` with
   `{"_subject": {"sequence": "GGATCCAAAA"}, "enzymes": ["BamHI"]}`. It returns BamHI cutting
   the sequence; any error means the server was not added.

Tools take the molecule to act on as `_subject`: exactly one of `sequence`, `accession` (+ `source`),
`sample` (an id from `list_samples`) or `file` (`{name, text}` or `{name, base64}`). The server is
stateless, so pass it with every call. The calling contract, results and errors:
[docs/protocol.md](docs/protocol.md). Every tool's arguments and outputs: [docs/tools/](docs/tools/README.md).
