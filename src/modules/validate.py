# pylint: disable=too-many-branches, too-many-statements
def validate_ref(ref_type, *argv):
    failed = False
    message = ""
    if ref_type == "article":
        author = argv[0]
        title = argv[1]
        journal = argv[2]
        year = argv[3]

        if len(author) > 100:
            failed = True
            message = "Name of author cannot exceed 100 characters"

        if len(title) > 500:
            failed = True
            message = "Title cannot exceed 500 characters"

        if len(journal) > 100:
            failed = True
            message = "Name of journal cannot exceed 100 characters"

        if year < 1900 or year > 2099:
            failed = True
            message = "Year must be set between 1900 and 2099"

    if ref_type == "book":
        author = argv[0]
        year = argv[1]
        title = argv[2]
        publisher = argv[3]
        address = argv[4]

        if len(author) > 100:
            failed = True
            message = "Name of author cannot exceed 100 characters"

        if len(title) > 500:
            failed = True
            message = "Title cannot exceed 500 characters"

        if len(publisher) > 100:
            failed = True
            message = "Name of publisher cannot exceed 100 characters"

        if len(address) > 100:
            failed = True
            message = "Name of address cannot exceed 100 characters"

        if year < 1 or year > 2099:
            failed = True
            message = "Year must be set between 1 and 2099"

    if ref_type == "inproceedings":
        author = argv[0]
        title = argv[1]
        booktitle = argv[2]
        year = argv[3]

        if len(author) > 100:
            failed = True
            message = "Name of author cannot exceed 100 characters"

        if len(title) > 500:
            failed = True
            message = "Title cannot exceed 500 characters"

        if len(booktitle) > 100:
            failed = True
            message = "Name of booktitle cannot exceed 100 characters"

        if year < 1700 or year > 2099:
            failed = True
            message = "Year must be set between 1700 and 2099"



    return failed, message
