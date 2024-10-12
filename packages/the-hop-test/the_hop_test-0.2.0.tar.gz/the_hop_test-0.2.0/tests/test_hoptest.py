import pytest
from hoptest.hoptest import commit_message_format


@pytest.mark.parametrize(
    "msg,result",
    (
        ("hello\n\nworld", True),
        ("[prefix]: hello\n\nworld", True),
        ("hello\nworld", False),
        ("h" * 53 + "\n\ntext", False),
        ("h" + "\n\n" + "z" * 71 + "\n\nanother line", True),
        ("h" + "\n\n" + "z" * 79, False),
        (
            """Update documentation for setting up and testing

The README didn't accurately capture how to set up and work on this
project. Some dependencies were not explained, and some institutional
knowledge on how to work with Docker was being being assumed or passed
around in Slack instead of documented in the README.

This PR attempts to remedy that so that anyone, with no context, should
be able to setup this project and get to work.

venv is a standardlib subset of virtualenv that has been available since
Python 3.3. This project isn't using any of the extended features of
virtualenv so might as well simplify the dependency graph.

The README is a little vague about what python executable is to be used
and what name it is called. This change attempts to clarify using python
within the virtual environment vs using the system-installed python.

I didn't know how to mount the code so as to avoid doing docker build .
ever time I made a change.

This change addresses the need by:
* Removing all references to virtualenv and replacing it with stdlib
  venv module
* Tells you how to install Python 3.8
* Clarifies which python executable it means to use in different places
  (system vs venv)
* Documents how to use docker binding mounts to edit code and run it
  without rebuilding""",
            True,
        ),
        (
            """Remove suspicious import munging code

All test files have relied on a path modification to properly function.
This is not common and should not be necessary here.

This change addresses the need by:
* making the tests module import-able with an __init__.py file
""",
            True,
        ),
        (
            """Remove AWS Lambda altogether

The jump through AWS Lambda from EventBridge (formerly CloudWatch) to
AWS Batch was unnecessary, since EventBridge can directly invoke Batch
these days.

This change addresses the need by:
* removing the usage of a Lambda function altogether
""",
            True,
        ),
    ),
)
def test_commit_message_regex(msg, result):
    assert commit_message_format(msg) is result
