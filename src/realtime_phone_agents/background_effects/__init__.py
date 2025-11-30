from realtime_phone_agents.background_effects.keyboard import KeyboardEffect


def get_sound_effect(effect_type: type | None = None):
    """
    Create and return a sound effect instance.

    Args:
        effect_type: The type of effect to create. Defaults to KeyboardEffect.

    Returns:
        An instance of the specified effect type.
    """
    effect_type = effect_type or KeyboardEffect
    return effect_type()
