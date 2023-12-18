#***************************************************************************
# Fix photo metadata and delete duplicates
#***************************************************************************
## Options:
## * [path] required. See README.md for more details.
## * [folder_priority] required. See README.md for more details.
.PHONY: run
run:
	@echo "Running fix_photos.py"
	@python3 fix_photos.py $(path)
	@echo "Running delete_duplicates.py"
	@python3 delete_duplicates.py $(path) $(folder_priority)

.PHONY: test
test:
	@echo "Running tests"
	@python3 -m unittest discover -s tests -p "*_test.py"
