from ray_haystack.ray_pipeline_settings import (
    RayPipelineSettings,
    RayPipelineSettingsWrapper,
)


def test_common_settings_merge_with_default():
    default_actor_options = RayPipelineSettingsWrapper.DEFAULT_COMMON_SETTINGS["actor_options"]

    settings: RayPipelineSettings = {
        "common": {
            "actor_options": {
                "max_concurrency": 2,
                "lifetime": "detached",  # override default
            }
        }
    }
    settings_wrapper = RayPipelineSettingsWrapper(settings)

    assert settings_wrapper.common_settings == {
        "actor_options": {
            "max_concurrency": 2,
            "enable_task_events": default_actor_options["enable_task_events"],
            "lifetime": "detached",
        }
    }


def test_component_settings():
    default_actor_options = RayPipelineSettingsWrapper.DEFAULT_COMMON_SETTINGS["actor_options"]

    settings: RayPipelineSettings = {
        "common": {
            "actor_options": {
                "num_cpus": 2,
                "namespace": "haystack",
                "get_if_exists": False,
                "runtime_env": {"env_vars": {"ENV_1": "VAL_1", "ENV_2": "VAL_2"}},
            },
        },
        "components": {
            "comp_1": {
                "actor_options": {
                    "name": "comp_1_actor",
                    "get_if_exists": True,
                    "runtime_env": {"env_vars": {"ENV_2": "VAL_2_2", "ENV_3": "VAL_3"}},
                }
            }
        },
    }
    settings_wrapper = RayPipelineSettingsWrapper(settings)

    component_settings = settings_wrapper.get_component_settings("comp_1")

    assert component_settings == {
        "actor_options": {
            "enable_task_events": default_actor_options["enable_task_events"],
            "lifetime": default_actor_options["lifetime"],
            "num_cpus": 2,
            "namespace": "haystack",
            "name": "comp_1_actor",  # component specific
            "get_if_exists": True,  # component specific
            "runtime_env": {
                "env_vars": {
                    "ENV_1": "VAL_1",
                    "ENV_2": "VAL_2_2",  # component specific
                    "ENV_3": "VAL_3",  # component specific
                },
            },
        }
    }
