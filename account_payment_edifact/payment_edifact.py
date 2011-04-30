# -*- coding: utf-8 -*-
##############################################
#
# Swing Entwicklung betrieblicher Informationssysteme GmbH
# (<http://www.swing-system.com>)
# Copyright (C) ChriCar Beteiligungs- und Beratungs- GmbH
# all rights reserved
#    05-AUG-2010 (GK) created
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs.
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
###############################################
from osv import fields, osv
from tools.translate import _
import os
import time
import unicode2ascii
import base64

class payment_type(osv.osv) :
    _inherit = "payment.type"
    # http://www.unece.org/trade/untdid/d00a/tred/tred4471.htm
    _columns = \
        { 'charges_alloc' : fields.selection
            ([ ( '1', 'Bill back')
             , ( '2', 'Off invoice')
             , ( '3', 'Vendor check to customer')
             , ( '4', 'Credit customer account')
             , ( '5', 'Charge to be paid by vendor')
             , ( '6', 'Charge to be paid by customer')
             , ( '7', 'Optional')
             , ( '8', 'Off gross quantity invoiced')
             , ( '9', 'Electric cost recovery factor')
             , ('10', 'Gas cost recovery factor')
             , ('11', 'Prior credit balance')
             , ('12', 'Non-dutiable')
             , ('13', 'All charges borne by payee')
             , ('14', 'Each pay own cost')
             , ('15', 'All charges borne by payor')
             , ('16', 'All bank charges to be borne by applicant')
             , ('17', 'All bank charges except confirmation commission to be borne by applicant')
             , ('18', 'All bank charges to be borne by beneficiary')
             , ('20', 'Amendment charges to be borne by applicant')
             , ('21', 'Amendment charges to be borne by beneficiary')
             , ('22', 'Discount charges to be borne by applicant')
             , ('23', 'Discount charges to be borne by beneficiary')
             , ('24', 'All bank charges other than those of the issuing bank to be borne by beneficiary')
             , ('25', 'Amendment charges other than those of the issuing bank to be borne by beneficiary')
             , ('26', 'All charges to be paid by the principal of the collection')
             , ('27', 'All charges to be paid by the drawee of the collection')
             , ('28', 'All charges to be borne by the drawee except those levied by the remitting bank, to be paid by principal')
             , ('29', 'All bank charges are to be paid by the principal of the documentary credit collection')
             , ('30', 'All bank charges to be borne by receiving bank')
             , ('31', 'All bank charges to be borne by sending bank')
             , ('32', 'Charges levied by a third bank')
             , ('33', 'Information charges levied by a third bank')
             , ('34', 'Total payment borne by patient')
             , ('35', 'Part payment borne by patient')   
             , ('ZZZ', 'Mutually defined')
             ]
            , 'Financial Charges Allocation'
            )
        }
    _defaults = {'charges_alloc'    : lambda *a: '14'}
# end class payment_type
payment_type()

