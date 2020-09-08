# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TempMap
                                 A QGIS plugin
 Test
                             -------------------
        begin                : 2017-04-22
        copyright            : (C) 2017 by Thomas
        email                : thomasgardes.31@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load TempMap class from file TempMap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .temp_map import TempMap
    return TempMap(iface)
