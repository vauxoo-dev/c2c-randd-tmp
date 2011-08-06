# -*- coding: utf-8 -*-
{
     "name"         : "Account Moves Igel",
     "version"      : "1.0",
     "author"       : "ChriCar Beteiligungs- und Beratungs GmbH",
     "website"      : "http://www.chricar.at",
     "description"  : """Import table for account move lines of Igel""",
     "category"     : "Client Modules/ChriCar Addons",
     "depends"      : ["base","account"],
     "init_xml"     : [],
     "demo_xml"     : [],
     "update_xml"   : ["account_move_line_igel_view.xml","security/rule.xml","security/ir.model.access.csv"],
     "active"       : False,
     "installable"  : True
}

