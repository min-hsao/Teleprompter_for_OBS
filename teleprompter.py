import obspython as obs
import time

# Global variables
source_name = "Teleprompter_Text"
text = "This is a sample teleprompter text.\nReplace this with your script."
scroll_speed = 1  # Pixels per frame
scroll_position = 0
alignment = "left"
font_size = 50
line_height = 1.2
is_running = False
hotkey_ids = {}  # To store hotkey IDs

def update_css():
    """Update the CSS with current styling and scroll position"""
    source = obs.obs_get_source_by_name(source_name)
    if source:
        try:
            settings = obs.obs_data_create()
            css = f"""
                div {{
                    text-align: {alignment};
                    font-size: {font_size}px;
                    line-height: {line_height};
                    margin-top: -{scroll_position}px;
                    white-space: pre-line;
                }}
            """
            obs.obs_data_set_string(settings, "css", css)
            obs.obs_source_update(source, settings)
        finally:
            obs.obs_data_release(settings)
            obs.obs_source_release(source)

# ... [keep previous update_text_source, tick_callback, reset_position_button functions] ...

def on_hotkey_start_stop(pressed):
    """Handle start/stop hotkey"""
    global is_running
    if pressed:
        is_running = not is_running

def on_hotkey_speed_up(pressed):
    """Handle speed increase hotkey"""
    global scroll_speed
    if pressed:
        scroll_speed = min(10.0, scroll_speed + 0.5)

def on_hotkey_speed_down(pressed):
    """Handle speed decrease hotkey"""
    global scroll_speed
    if pressed:
        scroll_speed = max(0.1, scroll_speed - 0.5)

def on_hotkey_mouse_wheel(pressed, delta):
    """Handle mouse wheel scroll"""
    global scroll_speed
    if pressed:
        scroll_speed = max(0.1, min(10.0, scroll_speed + (delta * 0.1)))

def script_properties():
    """Add hotkey configuration to properties"""
    props = obs.obs_properties_create()

    # Original properties
    obs.obs_properties_add_text(props, "text", "Teleprompter Text", obs.OBS_TEXT_MULTILINE)
    # ... [keep other existing properties] ...

    # Add hotkey controls
    obs.obs_properties_add_button(props, "start_stop", "Start/Stop Teleprompter", start_stop_button)
    obs.obs_properties_add_button(props, "reset_position", "Reset Scroll Position", reset_position_button)

    # Hotkey configuration
    obs.obs_properties_add_hotkey(props, "hotkey_start_stop", "Start/Stop Hotkey (Space)")
    obs.obs_properties_add_hotkey(props, "hotkey_speed_up", "Speed Up (Up Arrow)")
    obs.obs_properties_add_hotkey(props, "hotkey_speed_down", "Slow Down (Down Arrow)")
    obs.obs_properties_add_hotkey(props, "hotkey_mouse_wheel", "Mouse Wheel Control")

    return props

def script_update(settings):
    """Handle hotkey registration"""
    global hotkey_ids

    # Register hotkeys
    hotkey_ids["start_stop"] = obs.obs_data_get_array(settings, "hotkey_start_stop")
    hotkey_ids["speed_up"] = obs.obs_data_get_array(settings, "hotkey_speed_up")
    hotkey_ids["speed_down"] = obs.obs_data_get_array(settings, "hotkey_speed_down")
    hotkey_ids["mouse_wheel"] = obs.obs_data_get_array(settings, "hotkey_mouse_wheel")

def script_save(settings):
    """Save hotkey configurations"""
    obs.obs_data_set_array(settings, "hotkey_start_stop", hotkey_ids["start_stop"])
    obs.obs_data_set_array(settings, "hotkey_speed_up", hotkey_ids["speed_up"])
    obs.obs_data_set_array(settings, "hotkey_speed_down", hotkey_ids["speed_down"])
    obs.obs_data_set_array(settings, "hotkey_mouse_wheel", hotkey_ids["mouse_wheel"])

def script_description():
    return """OBS Teleprompter with Controls
    Controls:
    - Space: Start/Stop
    - Up/Down Arrows: Adjust Speed
    - Mouse Wheel: Adjust Speed
    - Reset Button: Reset Position
    """

# ... [keep previous script_load, script_unload, and other functions] ...

# Register hotkey callbacks
def script_load(settings):
    obs.timer_add(tick_callback, 16)
    update_text_source()
    update_css()

    # Register hotkey callbacks
    hotkey_callbacks = {
        "start_stop": on_hotkey_start_stop,
        "speed_up": on_hotkey_speed_up,
        "speed_down": on_hotkey_speed_down,
        "mouse_wheel": on_hotkey_mouse_wheel
    }

    for name, callback in hotkey_callbacks.items():
        hotkey_id = obs.obs_hotkey_register_frontend(
            f"htk_{name}",
            f"Teleprompter {name.replace('_', ' ').title()}",
            callback
        )
        hotkey_ids[name] = hotkey_id
