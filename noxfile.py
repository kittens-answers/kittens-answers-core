import nox


@nox.session(python=False)
def style(session: nox.Session):
    session.run("poetry", "run", "isort", ".", external=True)
    session.run("poetry", "run", "black", ".", external=True)
    session.run("poetry", "run", "ruff", ".", external=True)
    session.run("poetry", "run", "deptry", "src", "tests", external=True)


@nox.session(python=False)
def test(session: nox.Session):
    session.run("poetry", "run", "pytest", external=True)
