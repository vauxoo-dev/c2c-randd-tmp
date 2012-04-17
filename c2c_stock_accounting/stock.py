# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2010 Camptocamp Austria (<http://www.camptocamp.at>)
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

from osv import osv, fields
import decimal_precision as dp
from tools.translate import _
import logging
#----------------------------------------------------------
#  Stock Move INHERIT
#----------------------------------------------------------
class stock_move(osv.osv):
    _inherit = "stock.move"
    _logger = logging.getLogger(_name)

    def _compute_move_value_cost(self, cr, uid, ids, name, args, context):
        if not ids : return {}
        result = {}
        for move in self.browse(cr, uid, ids):
            self._logger.debug('type cost `%s`', move.picking_id.type)
            if move.state in ['done','cancel']: return {}
            if not move.sale_line_id:
                result[move.id] = move.product_qty * move.price_unit
            else:
                loc_id = str(move.location_id.id)
                self._logger.debug('loc_id `%s`', loc_id)
                # compute avg price per stock location
                sql = 'select \
                 sum( case when location_id = '+loc_id+' then -move_value_cost else 0 end + case when location_dest_id = '+loc_id+' then move_value_cost else 0 end) as sum_amount, \
                 sum( case when location_id = '+loc_id+' then -product_qty else 0 end + case when location_dest_id     = '+loc_id+' then product_qty else 0 end) as sum_qty \
                 from stock_move \
                where product_id = '+ str(move.product_id.id) +' \
                  and state = \'done\' \
                  and (location_id = '+loc_id+' or location_dest_id = '+loc_id+')' 
                if move.prodlot_id:
                   sql = sql + ' and prodlot_id = ' + str(move.prodlot_id.id )
                self._logger.debug('sql `%s`', sql)
                cr.execute(sql)
                for r in cr.dictfetchall():
                   sum_amount = r['sum_amount']
                   sum_qty    = r['sum_qty']
                   self._logger.debug('sum `%s` `%s`', sum_amount, sum_qty)
                   if sum_qty and sum_qty > 0.0 and sum_amount > 0.0:
                       avg_price = sum_amount / sum_qty 
                       result[move.id] = move.product_qty * avg_price
                   else :
                       result[move.id] = move.product_qty * move.product_id.standard_price
                
        return result

    def _compute_move_value_sale(self, cr, uid, ids, name, args, context):
        self._logger.debug('value_sale')
        if not ids: return {}
        result = {}
        for move in self.browse(cr, uid, ids):
            if move.state in ['done','cancel']: return {}
            self._logger.debug('type sale `%s`', move.picking_id.type)
            if move.sale_line_id:
                result[move.id] = move.product_qty * move.sale_line_id.price_unit
                self._logger.debug('value_sale `%s`', result[move.id])
        return result

    def _compute_price_unit_sale(self, cr, uid, ids, name, args, context):
        self._logger.debug('value_price')
        if not ids: return {}
        result = {}
        for move in self.browse(cr, uid, ids):
            avg_price = 0.0
            if move.picking_id.type == 'out' and move.state != 'cancel' and move.product_qty and move.product_qty != 0:
                self._logger.debug('type sale `%s`', move.picking_id.type)
                avg_price = move.move_value_sale / move.product_qty 
            result[move.id] = avg_price
            self._logger.debug('value_sale `%s`', result[move.id])
        return result


    def _period_id(self, cr, uid, ids, name, arg, context):
         result = {}
         for move in self.browse(cr, uid, ids):
             #period_ids= self.pool.get('account.period').search(cr,uid,[('date_start','<=',move.date),('date_stop','>=',move.date ), ('special','=',False)])
             period_ids= self.pool.get('account.period').search(cr,uid,[('date_start','<=',move.date),('date_stop','>=',move.date )])
             
             if len(period_ids):
                 result[move.id] = period_ids[0]
             
         return result

    _columns = { 
        'move_value_cost'    : fields.function(_compute_move_value_cost, method=True, string='Amount', digits_compute=dp.get_precision('Account'),type='float' ,  store=True, \
                            help="""Product's cost for accounting valuation.""") ,
        'move_value_sale'    : fields.function(_compute_move_value_sale, method=True, string='Amount Sale', digits_compute=dp.get_precision('Account'),type='float' , store=True, \
                             help="""Product's sale value for accounting valuation.""") ,
        'period_id'          : fields.function(_period_id, method=True, string="Period",type='many2one', relation='account.period', store=True, select="1",  ),
        'price_unit_sale'    : fields.function(_compute_price_unit_sale, method=True, string='Sale Price',  digits_compute=dp.get_precision('Account') ),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),

    }


    def init(self, cr):
      # Purchase
      cr.execute("""
          update stock_move m set move_value_cost = (select m.product_qty * p.price_unit from purchase_order_line p
                                   where p.id = m.purchase_line_id) where move_value_cost is null;
      """)
      # Sales
      cr.execute("""
          update stock_move m set move_value_sale = (select m.product_qty * l.price_unit from sale_order_line l
                                   where l.id = m.sale_line_id) where move_value_sale is null;
      """)
      # other
      cr.execute("""
          update stock_move m set move_value_cost = (select m.product_qty * t.standard_price from product_product p, product_template t
                                   where p.id = m.product_id and t.id = p.product_tmpl_id) where move_value_cost is null;
      """)

stock_move()


#----------------------------------------------------------
#  Company Config INHERIT
#----------------------------------------------------------

#class res_company(osv.osv):
#    _inherit = "res.company"
#
#
#    _columns = {
#        'valuation':fields.selection([('manual_periodic', 'Periodical (manual)'),
#                                        ('real_time','Real Time (automated)'),], 'Inventory Valuation',
#                                        help="If real-time valuation is enabled for a product, the system will automatically write journal entries corresponding to stock moves." \
#                                             "The inventory variation account set on the product category will represent the current inventory value, and the stock input and stock output account will hold the counterpart moves for incoming and outgoing products."
#    }

#res_company()

## no connection from product to company !!!!
#class product_product(osv.osv):
#    _inherit = "product.product"
#
#    def _get_valuation(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         for res in self.browse(cr, uid, ids, context):
#             result[res.id] = 
#         return result
#
#
#    _columns = {
#        'valuation':  fields.function(_get_valuation, method=True, string="Valuation",type='char',size=128),
#
#    }
#
#product_product()
