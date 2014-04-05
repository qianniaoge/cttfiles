#!/usr/bin/env python
#coding=utf-8

"""
Author: secfree
Email: zzd7zzd#gmail.com
"""

import getopt
import sys
import os
import random
import time
import StringIO


def usage():
    print """
    Usage:
        create_test_files [options] directory

    Options:
        -d    create directories, default false, Create directories recursivly, 
                depth of directry is set by argument 'depth'.
        -f    create files, default true
        -h    show help message
        -m    mix mode, default false. Create directories recursivly, then create files in each directory.
              
      Directory
        --depth=DEPTH   directory depth, default 1
        --dnum=DNUM     num of directories, default 10
        --dprefix=DPRE  prefix of directory name
        --dsuffix=DSUF  suffix of directory name

      File
        --exts=EXTS                 file extensions, separated by ','
        --from_dirs=DIRECTORIES     A test file's content is one of file in DIRECTORIES, which is randomly selected.
        --from_files=FILES          A test file's content is one of FILES, which is randomly selected.
        --fprefix=FPRE              prefix of file name
        --fsuffix=FSUF              suffix of file name
        --fnum=FNUM                 num of files, default 10
        --fminsize=FMINSIZE         min size of file when file's content is created randomly. default 1.
        --fmaxsize=FMAXSIZE         max size of file when file's content is created randomly. default 1024.
    """


def create_dir_recursivly(
        parent_dir, 
        depth,
        depth_limit,
        num,
        prefix,
        suffix
    ):
    """
    create directories recursivly.

    :param parent_dir: directories will be created in parent_dir
    :type parent_dir: str

    :param depth: depth of this directory
    :type depth: int

    :param depth_limit: depth limit
    :type depth_limit: int

    :param num: num of directories to be created
    :type num: int

    :param prefix: prefix of directory name to be created
    :type prefix: str

    :param suffix: suffix of directory name to be created
    :type suffix: str
    """
    if depth > depth_limit:
        return

    for n in xrange(num):
        dn = '%s%s%s' % (prefix, n, suffix)
        path = os.path.join(parent_dir, dn)
        os.mkdir(path)
        if (depth+1) <= depth_limit:
            create_dir_recursivly(
                path,
                depth+1,
                depth_limit,
                num,
                prefix,
                suffix
                )


def get_random_content(minsize, maxsize):
    """
    create random file content.

    :param minsize: min size of file
    :type minsize: int

    :param maxsize: max size of file
    :type maxsize: int
    """
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n\t'
    n_chars = len(chars)
    size = random.randrange(minsize, maxsize)
    f = StringIO.StringIO()
    for n in xrange(size):
        f.write(chars[random.randrange(n_chars)])
    content = f.getvalue()
    f.close()
    return content


def create_file_recursivly(
        parent_dir,
        exts,
        num,
        from_files,
        prefix,
        suffix,
        minsize,
        maxsize
    ):
    """
    create files.

    :param parent_dir: directories will be created in parent_dir
    :type parent_dir: str

    :param exts: file's extension will be in exts
    :type exts: list

    :param num: num of files to be created
    :type num: int

    :param from_files: files' source content
    :type from_files: list

    :param prefix: prefix of file name to be created
    :type prefix: str

    :param suffix: suffix of file name to be created
    :type suffix: str

    :param minsize: min size of file
    :type minsize: int

    :param maxsize: max size of file
    :type maxsize: int
    """
    # go to sub directories and create files
    names = os.listdir(parent_dir)
    for nm in names:
        path = os.path.join(parent_dir, nm)
        if os.path.isdir(path):
            create_file_recursivly(
                path,
                exts,
                num,
                from_files,
                prefix,
                suffix,
                minsize,
                maxsize
            )

    n_ext = len(exts)
    n_files = len(from_files)
    ce = 0
    cf = 0
    
    # create files
    for n in xrange(num):
        # decide ext
        if n_ext:
            fn = '%s%s%s.%s' % (prefix, n, suffix, exts[ce])
            ce = (ce+1)%n_ext
        else:
            fn = '%s%s%s' % (prefix, n, suffix)

        # if file is already exist, we will not overwirite it.
        path = os.path.join(parent_dir, fn)
        if os.path.exists(path):
            continue

        # get file's content
        content = ''
        if n_files:
            with open(from_files[cf]) as f:
                content = f.read()
            cf = (cf+1)%n_files
        else:
            content = get_random_content(minsize, maxsize)
        f = open(path, 'w')
        f.write(content)
        f.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(-1)

    try:
        opts, args = getopt.getopt(sys.argv[1:], 
            'dfhm', 
            ['depth=', 'dnum=', 'dprefix=', 'dsuffix=', 
            'exts=', 'from_dirs=', 'from_files=', 'fprefix=', 'fsuffix=', 'fnum=', 'fminsize=', 'fmaxsize=']
            )
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(-1)

    if not args:
        usage()
        sys.exit(-1)
    directory = args[0]

    fvalid = True
    exts = []
    from_dirs = []
    from_files = []
    fprefix = ''
    fsuffix = ''
    fnum = 10
    fminsize = 1
    fmaxsize = 1024

    dvalid = False
    depth = 1
    dnum = 10
    dprefix = ''
    dsuffix = ''

    for t, a in opts:
        if t == '-d':
            dvalid = True
            fvalid = False
        if t == '-f':
            fvalid = True
        if t == '-h':
            usage()
            sys.exit(0)
        if t == '-m':
            fvalid = True
            dvalid = True
        if t == '--depth':
            depth = int(a)
        if t == '--dnum':
            dnum = int(a)
        if t == '--dprefix':
            dprefix = a
        if t == '--dsuffix':
            dsuffix = a
        if t == '--exts':
            exts = a.split(',')
        if t == '--from_dirs':
            from_dirs.extend(a.split(','))
        if t == '--from_files':
            from_files.extend(a.split(','))
        if t == '--fprefix':
            fprefix = a
        if t == '--fsuffix':
            fsuffix = a
        if t == '--fnum':
            fnum = int(a)
        if t == '--fmsize':
            fmsize = int(a)

    # seed random
    random.seed(time.time())

    # create directories if dvalid
    if dvalid:
        create_dir_recursivly(
            parent_dir=directory, 
            depth=1, 
            depth_limit=depth, 
            num=dnum, 
            prefix=dprefix, 
            suffix=dsuffix
            )

    # add files in from_dirs to from_files
    for d in from_dirs:
        names = os.listdir(d)
        for nm in names:
            path = os.path.join(d, nm)
            if os.path.isfile(path):
                from_files.append(path)

    # create files if fvalid
    if fvalid:
        create_file_recursivly(
            parent_dir=directory, 
            exts=exts, 
            num=fnum,
            from_files=from_files, 
            prefix=fprefix, 
            suffix=fsuffix,
            minsize=fminsize,
            maxsize=fmaxsize
            )











