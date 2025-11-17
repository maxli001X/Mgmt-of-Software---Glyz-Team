# Import all tests for test discovery
# This allows Django's test runner to find all tests

from .test_feed import *  # noqa
from .test_forms import *  # noqa
from .test_models import *  # noqa
from .test_post_actions import *  # noqa
from .test_user_stats import *  # noqa

