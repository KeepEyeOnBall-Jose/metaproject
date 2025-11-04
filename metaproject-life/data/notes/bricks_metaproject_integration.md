Title: Add BRICKS project to metaproject — dual branch structure
Created: 2025-10-01
Tags: bricks, metaproject, integration, branches, autolinker, aam-analyzer

Category: Project-Specific Technical

Project integration task

Need to add the BRICKS project to the metaproject workspace, but it has a unique dual-branch structure that serves two different purposes.

BRICKS project structure

**Two main branches with different purposes:**

1. **Xuerong's branch**: 
   - Purpose: Analyzer for AAM and Hipoges sites
   - Focus: Site analysis and data extraction
   - Owner/maintainer: Xuerong

2. **My branch**:
   - Purpose: Autolinker functionality
   - Focus: Linking and connection logic
   - Owner/maintainer: Jose (me)

Integration considerations

**Workspace setup:**
- Decide whether to include both branches or just one in the linked projects
- Consider separate symlinks for each branch if they're maintained independently
- Update `projects.json` and workspace configuration accordingly

**Branch management:**
- Document which branch serves which purpose in the project manifest
- Ensure clear naming/paths to avoid confusion
- Consider branch-specific documentation or README updates

**Dependencies and conflicts:**
- Check if both branches can coexist in the same workspace
- Verify no conflicting dependencies between the two branches
- Ensure proper isolation if both branches are active simultaneously

Current status

- **Not yet added**: BRICKS project is not currently in the metaproject
- **Missing from workspace**: Not in `linked_projects/` directory
- **Not in manifest**: Not listed in `projects.json`

Action items

1. **Determine integration strategy:**
   - Include both branches as separate entries?
   - Focus on one primary branch?
   - Use git worktrees for branch separation?

2. **Update project manifest:**
   - Add BRICKS entry/entries to `projects.json`
   - Document branch purposes and owners
   - Include path information for both branches if needed

3. **Create symlinks:**
   - Link appropriate BRICKS directories to `linked_projects/`
   - Use descriptive names (e.g., `bricks-autolinker`, `bricks-aam-analyzer`)

4. **Update workspace:**
   - Add to VS Code workspace configuration
   - Test that both branches work correctly in the metaproject context

5. **Documentation:**
   - Update project README with BRICKS integration notes
   - Document the dual-purpose nature of the project

Next steps

- Locate BRICKS project directory structure
- Identify exact paths for both branches
- Decide on naming convention for integration
- Execute integration following established metaproject patterns

Done: saved as `data/notes/bricks_metaproject_integration.md`