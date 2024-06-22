# back-end

## Commands
If profile is not set, it will use the `default` profile
### Run project locally
This command will also build as well as run through all test cases.
```bash
./build.sh -p [your profile name] start
```

### Test project
This command will also build.
```bash
./build.sh -p [your profile name] start
```

###  Deploy to AWS
This command will also build as well as run through all test cases.
```bash
./build.sh -p [your profile name] deploy
```

### Poetry

Package management: poetry <br>
[Good resource on what poetry is.](https://chariotsolutions.com/blog/post/building-lambdas-with-poetry/)

Install package
```bash
poetry add [package name]
```

Auto reformat
```bash
black --target-version=py35 . --line-length 80
```

Manually trigger precommit
```bash
poetry shell
pre-commit run --all-files
```
