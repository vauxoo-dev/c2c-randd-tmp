# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2012 Camptocamp Austria (<http://www.camptocamp.at>)
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
import time
from osv import fields, osv
from tools.translate import _
import logging
import one2many_sorted
import decimal_precision as dp
import time as tm

class sale_order(osv.osv):
    _inherit = "sale.order"
  
    _columns = {
        'categ_id': fields.many2one('product.category','Category', help="Select category to be displayed"),
        'order_line_portal_sorted' : one2many_sorted.one2many_sorted
              ( 'sale.order.line'
              , 'order_id'
              , 'Product to Order'
              , states={'draft': [('readonly', False)]}
              , order  = 'categ_id.name , product_id.name'
              ),
        'order_line_portal_ordered_sorted' : one2many_sorted.one2many_sorted
              ( 'sale.order.line'
              , 'order_id'
              , 'Ordered Products'
              , search = [('product_uom_qty','!=',0)]
              , states={'draft': [('readonly', False)]}
              , order  = 'categ_id.name , product_id.name'
              ),
        }

    def get_order_lines(self, cr, uid, ids, context=None):
        prod_obj = self.pool.get('product.product')
        so_line_obj = self.pool.get('sale.order.line')
        fp = self.pool.get('account.fiscal.position')

        product_ids = prod_obj.search(cr, uid, [('display_portal_ok','=',True)])
        for order in self.browse(cr,uid,ids,context):
            fpos = order.partner_id.property_account_position.id
            ordered_product_ids = []
            for ordered in order.order_line:
                ordered_product_ids.append( ordered.product_id.id)
            t_tot = 0
            t_count = 0
            for product in prod_obj.browse(cr,uid,product_ids):
              if product.id not in ordered_product_ids:
                p = product.name
                vals = {
                       'order_id' : order.id,
                       'product_id': product.id,
                       'name' : p,
                       'product_uom': product.uom_id.id,
                       'product_uom_qty' : 0,
                       'price_unit': product.list_price,
                       'type': product.procure_method,
                       'product_packaging' : product.packaging and product.packaging[0].id or '',
                       'content_qty' : product.packaging and product.packaging[0].qty or 1.0,
                       'state' : 'draft',
                       'delay': 0.0,
                       'tax_id' : [(6, 0, fp.map_tax(cr, uid, fpos, product.taxes_id))],
                       }
                vals_sql = {
                       'order_id' : order.id,
                       'product_id': product.id,
                       'name' : '\''+p+'\'',
                       'product_uom': product.uom_id.id,
                       'product_uom_qty' : 0,
                       'price_unit': product.list_price,
                       'type': '\''+product.procure_method+'\'',
                       'product_packaging' : product.packaging and product.packaging[0].id or 'null',
                       'content_qty' : product.packaging and product.packaging[0].qty or 1.0,
                       'state' : '\''+'draft'+'\'',
                       'delay': 0.0,
                       }
                # the following statement takes 120 seconds to insert 400 rows
                
                t1 = tm.time()
                so_line_obj.create(cr, 1, vals)
                t_tot += tm.time() - t1
                t_count += 1
                 
                # the following statement takes 2 seconds to insert 400 rows
                #cr.execute("""
                #insert into
                #sale_order_line(order_id,product_id,name,product_uom,product_uom_qty,price_unit,type,product_packaging,content_qty,state,delay)
                #values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)""" % (
                #        vals['order_id'],
                #        vals['product_id'],
                #        vals['name'],
                #        vals['product_uom'],
                #        vals['product_uom_qty'],
                #        vals['price_unit'],
                #        vals['type'],
                #        vals['product_packaging'],
                #        vals['content_qty'],
                #        vals['state'],
                #        vals['delay'],
                #        )
                #)
            
            _logger  = logging.getLogger(__name__)
            _logger.debug('FGF create count %s time %s avg %s '
                    %(t_count,t_tot*1000.0, t_tot*1000.0/t_count)   )


    def rm_zero_lines(self, cr, uid, ids, context=None):
        so_line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr,uid,ids,context):
            line_ids = so_line_obj.search(cr, uid , [('order_id','=',order.id),('product_uom_qty','=',0)])
            so_line_obj.unlink(cr, uid, line_ids)

sale_order()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _columns = {
         'categ_id'       : fields.related('product_id','categ_id',type="many2one", relation="product.category", string='Category',readonly=True),
         'code'           : fields.related('product_id','code',type="varchar", string='Code',readonly=True),
         'product_pack_qty_helper': fields.float('Package #' ,digits_compute= dp.get_precision('Product UoS'), readonly=True, states={'draft': [('readonly', False)]}),
        }

    def product_pack_helper_change(self, cr, uid, ids,pack_helper_qty, content_qty, 
            pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                        lang=False, update_tax=True, date_order=False,
                        packaging=False, fiscal_position=False, flag=False,
                        context=None):
        
        qty = round(pack_helper_qty * content_qty,0)
        res = super(sale_order_line, self).product_id_change(cr,uid, ids, 
            pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
                        lang, update_tax, date_order,
                        packaging, fiscal_position, flag,
                        context)

        res['value']['qty'] = qty

        return res

sale_order_line()

class product_template(osv.osv):
    _inherit = "product.template"
    _columns = {
        'display_portal_ok': fields.boolean('Display in Partner Portal', help="Determines if the product can be visible in the list of product within a selection from a sale order line."),
    }
product_template()

