release:
	git tag "$(shell poetry version --short)"
	git push --tags
	poetry build
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish # -r testpypi -v
