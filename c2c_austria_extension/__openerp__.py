# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2012 Camptocamp (<http://www.camptocamp.at>)
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


{
    'name': 'Camptocamp Extra Addons',
    'version': '1.0',
    'category': 'Others',
    'description': """
This module installs everything we need for Austrian extra addons c2c_extension
""",
    'author': 'Camptocamp',
    'depends': [
"c2c_austria_base"
,"c2c_partner_address_label"
,"c2c_sequence_fy"
,"c2c_process"
,"c2c_iban_formatter"
,"c2c_account_line_change"
,"c2c_account_interest"
,"c2c_account_tax_rounding"
,"c2c_budget"
,"c2c_managment_board"
,"c2c_period_yyyymm"
,"c2c_product_price_unit"
,"c2c_reporting_tools"
,"c2c_stock_accounting"
,"c2c_stock_negative"
,"c2c_stock_track_internal"
,"account_analytic_analysis"
,"account_analytic_default"
#,"account_asset"
#,"account_reporting"
#,"account_simulation"
,"analytic_journal_billing_rate"
,"analytic_user_function"
,"account_financial_report"
#,"account_payment_extension"
#,"account_report"
,"audittrail"
,"base_contact"
,"document_ics"
,"pad"
,"project_caldav"
,"project_issue"
,"project_issue_sheet"
,"project_mailgate"
,"project_messages"
,"project_planning"
,"project_timesheet"
#,"project_contact"
,"chricar_account_analytic"
,"chricar_account_period_sum"
,"chricar_crm_helpdesk"
,"chricar_partner_id_number"
,"chricar_partner_parent_companies"
,"chricar_product_gtin"
,"chricar_product_image"
,"chricar_stock_location_product_limited"
,"chricar_stock_partner_stat"
,"stock_location"
,"chricar_partner_layout"
],
    'update_xml': [],
    #'update_xml': ['product_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
