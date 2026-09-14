module.exports = {
	parserPreset: "conventional-changelog-conventionalcommits",
	rules: {
		"subject-empty": [2, "never"],
		"type-case": [2, "always", "lower-case"],
		"type-empty": [2, "never"],
		"type-enum": [
			2,
			"always",
			[
				"feat",
				"fix",
				"chore",
				"refactor",
				"docs",
				"style",
				"test",
				"perf",
				"ci",
				"build",
				"revert",
				"meta",
			],
		],
	},
};
