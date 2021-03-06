
__version__     = '2011.07.10-03'
__author__      = 'Scott Rogers, aka trash80'
__stability__   = 'alpha'
__copying__     = """Copyright (C) 2011 W. Scott Rogers \
                        This program is free software.
                        You can redistribute it and/or modify it under the terms of the
                        GNU General Public License as published by the Free Software Foundation;
                        version 2 of the License.
                    """
#   Special thanks: h2, aka Harald Hope

import optparse

################################################################################
####
####        Main xiin class
####
################################################################################

class Base(object):

    def __init__(self, textConf = 'xiin'):
        self = self
        self.version    = '%prog-{0}-{1}'
    #end

    def xiin(self, xiinArgs):
        """
        Starts the read capabilities
        """
        # check python version
        self.__check_python_version()

        # http://docs.python.org/library/optparse.html

        xiinDesc = """ xiin is a directory parser meant to help debug inxi(www.inxi.org) bugs.
            xiin will take a given directory, usually /sys or /proc and write the contents
            to a specified file in key:value format where key is the directory/filename
            and value is the contents of key."""

#        xiinUsage   = "%prog [-d] <directory to read> [-f] <file to write>"

        xiinVersion = self.version.format(__version__, __stability__)

        dirHelp     = 'Directory containing files. \
                        [Usage:  ] \
                        [Example:  ]'
        fileHelp    = 'If used write report to file, otherwise write output to the screen. \
                        [Usage:  ] \
                        [Example:  ]'
        displayHelp = 'Prints to terminal not to a file.  Cannot use with -f option. \
                        [Usage:  ] \
                        [Example:  ]'
        grepHelp    = 'Grep-like function. Can be sent to display(default) or file. \
                        [Usage: unused at this time] \
                        [Example: ]'
        uploadHelp  = 'Uploads a specified file to a specified ftp sight.  \
                        [Usage: xiin -u <source> <target> <uname> <password> ] \
                        [Example: xiin -u /home/myhome/.inxi/some.txt somedomain.com anon anon ]'

        self.parser = optparse.OptionParser(description = xiinDesc, version = xiinVersion)

        self.parser.add_option('-d', '--directory', dest = 'directory', help = dirHelp)
        self.parser.add_option('-f', '--file', dest = 'filename', help = fileHelp)
        self.parser.add_option('-o', '--out', action = 'store_true', dest = 'display', help = displayHelp)
        self.parser.add_option('-g', '--grep', dest = 'grep', help = grepHelp)
        self.parser.add_option('-u', '--upload', nargs=2, dest = 'upload', help = uploadHelp)

        (options, args) = self.parser.parse_args()

        options.args = xiinArgs

        self.__use_checker(options)
        self.__switch(options)

        exit(0)
    #end

    def __use_checker(self, xiinArgDict):
        """
        Checks for use errors.
        """
        if xiinArgDict.upload is None:
        # no arguements specified, so display helpful error
            if len(xiinArgDict.args) < 2:
                self.parser.error('Nothing to do. Try option -h or --help.')
                exit(2)

        # no output specified
            elif xiinArgDict.filename is None and xiinArgDict.display is None and xiinArgDict.grep is None:
                self.parser.error('specify to display output or send to a file')
                exit(3)

        # reading /proc will hang system for a while, it's a big deep virtual-directory
            elif xiinArgDict.directory == '/proc':
                self.parser.error('xiin can not walk /proc')
                exit(4)

        # the directory needed when option used
            elif xiinArgDict.directory is None:
                self.parser.error('xiin needs a directory')
                exit(5)

        else:
            if len(xiinArgDict.upload ) < 2:
                print('')
                self.parser.error('ERROR: No xiin upload options given')
                self.parser.error('[Usage: uploader <source> <target> <uname> <password> ]')
                exit(6)
    #end

    def __switch(self, xiinArgDict):
        """
        Traffic director.
        """
        from reader import Reader
        reader = Reader()
        # Write output
        if xiinArgDict.filename is not None:
            print('Starting xiin...')
            print('')
            with open(xiinArgDict.filename, 'w') as xiinArgDict.outputFile:
                reader.info(xiinArgDict)

        #Displays output.
        elif xiinArgDict.display:
            print('Starting xiin...')
            print('')
            reader.info(xiinArgDict)

        elif xiinArgDict.grep is not None:
            print('Starting xiin...')
            print('')
            print('Searching files...')
            print('')
            self.grepXiinInfo(xiinArgDict.grep)

        elif xiinArgDict.upload is not None:
    #        xiin.ftp = {'source': '', 'destination': '', 'uname': '', 'password': ''}
            from uploader import Uploader

            xiinArgDict.ftpSource      = None
            xiinArgDict.ftpDestination = None
            xiinArgDict.ftpUname       = None
            xiinArgDict.ftpPwd         = None

            if len(xiinArgDict.upload ) > 0:
                xiinArgDict.ftpSource      = xiinArgDict.upload[0]
                xiinArgDict.ftpDestination = xiinArgDict.upload[1]

            if len(xiinArgDict.upload ) > 2:
                # Legacy support
                if xiinArgDict.ftpUname is 'anon' or xiinArgDict.ftpUname is 'anonymous':
                    pass
                else:
                    xiinArgDict.ftpUname       = xiinArgDict.upload[2]
                    xiinArgDict.ftpPwd         = xiinArgDict.upload[3]

            print('Starting xiin uploader...')
            print('')
            print('Uploading debugging information...')
            print('')

            uploader = Uploader()
            uploader.upload(xiinArgDict.ftpSource, xiinArgDict.ftpDestination, xiinArgDict.ftpUname, xiinArgDict.ftpPwd)
        else:
            print('ERROR: Unknown')
            exit(7)
    #end

    def __check_python_version(self):
        from PythonVersionCheck import PythonVersionCheck
        # check the Version of python
        checkPython = PythonVersionCheck()
        checkPython.check()
    #end
#end