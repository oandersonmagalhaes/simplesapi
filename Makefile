publish:
ifndef version
	$(error You must specify a version. Usage: make publish version=x.y.z)
endif
	poetry version $(version)
	poetry publish --build