# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011 Camptocamp (<http://www.camptocamp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import fields, osv

class account_bank_statement_line(osv.osv):

    _inherit = "account.bank.statement.line"

    def _get_statement_date(self, cursor, user, ids,  context=None):
        res = {}        
        for line in self.browse(cursor, user, ids, context=context):
            if line and line.statement_id:
                res[line.id] = line.statement_id.date or ''
        return res    

    _defaults = {
        #'date': lambda self, cr, uid, context: context.get('date', False),
        'date' : '',
    }


account_bank_statement_line()