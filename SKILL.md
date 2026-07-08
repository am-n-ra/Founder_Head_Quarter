# FounderOS V4

## Chapter 8 - Task Engine
The Task Engine translates executable plans into coordinated work units.

### Responsibilities
- Create tasks from milestones.
- Track execution state.
- Manage dependencies.
- Assign ownership.
- Synchronize with external systems.
- Measure execution progress.

### Task Lifecycle
Draft → Ready → Active → Blocked → Review → Completed → Archived

### Task Model
Each task contains:
- objective
- owner
- priority
- dependencies
- due dates
- acceptance criteria
- evidence
- execution history

### Synchronization
The Task Engine exposes adapters for:
- GitHub Issues
- Local Markdown backlogs
- MCP task services
- Future project management providers

### Execution Rules
Tasks are generated from Planning outputs and continuously updated from OODA feedback.

Next chapter: Execution Engine.
