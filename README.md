# Elgameya

## Overview

ElGameya is a custom business application built on the Frappe Framework by the ElGameya Development Team. It supports ElGameya\'s digital financial services, which aim to digitize traditional rotating savings and money cycles (ROSCA), enabling individuals to participate in organized savings cycles and manage their financial commitments digitally. The application extends the Frappe platform with organization-specific business functionality, workflows, data management, integrations, automation, and reporting to support ElGameya\'s digital financial services operations.

## Installation

### Prerequisites

- Frappe Bench installed
- Python 3.8+
- Node.js 14+

### Installation Steps

1. Install the app:
```bash
bench get-app --branch main elgameya <repo-url>
```

2. Install to site:
```bash
bench --site your-site install-app elgameya
```

3. Migrate database:
```bash
bench --site your-site migrate
```

4. Build assets:
```bash
bench --site your-site build
```

## Updating the App

1. Update the app:
```bash
bench update --reset --apps elgameya
```

2. Migrate changes:
```bash
bench --site your-site migrate
```

3. Build assets:
```bash
bench --site your-site build
```

## Uninstalling the App

1. Uninstall from site:
```bash
bench --site your-site uninstall-app elgameya
```

2. Remove from bench:
```bash
bench remove-app elgameya
```

## Development

### Running Tests
```bash
bench --site your-site run-tests elgameya
```

### Building Assets
```bash
bench --site your-site build
```

### Clearing Cache
```bash
bench --site your-site clear-cache
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Pre-commit

There's a [pre-commit](https://pre-commit.com/) hook included in the repo. You can set it up by doing

```bash
pip install pre-commit
pre-commit install
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email info@elgameya.net or create an issue in the repository.