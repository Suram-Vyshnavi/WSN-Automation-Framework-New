"""
Force-load nested step modules so Behave can register all step definitions
from Common_steps and Faculty_steps regardless of behave version/config.
"""

from features.steps.Common_steps.Common_activityinsights_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_batchmembers_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_chat_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_createmeeting_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_login_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_notifications_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_performance_steps import *  # noqa: F401,F403
from features.steps.Common_steps.Common_settings_steps import *  # noqa: F401,F403

from features.steps.Faculty_steps.Batch_details_collaboratesetup_steps import *  # noqa: F401,F403
from features.steps.Faculty_steps.Batch_details_scorecard_steps import *  # noqa: F401,F403
from features.steps.Faculty_steps.Batch_details_steps import *  # noqa: F401,F403
from features.steps.Faculty_steps.Create_newbatch_steps import *  # noqa: F401,F403
from features.steps.Faculty_steps.Home_steps import *  # noqa: F401,F403
