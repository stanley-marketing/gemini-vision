# Maintainers

This document lists the maintainers of the Gemini Vision MCP Server project.

## Current Maintainers

- **Progressus Software Ltd.** - Primary maintainer
- Contact: oss@progressus-software.com

## Maintainer Responsibilities

- Review and merge pull requests
- Triage and respond to issues
- Manage releases and versioning
- Ensure code quality and security standards
- Maintain project documentation
- Coordinate with contributors

## Becoming a Maintainer

We welcome contributions from the community. Active contributors who demonstrate:

- Consistent high-quality contributions
- Understanding of the project goals and architecture
- Commitment to the project's code of conduct
- Willingness to help with maintenance tasks

May be invited to become maintainers.

## Communication

- **General Questions**: Create GitHub issues or discussions
- **Security Issues**: Email security@progressus-software.com
- **Maintainer Contact**: Email oss@progressus-software.com

## Release Process

Maintainers follow this process for releases:

1. Update version in package.json and pyproject.toml
2. Update CHANGELOG.md
3. Create and push git tag (vX.Y.Z)
4. GitHub Actions automatically creates release with SBOM
5. Publish to npm registry if applicable