#!/usr/bin/env python3

import sys
import re

def main():
    branch_name = sys.argv[1]
    pattern = r"^(feature|bugfix|hotfix)\/[a-zA-Z0-9_-]+$"
    if not re.match(pattern, branch_name):
        print("Error: Branch name does not follow the convention (feature/..., bugfix/..., hotfix/...)")
        sys.exit(1)

if __name__ == "__main__":
    main()
