from click.testing import CliRunner


def test_smoke_cli():
    from colorevo import __version__
    from colorevo.maingui import main

    runner = CliRunner()
    result = runner.invoke(main, args=["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout

    result = runner.invoke(main, args=["--help"])
    assert result.exit_code == 0
    assert "--reset" in result.stdout
    assert "--keep-alive" in result.stdout
    assert "--no-keep-alive" in result.stdout
