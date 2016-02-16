import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'gmi.django.avatar.test.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)

from django.conf import settings
from django_nose import NoseTestSuiteRunner

def runtests(*test_labels):
    runner = NoseTestSuiteRunner(verbosity=1, interactive=True)
    failures = runner.run_tests(test_labels)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