class payment_order(osv.osv) :
    _inherit = "payment.order"

    def _address(self, partner, type_list):
        for type in type_list :
            for addr in partner.address :
                if addr.type == type :
                    return addr
        raise osv.except_osv \
            ( _('Data Error !')
            , _('Partner "%s" has no address defined.')
                % (partner.name)
            )
    # end def _address

    def _invoice_customer_data(self) :
        invoice_obj = self.pool.get('account.invoice')
        return invoice_obj._columns.has_key("customer_data")
    # end def _invoice_customer_data

    def _u2a(self, text) :
        if not text : return ""
        txt = ""
        for c in text:
            if ord(c) < 128 : txt += c
            elif c in unicode2ascii.EXTRA_LATIN_NAMES : txt += unicode2ascii.EXTRA_LATIN_NAMES[c]
            elif c in unicode2ascii.UNI2ASCII_CONVERSIONS : txt += unicode2ascii.UNI2ASCII_CONVERSIONS[c]
            elif c in unicode2ascii.EXTRA_CHARACTERS : txt += unicode2ascii.EXTRA_CHARACTERS[c]
            elif c in unicode2ascii.FG_HACKS : txt += unicode2ascii.FG_HACKS[c]
            else : txt+= "_"
        return txt
    # end def _u2a

    def _strip(self, text) :
        result = text
        txt = "/.+:'"
        for c in txt:
            result = result.replace(c, "")
        return result
    # end def _strip

    def action_open(self, cr, uid, ids, *args):
        result = True
        result = super(payment_order, self).action_open(cr, uid, ids, args)
        self.generate_edifact(cr, uid, ids, {})
        return result
    # end def action_open
    
    def get_wizard(self, type):
        return False
    # end def get_wizard

    def _line(self, l, interntl) :
        s = []
        s.append("SEQ++%(seq)s'" % l)
        s.append("MOA+9:%(amount)s:%(currency)s'" % l)
        if l['move_name'] :
            s.append("RFF+PQ:%(move_name)s'" % l)
        if l['customer_data'] :
            s.append("RFF+AEF:%(customer_data)s'" % l)
        if interntl :
            s.append("FCA+%(fca)s'" % l)
            s.append("FII+BF+%(iban)s:%(name)s+%(bic)s:25:5'" % l)
        else :
            s.append("FII+BF+%(account)s:%(name)s+%(blz)s:25:137+%(bank_country)s'" % l) # sgr12
        s.append("NAD+BE+++%(name)s+%(street)s+%(city)s+%(zip)s+%(country)s'" % l) # sgr3
        s.append("PRC+11'")
        s.append("FTX+PMD+++%(reference)s'" % l)
        return s
    # end def _line
    
    def _region(self, order, banks, i, area_code):
        partner_bank_obj = self.pool.get('res.partner.bank')
        s = []
        for p_bank, lines in banks.iteritems() :
            if p_bank.state == "iban"  :
                iban    = p_bank.iban.replace(" ", "").upper()
                account = p_bank.acc_number or iban[9:] ### austria-specific!!!
            else :
                iban    = partner_bank_obj._construct_iban(p_bank)
                account = p_bank.acc_number
            bic = ''
            if p_bank.bank.bic:
                bic     = p_bank.bank.bic.replace(" ", "").upper()
            blz          = p_bank.bank.code
            bank_name    = self._u2a(p_bank.bank.name).upper()[0:70]
            bank_country = "" if not p_bank.bank.country else p_bank.bank.country.code
            if [l for l in lines if l.amount <= 0.0] :
                line = lines[0]
                i += 1
                a = sum(l.amount for l in lines)
                own_ref = []
                customer_ref = []
                for l in lines :
                    invoice   = l.move_line_id.invoice
                    if invoice.number :
                        invoice_number = self._u2a(self._strip(invoice.number)).upper()
                        own_ref.append(invoice_number)
                    if invoice.reference :
                        own_ref.append(self._u2a(invoice.reference).upper())
                    if l.communication != "/" :
                        customer_ref.append(self._u2a(l.communication).upper())
                    if l.communication2 :
                        customer_ref.append(self._u2a(l.communication2).upper())
                    if not customer_ref :
                        raise osv.except_osv \
                            ( _('Data Error !')
                            , _('A descriptive text for the payment is missing')
                            )
                    
                p_address = self._address(line.partner_id, ['invoice', 'default', False])
                l = \
                    { 'seq'       : "%s" % i
                    , 'amount'    : "%s" % a
                    , 'bank_name' : bank_name
                    , 'bank_country' : bank_country
                    , 'iban'      : iban
                    , 'account'   : account
                    , 'bic'       : bic
                    , 'blz'       : blz
                    , 'currency'  : line.currency.name
                    , 'move_name' : (" ".join(customer_ref))[0:35]
                    , 'customer_data' : None
                    , 'fca'       : order.mode.type.charges_alloc
                    , 'name'      : self._u2a(line.partner_id.name).upper()[0:35]
                    , 'street'    : self._u2a(p_address.street).upper()[0:35]
                    , 'city'      : self._u2a(p_address.city).upper()[0:35]
                    , 'zip'       : self._u2a(p_address.zip).upper()[0:9]
                    , 'country'   : p_address.country_id.code or ""
                    , 'reference' : (" ".join(own_ref))[0:70]
                    }
                s.extend(self._line(l, area_code == 'IN'))
            else :
                for line in lines :
                    i += 1
                    invoice   = line.move_line_id.invoice
                    own_ref = []
                    customer_ref = []
                    customer_data = None
                    if invoice.number :
                        invoice_number = self._u2a(self._strip(invoice.number)).upper()
                        own_ref.append(invoice_number)
                    if invoice.reference :
                        own_ref.append(self._u2a(invoice.reference).upper())
                    if line.communication != "/" :
                        customer_ref.append(self._u2a(line.communication).upper())
                    if line.communication2 :
                        customer_ref.append(self._u2a(line.communication2).upper())
                    if self._invoice_customer_data() and invoice.customer_data :
                        customer_data = invoice.customer_data[0:12]
                    if not (customer_ref or customer_data) :
                        raise osv.except_osv \
                            ( _('Data Error !')
                            , _('A descriptive text for the payment is missing')
                            )

                    p_address = self._address(line.partner_id, ['invoice', 'default', False])
                    l = \
                        { 'seq'       : "%s" % i
                        , 'amount'    : "%s" % line.amount
                        , 'bank_name' : bank_name
                        , 'bank_country' : bank_country
                        , 'iban'      : iban
                        , 'account'   : account
                        , 'bic'       : bic
                        , 'blz'       : blz
                        , 'currency'  : line.currency.name
                        , 'move_name' : (" ".join(customer_ref))[0:28] # smaller for AEF
                        , 'customer_data' : customer_data
                        , 'fca'       : order.mode.type.charges_alloc
                        , 'name'      : self._u2a(line.partner_id.name).upper()[0:35]
                        , 'street'    : self._u2a(p_address.street).upper()[0:35]
                        , 'city'      : self._u2a(p_address.city).upper()[0:35]
                        , 'zip'       : self._u2a(p_address.zip).upper()[0:9]
                        , 'country'   : p_address.country_id.code or ""
                        , 'reference' : (" ".join(own_ref))[0:70]
                        }
                    s.extend(self._line(l, area_code == 'IN'))
        return s
    # end def _region

    def _line_count(self, banks):
        i = 0
        for p_bank, lines in banks.iteritems() :
            if [l for l in lines if l.amount <= 0.0] :
                i += 1
            else :
                for line in lines :
                    i += 1
        return i
    # end def _line_count

    def generate_edifact(self, cr, uid, ids, context=None) :
        attachment_obj = self.pool.get('ir.attachment')
        company = self.pool.get('res.users').browse(cr, uid, uid).company_id
        currency_name = company.currency_id.name
        description = 'EDIFACT-file'
        for order in self.browse(cr, uid, ids) :
            if order.state == "cancel" : continue
            att_ids = attachment_obj.search \
                ( cr, uid
                , [ ('res_model', '=', order._table_name)
                  , ('res_id', '=', order.id)
                  , ('description', '=', description)
                  ]
                )
            if att_ids :
                attachment_obj.unlink(cr, uid, att_ids, context=context)
            ref     = self._strip(order.reference).upper()
            refkey  = ref
            refname = time.strftime("%Y%m%d%H%M%S")
            company_name = self._u2a(company.name).upper()[0:35]
            address = self._address(company.partner_id, ['invoice', 'default', False])
            country = address.country_id.code or ""
            bank    = order.mode.bank_id
            if not bank.bank.bic :
                raise osv.except_osv \
                    ( _('Data Error !')
                    , _('Bank %s has no BIC') % (bank.bank.name)
                    )
            if not bank.iban :
                raise osv.except_osv \
                    ( _('Data Error !')
                    , _('Banking Account for bank %s has no IBAN') % (bank.bank.name)
                    )
            iban    = bank.iban.replace(" ", "").upper()
            bic     = bank.bank.bic.replace(" ", "").upper()
            street  = self._u2a(address.street).upper()[0:35]
            city    = self._u2a(address.city).upper()[0:35]
            zip     = self._u2a(address.zip).upper()[0:9]
            amount  = "%s" % order.total
            regions = {'IN' : {}, 'DO' : {}}
            for line in order.line_ids :
                if not line.bank_id : 
                    raise osv.except_osv \
                        ( _('Data Error !')
                        , _('Payment for (%s) needs banking information') % (line.partner_id.name)
                        )
