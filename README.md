### Elgameya

ElGameya is a custom business application built on the Frappe Framework by the ElGameya Development Team. It supports ElGameya\'s digital financial services, which aim to digitize traditional rotating savings and money cycles (ROSCA), enabling individuals to participate in organized savings cycles and manage their financial commitments digitally. The application extends the Frappe platform with organization-specific business functionality, workflows, data management, integrations, automation, and reporting to support ElGameya\'s digital financial services operations.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app elgameya
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/elgameya
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
