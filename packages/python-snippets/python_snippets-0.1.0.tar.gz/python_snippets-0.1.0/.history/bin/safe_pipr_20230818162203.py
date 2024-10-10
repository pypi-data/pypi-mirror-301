#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/08/18 16:12:33
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

import click
from snippets import 


@click.command()
@click.argument('req')
def main(req):
    with open(req, 'r') as f:
        lines = f.readlines()
        if not line:
            continue
        
    pass