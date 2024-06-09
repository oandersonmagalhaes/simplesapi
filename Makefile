publish:
	@if [ -z "$(version)" ]; then \
		echo "Error: You must specify a version. Usage: make publish version=x.y.z"; \
		exit 1; \
	fi
	poetry version $(version)
	poetry publish --build