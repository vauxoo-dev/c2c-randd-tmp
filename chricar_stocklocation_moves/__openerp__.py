# -*- coding: utf-8 -*-
{ "name"         : "chricar_stocklocation_moves"
, "version"      : "0.1"
, "author"       : "ChriCar Beteiligungs- und Beratungs GmbH"
, "category"     : "Warehouse Management"
, "depends"      : ["c2c_stock_accounting"]
, "init_xml"     : []
, "update_xml"   : ["stocklocation_move.xml","stock_report.xml","security/ir.model.access.csv","wizard/stock_location_product_view.xml"]
, "auto_install" : False
, "installable"  : True
, 'application'  : False
, "description"  : """Analysis of moves per location

(Group by Category is broken - related field)
"""
}
