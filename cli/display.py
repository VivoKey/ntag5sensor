def celsius_to_fahrenheit(temp):
    return (temp * 1.8) + 32

def print_system_info(info):
    print(f" - Unique identifier (UID): {info["uid"].hex()}")
    if("afi" in info):
        print(f" - Application family identifier (AFI): 0x{info["afi"]["family"]:01x}, sub 0x{info["afi"]["sub_family"]:01x}")
    if("dsfid" in info):
        print(f" - Data storage identifier (DSFID): 0x{info["dsfid"]:02x}")
    if("blocksize" in info):
        print(f" - Size of a memory block: {info["blocksize"]} bytes")
    if("numblocks" in info):
        print(f" - Number of memory blocks: {info["numblocks"]}")
    if("memory" in info):
        print(f" - Total amount of memory: {info["memory"]} bytes")
    if("icref" in info):
        print(f" - IC manufacturer reference: 0x{info["icref"]:02x}")

def print_extended_system_info(info):
    print_system_info(info)
    if("moi" in info):
        print(f" - Memory addressing mode (MOI): {"2-byte" if(info["moi"] == 1) else "1-byte"}")
    if("cmdlist" in info):
        print(" - Supported Commands:")
        for command, supported in info["cmdlist"].items():
            print(f"   - {command.replace("_", " ")}: {supported}")
    if("csi" in info):
        print(" - Cryptographic suite identifier (CSI) list:")
        for csi in info["csi"]:
            print(f"   - Class: {csi["class"]}, ID: {csi["id"]}")

def print_nxp_system_info(info):
    if("pp_pointer" in info):
        print(f" - Protection pointer (PP): 0x{info["pp_pointer"]:02x}")
    if("pp_condition" in info):
        print(" - Protection pointer condition flags:")
        for name, flag in info["pp_condition"].items():
            print(f"   - {name.replace("_", " ")}: {flag}")
    if("lock_bits" in info):
        print(" - Lock bits:")
        for name, flag in info["lock_bits"].items():
            print(f"   - {name.replace("_", " ")}: {flag}")
    if("features" in info):
        print(" - Feature flags:")
        for key, val in info["features"].items():
            print(f"   - {key.replace("_", " ")}: {val}")
    if("extended_feature_flags_raw" in info):
        print(f" - Extended feature flags: {info["extended_feature_flags_raw"].hex()}")

def print_config_info(info):
    if("auto_standby_mode_enabled" in info):
        print(f" - Auto standby mode enabled: {info["auto_standby_mode_enabled"]}")
    if("lock_session_register" in info):
        print(f" - Session register locked: {info["lock_session_register"]}")
    if("energy_harvesting_mode" in info):
        print(f" - Energy harvesting mode: {info["energy_harvesting_mode"]}")
    if("sram_copy_enabled" in info):
        print(f" - SRAM copy on POR enabled: {info["sram_copy_enabled"]}")

    if("pt_transfer_direction" in info):
        print(f" - Pass-through transfer direction: {info["pt_transfer_direction"]}")
    if("sram_enabled" in info):
        print(f" - SRAM enabled: {info["sram_enabled"]}")
    if("arbiter_mode" in info):
        print(f" - Arbiter mode: {info["arbiter_mode"]}")
    if("use_case" in info):
        print(f" - Use case configuration: {info["use_case"]}")
    if("eh_arbiter_mode_enabled" in info):
        print(f" - EH arbiter mode enabled: {info["eh_arbiter_mode_enabled"]}")

    if("gpio0_slew_rate" in info):
        print(f" - GPIO0 slew rate: {info["gpio0_slew_rate"]}")
    if("gpio1_slew_rate" in info):
        print(f" - GPIO1 slew rate: {info["gpio1_slew_rate"]}")
    if("lock_block_command_supported" in info):
        print(f" - Lock block command supported: {info["lock_block_command_supported"]}")
    if("extended_commands_supported" in info):
        print(f" - Extended commands supported: {info["extended_commands_supported"]}")
    if("gpio0_pad_in" in info):
        print(f" - GPIO0 pad input mode: {info["gpio0_pad_in"]}")
    if("gpio1_pad_in" in info):
        print(f" - GPIO1 pad input mode: {info["gpio1_pad_in"]}")

def print_eh_ed_config_info(config):
    if("eh_enable" in config):
        state = "enabled" if config["eh_enable"] else "disabled"
        print(f" - Energy harvesting at boot: {state}")
    if("eh_vout_i_sel" in config):
        print(f" - Energy harvesting minimum current trigger: {config["eh_vout_i_sel"]} mA")
    if("eh_vout_v_sel" in config):
        print(f" - Energy harvesting output voltage: {config["eh_vout_v_sel"]} V")
    if("disable_power_check" in config):
        state = "disabled" if config["disable_power_check"] else "enabled"
        print(f"  - Energy harvesting power check: {state}")
    if("ed_config" in config):
        print(f" - Energy detection config: {config["ed_config"].replace("_", " ").capitalize()}")

def print_tmp117_config_info(info):
    if("status_flags" in info):
        print(" - Status Flags:")
        for key, val in info["status_flags"].items():
            print(f"    - {key.replace("_", " ").capitalize()}: {"Yes" if val else "No"}")
    if("mode" in info):
        print(f" - Operating mode: {info["mode"]}")
    if("averaging" in info):
        print(f" - Averaging mode: {info["averaging"]} samples")
    if("conversion_cycle" in info):
        print(f" - Conversion cycle time: {info["conversion_cycle"]} ms")
    if("alert_config" in info):
        print(" - Alert configuration:")
        print(f"   - Therm/Alert mode: {"Therm" if info["alert_config"].get("therm_mode") else "Alert"}")
        print(f"   - Alert pin polarity: {"Active high" if info["alert_config"].get("alert_polarity_high") else "Active low"}")
        print(f"   - Alert pin selection: {"Data ready flag" if info["alert_config"].get("alert_select_data_ready") else "Alert flags"}")
    if("soft_reset" in info):
        print(f" - Soft reset pending: {"Yes" if info["soft_reset"] else "No"}")

def print_tmp117_eeprom_info(info):
    if("thigh_limit" in info):
        print(f" - High temperature alert limit: {info["thigh_limit"]:.3f} °C")
    if("tlow_limit" in info):
        print(f" - Low temperature alert limit: {info["tlow_limit"]:.3f} °C")
    if("temperature_offset" in info):
        print(f" - Temperature calibration offset: {info["temperature_offset"]:.3f} °C")

    for key in ("eeprom1", "eeprom2", "eeprom3"):
        if(key in info):
            print(f" - {key.upper()}: 0x{info[key].hex()}")

    if("device_id" in info):
        dev = info["device_id"]
        print(f" - Device ID: 0x{dev["id"]:03x}")
        print(f" - Revision: {dev["rev"]}")
