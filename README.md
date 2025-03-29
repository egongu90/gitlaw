# scm-policy
SCM policy manager

# MVP:
- Basic option support
- dry-run,check -> output what is not in desired state
- SAST, unit tests, packaging (signed, attested, provenance)
- Hierarchical merge of values, from more specific to default
- Design with multi scm support in mind
# Must have:
- More complex options
- Support for github
- Funtional tests
- Easy to extend config, ie: group1: &permissions['group2']
- CI template/Github Action 
- Read config from directory and apply all files config
# Nice to have
- Config file pre execution validation and linter
- Log state, changed, misconfigured or rendered config values in file for attestations --output result.json
- Support for bitbucket and other scm
- Multi thread, paralelism
- Value merges, ie: group inherit from other group
- Extended capabilities