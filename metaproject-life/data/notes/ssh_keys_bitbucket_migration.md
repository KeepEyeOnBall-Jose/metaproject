Title: SSH keys and migrating repos from Bitbucket to GitHub
Created: 2025-10-01
Tags: ssh, git, github, bitbucket, migration, general-technical

Category: General Technical (AI & SW Dev Tools)

Key questions

- Should I have an SSH key for Git operations?
- How can I port all of my repos from Bitbucket to GitHub?
- Should I migrate everything or be selective?

SSH Key considerations

**Benefits of SSH keys:**
- No need to enter username/password for Git operations
- More secure than HTTPS with credentials
- Required for many automated workflows and CI/CD
- Enables secure access to servers and remote development

**Setup checklist:**
- Generate SSH key pair (`ssh-keygen -t ed25519 -C "your_email@example.com"`)
- Add public key to GitHub/Bitbucket account settings
- Configure SSH agent to manage keys
- Test connection (`ssh -T git@github.com`)
- Update Git remote URLs to use SSH format

Bitbucket to GitHub migration

**Migration strategies:**
- **Bulk migration**: Use GitHub's import tool or scripts to migrate all repos
- **Selective migration**: Choose active/important repos first
- **Gradual migration**: Move repos as you work on them

**Migration steps per repo:**
1. Create new GitHub repo (can be private initially)
2. Clone Bitbucket repo locally
3. Add GitHub as new remote (`git remote add github git@github.com:user/repo.git`)
4. Push all branches and tags to GitHub
5. Update any CI/CD configurations
6. Update documentation and links
7. Archive or delete Bitbucket repo when ready

**Considerations:**
- Private vs public repo decisions
- Issue/wiki migration (may require separate tools)
- Update any hardcoded Bitbucket URLs in code/docs
- Notify collaborators of the migration

Decision factors for "Should I migrate?"

**Reasons to migrate:**
- GitHub has better ecosystem integration
- More active community and discovery
- Better CI/CD options (GitHub Actions)
- Easier collaboration features

**Reasons to keep some on Bitbucket:**
- Already established workflows
- Team preferences
- Private repo pricing differences
- Integration with Atlassian tools (Jira, Confluence)

Next actions to research

- Compare current SSH key setup across machines
- Audit Bitbucket repos to prioritize migration candidates
- Test GitHub import tool with a sample repo
- Research bulk migration scripts/tools

Done: saved as `data/notes/ssh_keys_bitbucket_migration.md`