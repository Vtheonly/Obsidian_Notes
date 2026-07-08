# Read me first

This folder is for Obsidian configuration. When you open the vault folder in Obsidian, it will create additional files here automatically.

## Recommended Settings

After opening the vault, configure these settings for the best experience with this vault:

### Editor
- **Default view for new tabs:** Editing view
- **Strict line breaks:** Off (let paragraphs flow)
- **Show line number:** On

### Files & Links
- **New link format:** Shortest path when possible (so `[[01.01 What is a Network]]` works regardless of which folder the file is in)
- **Default location for new attachments:** In subfolder under current folder (`Attachments`)
- **Use [[Wikilinks]]:** On

### Appearance
- **Base color scheme:** Dark (recommended)
- **Font:** Inter or system default

### Core Plugins (enable)
- **Files & Links** — for managing attachments
- **Search** — full-text search across the vault
- **Graph view** — visualize vault connections
- **Backlinks** — see what links to the current note
- **Outgoing links** — see what the current note links to
- **Tags view** — see all tags and their counts
- **Outline** — table of contents from headings
- **Page preview** — hover to preview linked notes
- **Templates** — for the templates in `/Templates`
- **Command palette** — quickly run any command

### Community Plugins (recommended)
- **Dataview** — for dynamic tables (this vault uses some frontmatter-based queries)
- **Excalidraw** — for hand-drawn diagrams
- **Mind Map** — for visualizing hierarchies
- **Templater** — for advanced templating
- **Advanced Tables** — for managing tables
- **Mermaid Tools** — better Mermaid diagram support

## Configure Templates Plugin

1. Settings → Templates
2. **Template folder location:** `Templates`
3. **Trigger on file creation:** Off (manually insert with `Ctrl+T`)

## Configure Dataview Plugin (if installed)

Enable JavaScript and inline queries in Dataview settings, then you can use queries like:

```dataview
TABLE chapter, section, type
FROM "01 - Network Fundamentals"
WHERE type = "topic-note"
SORT section ASC
```

## Theme Recommendation

The vault looks best with the **Default** or **Minimal** theme. Both render Mermaid diagrams and LaTeX math correctly.

## Mermaid and Math

Both Mermaid diagrams (in code blocks marked `mermaid`) and LaTeX math (between `$$`) should render natively in Obsidian without additional plugins. If they don't, check Settings → Editor → **Use legacy editor** (should be OFF).
