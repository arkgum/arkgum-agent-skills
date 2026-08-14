# NotebookLM routing

## Preferred MCP path

Use the configured NotebookLM MCP tools directly. Tool names may be namespaced by the runtime; match them by capability rather than guessing a new name.

| Stage | Capability | Required behavior |
|---|---|---|
| Create | `notebook_create` | Create one task-specific notebook and retain the full UUID. |
| Add supplied URL | `notebook_add_url` | Add websites or public YouTube URLs without user copy/paste. |
| Add supplied text | `notebook_add_text` | Add briefs, transcripts, notes, or product facts with a clear title. |
| Inspect | `notebook_get` | Verify sources and readiness before querying. |
| Research | `research_start` | Use `source=web`, normally `mode=deep`; pass the existing notebook UUID. |
| Poll | `research_status` | Poll in bounded calls; request `compact=false` before source selection. |
| Import | `research_import` | Import only selected completed research results. |
| Synthesize | `notebook_query` | Query existing imported sources; pass source IDs when practical. |

Use `notebook_query` for the report, opportunity matrix, page brief, and builder prompt. Do not use it to find new sources.

## Confirmation boundary

`report_create` and other Studio-generation tools can require explicit confirmation. The standard workflow does not need a Studio report: the Deep Research result plus source-grounded notebook queries are sufficient and avoid an unnecessary confirmation boundary.

If the user explicitly requests a persistent NotebookLM Studio report, presentation, audio, infographic, quiz, or other Studio artifact, obtain the required confirmation in the current conversation and follow the relevant tool contract.

## Existing notebook

When the user supplies a notebook:

1. Resolve the full notebook UUID.
2. Inspect sources before adding anything.
3. Do not delete, rename, or deactivate existing sources.
4. Add new research only when it is relevant to the stated run.
5. Record which sources pre-existed and which were added by this run.

## CLI fallback

When NotebookLM MCP is unavailable, read and apply the installed `notebooklm-api` skill. Use only its full-path CLI:

```bash
~/notebooklm-skill-venv/bin/notebooklm
```

Required fallback sequence:

```bash
~/notebooklm-skill-venv/bin/notebooklm auth check
~/notebooklm-skill-venv/bin/notebooklm create "R2P — <topic> — <date>"
~/notebooklm-skill-venv/bin/notebooklm use <full-notebook-id>
~/notebooklm-skill-venv/bin/notebooklm source add-research "<research-query>" --mode deep
~/notebooklm-skill-venv/bin/notebooklm source list
~/notebooklm-skill-venv/bin/notebooklm ask "<prompt>"
```

Set the output language to Russian unless the user requests another language. If authentication is missing, use the documented login flow and wait for the user to complete Google sign-in. Never expose or copy the stored browser state.

If both MCP and CLI are unavailable, stop. Do not silently substitute an ungrounded web summary for NotebookLM.
