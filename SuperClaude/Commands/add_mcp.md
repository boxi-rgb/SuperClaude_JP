# Command: add_mcp

## Description
Installs one or more MCP (Model Context Protocol) servers from the official registry. This allows adding new capabilities to SuperClaude on-demand.

## Usage
`/sc:add_mcp [server_name_1] [server_name_2] ...`

## Arguments
- `server_name` (required): The name of the MCP server to install. You can provide multiple server names separated by spaces. To see a list of available servers, use the `/sc:list_mcp` command (Note: this command will be created in a future step).

## Examples
- `/sc:add_mcp magic`
- `/sc:add_mcp playwright context7`

## Technical Details
- **Action**: `mcp.add`
- **Executor**: `SuperClaude.cli.McpController.add` (Note: This is a placeholder, the actual executor will be linked in the next step).
- **Requires**: `claude` CLI, `node`, `npm`

## Behavior
- The command will look up the provided server name(s) in the `config/mcp_registry.json` file.
- For each valid server name, it will invoke the `claude mcp add ...` command to install the corresponding npm package.
- It provides real-time feedback on the installation progress and reports success or failure for each requested server.
- If a server is already installed, it will be skipped.
- If an invalid server name is provided, an error message will be shown.
