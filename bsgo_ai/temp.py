PLAYER_STATUS = "MINING"

def player_status_detection():
    combat_log = text_from_image(zone_du_jeu_a_observer_combat_log)
    sector = text_from_image(zone_du_jeu_a_observer_sector)
    if "deals damage to you" in combat_log:
        PLAYER_STATUS = "IN COMBAT"
    if "killed you" in combat_log:
        PLAYER_STATUS = "KILLED"
    if sector is False:
        PLAYER_STATUS = "IN BASE"

def status():
    while True:
        if PLAYER_STATUS == "MINING":
            main()
        if PLAYER_STATUS == "IN COMBAT":
            combat()
        if PLAYER_STATUS == "KILLED":
            killed_procedure()
        if PLAYER_STATUS == "IN BASE":
            repair()
            undock()
        if PLAYER_STATUS == "JUMPING":
            jump()

        player_status_detection()
