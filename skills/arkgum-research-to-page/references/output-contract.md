# Output contract

## Run directory

Keep one isolated directory per invocation. Never mix artifacts from different topics or NotebookLM notebooks.

Required files:

| File | Contents |
|---|---|
| `manifest.json` | Machine-readable run identity, notebook metadata, research tasks, selection, status, and artifact paths. |
| `00-input.md` | User request, supplied sources, inferred inputs, explicit assumptions, and unresolved placeholders. |
| `10-research-plan.md` | Research question, scope, recency/region rules, notebook ID/URL, source-quality plan. |
| `20-source-manifest.md` | Imported sources, provenance, role, dates, limitations, and import status. |
| `30-grounded-report.md` | Full NotebookLM source-grounded report with citations. |
| `40-opportunity-matrix.md` | Ranked opportunities, evidence, gaps, risks, and selected winner. |
| `50-page-brief.md` | Evidence-led content, UX, SEO, and conversion brief. |
| `60-builder-prompt.md` | Final self-contained prompt for AI Studio or the selected builder. |
| `70-qa.md` | Traceability and build-readiness audit with PASS/FAIL outcomes. |

## Manifest fields

Preserve at minimum:

```json
{
  "version": 1,
  "skill": "arkgum-research-to-page",
  "created_at": "ISO-8601 timestamp",
  "status": "initialized|researching|grounded|briefed|complete|blocked",
  "topic": "string",
  "audience": "string",
  "page_goal": "string",
  "offer": "string",
  "cta": "string",
  "builder": "string",
  "language": "ru",
  "notebook_id": "full UUID",
  "notebook_url": "URL",
  "research_task_ids": [],
  "selected_opportunity": "string",
  "unresolved_placeholders": [],
  "artifacts": {}
}
```

## Citation contract

- Preserve NotebookLM citation markers and source identifiers where returned.
- Add source URLs to `20-source-manifest.md` when available.
- Trace consequential page claims back to the report and source manifest.
- Label inference as inference.
- Use `unknown` or `нет данных` rather than filling evidence gaps.

## QA gates

All gates must be present in `70-qa.md`:

1. Notebook ID and URL recorded.
2. Imported sources are ready or failures documented.
3. Core claims have primary or independent support.
4. Time-sensitive claims use current sources.
5. Conflicts and limitations remain visible.
6. Opportunity scores explain their evidence.
7. No fabricated search metrics or ranking guarantee.
8. Audience, opportunity, offer, goal, and CTA align.
9. Copy does not invent product facts, testimonials, or results.
10. Builder prompt contains information architecture and actual draft copy.
11. Mobile/responsive behavior is explicit.
12. Accessibility, performance, technical SEO, analytics, and acceptance criteria are explicit.
13. Missing business data remain visible placeholders.
14. Final prompt is self-contained and does not ask the builder to research again.

Set manifest status to `complete` only after all blocking gates pass. Otherwise use `blocked` and record why.
