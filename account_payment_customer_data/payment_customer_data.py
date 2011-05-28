# -*- coding: utf-8 -*-
##############################################
#
# Swing Entwicklung betrieblicher Informationssysteme GmbH
# (<http://www.swing-system.com>)
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
#    20-APR-2011 (GK) created
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
from osv import fields, osv
from tools.translate import _

class account_invoice(osv.osv) :
    _inherit = "account.invoice"

    _columns = \
        {'customer_data' : fields.char
            ( 'Customer Data'
            , size=12
            , help="""Numeric field used for electronic banking.\nContains number specified by the recipient."""
            )
        }

    def _check_reference(self, cr, uid, ids):
        for invoice in self.browse(cr, uid, ids):
            if invoice.type in ("in_invoice","in_refund") and invoice.state == "open" :
                if not invoice.reference : return False
        return True
    # end def _check_reference

    def _check_customer_data(self, cr, uid, ids):
        for invoice in self.browse(cr, uid, ids):
            if invoice.customer_data and invoice.type == "in_invoice" : #  and invoice.state == "open":
                if not invoice.customer_data.isdigit() : return False
        return True
    # end def _check_customer_data

    _constraints = \
        [ (_check_customer_data, _('Error: Invalid "Customer Data" [numeric12]'), ['customer_data'])
        , (_check_reference, _('Error: "Reference" is missing'), ['reference'])
        ]
account_invoice()
