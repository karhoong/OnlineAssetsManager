def base_set_up():
    import pymel.core as pm

    main_maya_window = pm.language.melGlobals['gMainWindow']

    custom_menu = pm.menu('Online Tools', parent=main_maya_window)
    pm.menuItem(label="Online Assets Manager", command="import OnlineAssetsManager.main as oam\nreload(oam)\n_oam = oam.OnlineAssetsManager()", parent=custom_menu)