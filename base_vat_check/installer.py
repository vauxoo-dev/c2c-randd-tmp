# -*- coding: utf-8 -*-
##############################################
#
# Swing Entwicklung betrieblicher Informationssysteme GmbH
# (<http://www.swing-system.com>)
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
#    22-JUN-2013 (GK) created
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
# Service Company.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/> or
# write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1.17, USA.
#
###############################################
from osv import fields, osv
from tools.translate import _
import os
from suds.client import Client
from suds.transport.http import HttpTransport as SudsHttpTransport

class WellBehavedHttpTransport(SudsHttpTransport):
    def u2handlers(self): return []
    
class base_vat_installer(osv.osv_memory):
    _name    = 'res.partner.base_vat.installer'
    _inherit = 'res.config.installer'

    def execute(self, cr, uid, ids, context=None):
        self.execute_simple(cr, uid, ids, context)
        super(base_vat_installer, self).execute(cr, uid, ids, context=context)
    # end def execute

    def execute_simple(self, cr, uid, ids, context=None) :
        if not self.pool.get('res.users').browse(cr, uid, uid).company_id.vat_check_vies :
            return
        partner_obj = self.pool.get('res.partner')
        import logging ######
        _logger = logging.getLogger(__name__) #####
#        proxy = {}
#        http  = os.environ.get("HTTP_PROXY")  or os.environ.get("http_proxy")
#        https = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
#        if http  : proxy["http"]  = http
#        if https : proxy["https"] = https
#        _logger.info(str(proxy)) #####
        client = Client("http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl", transport=WellBehavedHttpTransport())
        _logger.info(str(client)) ##########
        for partner in partner_obj.browse(cr, uid, partner_obj.search(cr, uid, [("vat", "!=", None)])) :
            vat = partner.vat.replace(" ", "")
            _logger.info("Checking UID: %s" % vat) ########
            code   = vat[:2]
            number = vat[2:]
            try:
                res = client.service.checkVat(countryCode=code, vatNumber=number)
                check = bool(res["valid"])
                if check :
                    vals = \
                        { 'vat_method'        : 'vies'
                        , 'vat_check_date'    : res["requestDate"]
                        , 'vat_check_name'    : res["name"]
                        , 'vat_check_address' : res["address"]
                        , 'vat'               : vat
                        }
                    partner_obj.write(cr, uid, [partner.id], vals)
            except:
                raise osv.except_osv(_('VIES Error'), _('General Error: either connection timeout or VAT-syntax error "%s"') % vat)
    # end def execute_simple
# end class base_vat_installer
base_vat_installer()

