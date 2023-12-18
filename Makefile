#***************************************************************************
# Fix photo metadata and delete duplicates
#***************************************************************************
## Options:
## * [path] required. See README.md for more details.
## * [folder_priority] required. See README.md for more details.
.PHONY: run
run:
	@echo "Running fix_photos.py"
	@python3 src/fix_metadata.py "$(path)"
	@echo "Running delete_duplicates.py"
	@python3 src/delete_duplicates.py "$(path)" '$(folder_priority)'
	
#***************************************************************************
# Run tests
#***************************************************************************
.PHONY: test
test:
	@echo "Running tests"
	@python3 -m unittest discover -s test -p "*_test.py"

