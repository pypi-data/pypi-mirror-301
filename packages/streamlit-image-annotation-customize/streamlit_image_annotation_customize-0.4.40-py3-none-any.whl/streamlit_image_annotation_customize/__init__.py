import os

IS_RELEASE = os.getenv('IS_RELEASE', 'False') == 'true'

from .Detection import detection