#                if not line.bank_id.bank.bic : 
#                    raise osv.except_osv \
#                        ( _('Data Error !')
#                        , _('Bank for (%s) needs BIC') % (line.partner_id.name)
#                        )
                if not line.move_line_id : 
                    raise osv.except_osv \
                        ( _('Data Error !')
                        , _('Payment for (%s) needs accounting information') % (line.partner_id.name)
                        )
                if line.currency != company.currency_id : 
                    raise osv.except_osv \
                        ( _('Data Error !')
                        , _('Payment contains currency (%s) different from company currency (%s).')
                            % (line.currency.name, currency_name)
                        )
                if (    line.bank_id.bank.country 
                    and bank.bank.country
                    and (line.bank_id.bank.country == bank.bank.country) 
                   ) :
                    region = "DO" # domestic
                else :
                    region = "IN" # international
                if line.bank_id not in regions[region] :
                    regions[region][line.bank_id] = [line,]
                else :
                    regions[region][line.bank_id].append(line)
            for area_code, banks in regions.iteritems() :
                for p_bank, lines in banks.iteritems() :
                    if sum(l.amount for l in lines) <= 0.0 :
                        raise osv.except_osv \
                            ( _('Data Error !')
                            , _('Payment contains a zero or negative amount for account "%s" of bank "%s".')
                                % (p_bank.acc_number, p_bank.bank.name)
                            )
            for area_code, banks in regions.iteritems() :
                if len(banks) == 0 : continue
                today = time.strftime("%Y%m%d")
                for p_bank, lines in banks.iteritems() :
                    dates = list(time.strftime("%Y%m%d", time.strptime(l.date, "%Y-%m-%d")) for l in lines if l.date)
                    if dates :
                        payment_date = min(dates)
                        payment_date = max(today, payment_date)
                    else : 
                        payment_date = today
                i = 0
                s = []
                s.append("UNA:+.? '")
                s.append("UNB+UNOC:3+%s+%s+%s:%s+%s++PAYMUL'" % (company_name, bic, time.strftime("%y%m%d"), time.strftime("%H%M"),refkey))
                s.append("UNH+%s+PAYMUL:D:96A:UN:FAT01G'" % refname)
                s.append("BGM+452+%s+9'" % ref)
                s.append("DTM+137:%s:203'" % (time.strftime("%Y%m%d%H%M%S")))
                s.append("FII+MR+%s'" % iban) # sgr2 # xxx
                s.append("NAD+MS+++%s+%s+%s++%s+%s'" % (company_name, street, city, zip, country)) # sgr3
                s.append("LIN+1'") # sgr4
                s.append("DTM+203:%s:102'" % (payment_date))
                s.append("RFF+AEK:%s'" % ref)
                s.append("BUS++%s++TRF'" % area_code)
                s.append("MOA+9:%s:%s'" % (amount, currency_name))
                s.append("FII+OR+%s:%s::%s'" % (iban, company_name, currency_name))
                s.append("NAD+OY+++%s+%s+%s+%s+%s'" % (company_name, street, city, zip, country)) # sgr3
                s.extend(self._region(order, banks, i, area_code))
                i += self._line_count(banks)
                s.append("CNT+1:%s'" % amount)
                s.append("CNT+2:1'")
                s.append("CNT+39:%s'" % i)
                t = "".join(s)
                t += ("UNT+%s+%s'" % (len(s)-1, refname))
                t += ("UNZ+1+%s'" % refkey)
                vals = \
                    { 'name'        : "%s_%s" % (area_code, ref)
                    , 'datas'       : base64.encodestring(t)
                    , 'datas_fname' : "%s_%s.txt" % (area_code, ref)
                    , 'res_model'   : order._table_name
                    , 'res_id'      : order.id
                    , 'description' : description
                    }
                attachment_obj.create(cr, uid, vals, context=context)
                print "EDIFACT ", t ####################
    # end def generate_edifact
# end class payment_order
payment_order()
