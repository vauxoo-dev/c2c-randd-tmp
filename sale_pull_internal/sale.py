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
import pooler
import time
from osv import fields, osv
from tools.translate import _
import netsvc
import logging

class stock_location(osv.osv):
    _inherit = "stock.location"

    _columns = {
        'sequence': fields.integer('Sequence', help="Important when pull pickings are create, the execution order will be decided based on this, low number is higher priority."),
    }

stock_location()

class sale_order(osv.osv):
    _inherit = "sale.order"
    

    _columns = {
        'state_internal': fields.selection([('', 'Unused'), ('calculation', 'Calculation'), ('calculated', 'Calculated')], 'Internal Pull Calcualtion', \
                help="This indicates the status of the internal pull calculation"),
    }


    def order_pull_internal(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        _logger = logging.getLogger(__name__)
        
        product_obj = self.pool.get('product.product')
        location_obj = self.pool.get('stock.location')
        picking_obj = self.pool.get('stock.picking')
        move_obj = self.pool.get('stock.move')
        company_obj = self.pool.get('res.company')

        if not context.get('company_id'):
            company_id = res_company._company_default_get(cr, uid, 'stock.company', context=context),
            context['company_id'] = company_id

        order_ids =[]

        move_lines = []
        back_log_lines = []
        loc_ids = []
        for order in self.browse(cr, uid, ids, context):
            if not order.state_internal and order.state == 'progress':
                order_ids.append(order.id)
        # FIXME uncomment# order.write(cr, uid, order_ids,{'state_internal':'calculation'} )

        order_ids2 = (', '.join(map(str,order_ids)))
        cr.execute("""select product_id, sum(product_uom_qty) as qty_requested
                   from sale_order_line
                  where order_id in (%s)
                  group by product_id""" % order_ids2)
        for product_qty in cr.dictfetchall():
            _logger.info('FGF sale pull internal %s' % (product_qty))
            product_id = product_qty['product_id']
            qty_requested = product_qty['qty_requested']
            cr.execute("""select id
                   from stock_location
                  where sequence is not null
                  order by sequence""") 
            for loc in cr.fetchall():
                _logger.info('FGF sale location %s ' % (loc))
                location_id = loc[0]
                context['location_id'] = loc[0]
                _logger.info('FGF sale location id %s ' % (context))
                qty_avail = product_obj.get_product_available(cr, uid, product_id , context)
                _logger.info('FGF sale location product %s %s ' % (product_id, qty_avail))
                if qty_avail > qty_requested:
                    qty_requested = 0.0
                    move_lines.append({'location_id':location_id, 'product_id': product_id, 'product_qty':qty_requested })
                    if location_id not in loc_ids:
                        loc_ids.append(location_id)
                else
                    qty_requested = qty_requested - qty_avail
                    move_lines.append({'location_id':location_id, 'product_id': product_id, 'product_qty':qty_avail })
                    if location_id not in loc_ids:
                        loc_ids.append(location_id)
            if qty_requested > 0.0:
                back_log_lines.append({'product_id': product_id, 'product_qty':qty_requested})

            
        # now we create a stock_picking for each location
        pick_vals = {
                'name': '/',
                'origin': _('auto Pull Picking'),
                'type' : 'internal',
                'move_type' : 'direct',
                'invoice_state': 'none',
                'state': 'draft',
                'date-done': time.strftime('%Y-%m-%d %H:%M:%S'),
                #'stock_journal_id': stock_journal_id #FIXME do not know where this comes from
                }
                
        move_vals = {
                'location_dest_id' : 
                }

        for loc in loc_ids:
            pick = pick_vals
            address_id = location_obj.read(cr,uid,loc)[address_id]
            if address_id:
                pick['address_id'] = address_id
            # FIXME add the move lines for this location
            stock_moves = move_vals
            stock_moves['location_id'] = loc[0]
            
            for l in move_lines:
                line = dict(l)
                if line['location_id'] = loc[0]
                    ml = {
                       'product_id' : line['product_id']
                       'product_uom' : product_obj.read(cr, uid, line['product_id'])['uom_id'][0]
                       'product_qty' : line['product_qty']
                       }
                stock_moves['product_id'] = 
            pick['vals'] = stock_moves
            picking_id = picking_obj.create(cr, uid, pick, context=context))

        if back_log_lines:
            _logger.info('FGF back_log lines %s ' % (back_log_lines))
            # FIXME - must write an internal pick

        # FIXME uncomment# order.write(cr, uid, order_ids,{'state_internal':'calculated'} )

        return


sale_order()

class sale_order_pull_internal(osv.osv_memory):
    _name = "sale.order.pull.internal"
    _description = "Create Pull Pickings"
    _columns = {
        'dummy': fields.boolean('Dummy', help='Check the box to group the invoices for the same customers'),
    }
    _defaults = {
        'dummy': False
    }

    def view_init(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False)
        order = self.pool.get('sale.order').browse(cr, uid, record_id, context=context)
        if order.state != 'progress':
            raise osv.except_osv(_('Warning !'),'You can only internal pull pickings from SO in progres.')
        return False


    def make_picking_internal(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('sale.order')
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        new_pick = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        order_obj.order_pull_internal(cr, uid, context.get(('active_ids'), []), )

#        wf_service = netsvc.LocalService("workflow")
#        for id in context.get(('active_ids'), []):
#            wf_service.trg_validate(uid, 'sale.order', id, 'manual_invoice', cr)
#
#        for o in order_obj.browse(cr, uid, context.get(('active_ids'), []), context=context):
#            for i in o.invoice_ids:
#                newinv.append(i.id)
#
        result = mod_obj.get_object_reference(cr, uid, 'stock', 'action_picking_tree6')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
#        result['domain'] = "[('id','in', ["+','.join(map(str,newinv))+"])]"

        return result


            
sale_order_pull_internal()

