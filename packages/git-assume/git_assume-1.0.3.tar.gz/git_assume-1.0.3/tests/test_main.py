from src.git_assume.main import main

testdata = {
    "assume": [
        "assume",
        "--netrc-longterm=tests/data/netrc_longterm",
        "--netrc=tests/data/netrc_01",
        "-y",
        "default",
    ],
    "list": [
        "list",
        "--netrc-longterm=tests/data/netrc_longterm",
    ],
}


def test_assume():
    main(testdata["assume"])


def test_list():
    main(testdata["list"])
