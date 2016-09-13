import click

@click.command()
@click.argument("image", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(exists=False))
@click.option("--shape", default="1,1")
def __main__(image, output, shape):
    x, y = map(int, shape.split(","))

    click.echo((x, y))

if __name__ == "__main__":
    __main__()
