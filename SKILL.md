# FounderOS V4

## Chapter 1 - Vision
FounderOS is a venture operating system built around engines, durable memory and environment abstraction.

## Principles
- Engine-first architecture
- Git-native persistence
- Capability abstraction (Git, GitHub, MCP, SSH, Filesystem)
- OODA before execution
- Knowledge graph over flat memory
- Durable decisions
- Modular extensions

## Kernel
- Memory Engine
- Knowledge Graph Engine
- OODA Engine
- Decision Engine
- Venture Engine
- Planning Engine
- Task Engine
- Research Engine
- Collaboration Engine
- Execution Engine

## Chapter 2 - Runtime & Capability Layer
FounderOS never assumes a fixed execution environment. At startup it detects available capabilities and dynamically adapts its behavior.

### Runtime Detection
- Chat-only
- Local filesystem
- Git repository
- GitHub connector
- MCP servers
- SSH shell
- Docker/container runtime

### Capability Model
Capabilities are advertised rather than assumed. Engines request capabilities through an abstraction layer instead of directly invoking tools.

### Drivers
Drivers provide a uniform interface for Git, GitHub, MCP, SSH, Filesystem and future integrations.

### Degraded Modes
If a capability is unavailable, the Kernel selects the highest compatible execution strategy while preserving correctness and auditability.

Next chapter: Memory Engine.
