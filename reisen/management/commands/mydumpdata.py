# taken (and adapted) from >> https://djangosnippets.org/snippets/10625/
#
from StringIO import StringIO
from io import open
from django.core.management.commands.dumpdata import Command as Dumpdata


class Command(Dumpdata):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--pretty', default=False, action='store_true',
            dest='pretty', help='Avoid unicode escape symbols'
        )

    def handle(self, *args, **kwargs):
        captcha_stdout = StringIO()
        old_stdout = self.stdout
        self.stdout = captcha_stdout
        output = kwargs['output']
        kwargs['output'] = None
        super(Command, self).handle(*args, **kwargs)
        captcha_stdout.seek(0)
        data = captcha_stdout.read()
        data = data.encode()
        if kwargs.get('pretty'):
            data = data.decode("unicode_escape").encode("utf-8")
        if output:
            with open(output, 'w', encoding='utf-8') as stream:
                stream.write(data.decode('utf-8'))
        else:
            old_stdout.write(data.decode('utf-8'))
