"""Extract a small sample from order data to speedup tests"""

full_order_file='data/orders.csv'
dev_order_file='data/orders_dev.csv'
n_lines=1000

def shorten_file(input,output,n):
    """"""
    source=open(full_order_file)
    sink=open(dev_order_file,'w')
    for _ in range(n_lines):
        sink.write(source.readline())
    

if __name__ == '__main__':
    shorten_file(full_order_file,dev_order_file,n_lines)
