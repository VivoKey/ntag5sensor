def print_system_info(info):
    print(f" - Unique identifier (UID): {info['uid'].hex()}")
    if("afi" in info):
        print(f" - Application family identifier (AFI): 0x{info['afi']['family']:01x}, sub 0x{info['afi']['sub_family']:01x}")
    if("dsfid" in info):
        print(f" - Data storage identifier (DSFID): 0x{info['dsfid']:02x}")
    if("blocksize" in info):
        print(f" - Size of a memory block: {info['blocksize']} bytes")
    if("numblocks" in info):
        print(f" - Number of memory blocks: {info['numblocks']}")
    if("memory" in info):
        print(f" - Total amount of memory: {info['memory']} bytes")
    if("icref" in info):
        print(f" - IC manufacturer reference: 0x{info['icref']:02x}")

def print_extended_system_info(info):
    print_system_info(info)
    if("moi" in info):
        print(f" - Memory addressing mode (MOI): {'2-byte' if(info['moi'] == 1) else '1-byte'}")
    if("cmdlist" in info):
        print(" - Supported Commands:")
        for command, supported in info["cmdlist"].items():
            print(f"   - {command.replace('_', ' ')}: {supported}")
    if("csi" in info):
        print(" - Cryptographic suite identifier (CSI) list:")
        for csi in info["csi"]:
            print(f"   - Class: {csi['class']}, ID: {csi['id']}")

def print_nxp_system_info(info):
    if("pp_pointer" in info):
        print(f" - Protection pointer (PP): 0x{info['pp_pointer']:02x}")
    if("pp_condition" in info):
        print(" - Protection pointer condition flags:")
        for name, flag in info["pp_condition"].items():
            print(f"   - {name.replace('_', ' ')}: {flag}")
    if("lock_bits" in info):
        print(" - Lock bits:")
        for name, flag in info["lock_bits"].items():
            print(f"   - {name.replace('_', ' ')}: {flag}")
    if("features" in info):
        print(" - Feature flags:")
        for key, val in info["features"].items():
            print(f"   - {key.replace('_', ' ')}: {val}")
    if("extended_feature_flags_raw" in info):
        print(f" - Extended feature flags: {info['extended_feature_flags_raw'].hex()}")

def print_config_info(info):
    if ("auto_standby_mode_enabled" in info):
        print(f"   - Auto standby mode enabled: {info['auto_standby_mode_enabled']}")
    if ("lock_session_register" in info):
        print(f"   - Session register locked: {info['lock_session_register']}")
    if ("energy_harvesting_mode" in info):
        print(f"   - Energy harvesting mode: {info['energy_harvesting_mode']}")

    if ("pt_transfer_direction" in info):
        print(f"   - Pass-through transfer direction: {info['pt_transfer_direction']}")
    if ("sram_enabled" in info):
        print(f"   - SRAM enabled: {info['sram_enabled']}")
    if ("arbiter_mode" in info):
        print(f"   - Arbiter mode: {info['arbiter_mode']}")
    if ("use_case" in info):
        print(f"   - Use case configuration: {info['use_case']}")
    if ("eh_arbiter_mode_enabled" in info):
        print(f"   - EH arbiter mode enabled: {info['eh_arbiter_mode_enabled']}")

    if ("gpio0_slew_rate" in info):
        print(f"   - GPIO0 slew rate: {info['gpio0_slew_rate']}")
    if ("gpio1_slew_rate" in info):
        print(f"   - GPIO1 slew rate: {info['gpio1_slew_rate']}")
    if ("lock_block_command_supported" in info):
        print(f"   - Lock block command supported: {info['lock_block_command_supported']}")
    if ("extended_commands_supported" in info):
        print(f"   - Extended commands supported: {info['extended_commands_supported']}")
    if ("gpio0_pad_in" in info):
        print(f"   - GPIO0 pad input mode: {info['gpio0_pad_in']}")
    if ("gpio1_pad_in" in info):
        print(f"   - GPIO1 pad input mode: {info['gpio1_pad_in']}")
