"""Extract a small sample from order data to speedup tests

use:

    python make_dev_data.py data/orders.csv data/orders_test.csv

"""
import click


def shorten_file(input_file,output_file,n):
    """Creates a new file with reduced line count

    writes the first n lines from input_file to output_file
    """
    print('limiting {} to {} lines, writes to {}'\
        .format(input_file,n,output_file))
    source=open(input_file)
    sink=open(output_file,'w')
    for _ in range(n):
        sink.write(source.readline())
    
@click.command()
@click.argument('original',type=click.Path())
@click.argument('shortened',type=click.Path())
@click.option('--n_lines',type=click.INT,default=1000)
def main(original,shortened,n_lines):
    shorten_file(original,shortened,n_lines)

if __name__ == '__main__':
    main()
    
