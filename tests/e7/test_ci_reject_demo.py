import unittest


class PullRequestRejectionDemo(unittest.TestCase):
    def test_intentional_failure_for_branch_protection_demo(self):
        self.fail(
            "E7 demonstration: this PR must be blocked until the failing test is fixed"
        )


if __name__ == "__main__":
    unittest.main()
