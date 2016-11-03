#!usr/bin/env python3
#-*- coding: UTF-8 -*-

from build import Route, Condition, Regex, Path, Variable, Method, SpecialDestination, Build
import os

def run():
    if os.getcwd().endswith('_aelfi'):
        print('Please make sure to run this tool from the projects root directory, not the `_aelfi` folder!\nRunning Anyway...\n')
    build = Build.from_file('aelfi.build')
    build.options = "+ExecCGI -Indexes"
    build.handlers = ['cgi-script .py .pl']
    build.indices = ["index.py", "index.pyv", "index.php", "index.html", "index.htm",
                        "index.xml", "index.txt", "index.jpg", "index.png",
                        "index.gif", "index.jpeg", "index.pl"]
    # Template-Base Documents (TBDs) Redirect
    build.routes.append(Route(
                                destination=Path('_aelfi/tbd.py?AELFI_TBD_PAGE={1}'),
                                origins=[Regex('^(.*)$')],
                                conditions=[
                                    Condition('&', Variable('filepath'),  Method('.isfile'), negate=False),
                                    Condition('&', Variable('filepath'),  Regex('\.pyv$'), negate=False),
                                ],
                                options=['L', 'END', 'QSA']
                            ))
    # Python Documents Redirect
    build.routes.append(Route(
                                destination=Path('_aelfi/loader.py?AELFI_PAGE={1}'),
                                origins=[Regex('^(.*)$')],
                                conditions=[
                                    Condition('&', Variable('filepath'),  Method('.isfile'), negate=False),
                                    Condition('&', Variable('filepath'),  Regex('\.py$'), negate=False),
                                ],
                                options=['L', 'END', 'QSA']
                            ))
    # Index Counter-protection
    build.routes.insert(0, Route(
                                destination=Path('{1}'),
                                origins=[Regex('^(.*)$')],
                                conditions=[
                                    Condition('&', Variable('filepath'),  Path('./?$', flags='a'), negate=False)
                                ],
                                options=['L', 'END', 'QSA']
                            ))
    # AElfi folder protection
    #build.routes.insert(0, Route(
    #                            destination=SpecialDestination('-'),
    #                            origins=[Regex('^.*$')],
    #                            conditions=[
    #                                Condition('&', Variable('filepath'),  Path('./_aelfi/?', flags='a'), negate=False)
    #                            ],
    #                            options=['F']
    #                        ))
    # AElfi build file protection
    build.routes.insert(0, Route(
                                destination=SpecialDestination('-'),
                                origins=[Regex('^.*$')],
                                conditions=[
                                    Condition('&', Variable('filepath'),  Path('./aelfi.build$', flags='a'), negate=False)
                                ],
                                options=['F']
                            ))
    # AElfi view file protection
    build.routes.insert(0, Route(
                                destination=SpecialDestination('-'),
                                origins=[Regex('^.*$')],
                                conditions=[
                                    Condition('&', Variable('filepath'),  Regex('\.view$'), negate=False)
                                ],
                                options=['F']
                            ))

    #Write new versions
    with open('.htaccess', 'w') as htaccess_file:
        htaccess_file.write(build.build_htaccess())
    with open('_aelfi/config.json', 'w') as conf_file:
        conf_file.write(build.build_config())

if __name__ == '__main__':
    run()
    print('built!')