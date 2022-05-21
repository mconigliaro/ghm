release:
	git tag "$(shell poetry version --short)"
	git push --tags
	poetry publish
