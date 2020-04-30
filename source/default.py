#-*- coding: utf-8 -*-
# Primatech.


from resources.lib.util import dialog, VSlog
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer

class main:
    def __init__(self):

        message = "Add-on: TvWatch2\n"
        message += "Repo: http://tvwatch2.000webhostapp.com/\n"
        message += "\n"
        message += "Afficher la procédure d'installation ?\n"

        if dialog().VSyesno(message, "Une nouvelle version de Tvwatch est disponible !"):

            url = 'https://www.youtube.com/watch?v=614nwd3J_x0'
            from resources.hosters.youtube import cHoster
            hote = cHoster()
            hote.setUrl(url)
            api_call = hote.getMediaLink()[1]
            if not api_call:
                return

            oGuiElement = cGuiElement()
            oGuiElement.setSiteName('youtube')
            oGuiElement.setTitle("Procédure d'installation TvWatch2")
            oGuiElement.setMediaUrl(api_call)
            oGuiElement.setThumbnail(oGuiElement.getIcon())

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()

        return
main()
