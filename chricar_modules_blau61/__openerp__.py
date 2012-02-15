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


{
    'name': 'Modules Blaustauden',
    'version': '1.0',
    'category': 'Others',
    'description': """
This module installs everything for Blaustauden
""",
    'author': 'Camptocamp Austria',
    'depends': [
"account"
,"account_accountant"
,"account_analytic_analysis"
,"account_analytic_default"
,"account_anglo_saxon"
,"account_asset"
,"account_bank_statement_defaults"
,"account_chart"
#,"account_coda"
,"account_financial_report"
,"account_followup"
,"account_invoice_layout"
,"account_invoice_webkit"
,"account_payment"
,"account_payment_customer_data"
,"account_payment_edifact"
#,"account_payment_extension"
,"account_payment_sepa"
,"account_voucher"
,"analytic"
,"analytic_hours_block"
,"analytic_user_function"
,"audittrail"
,"base"
,"base_action_rule"
,"base_calendar"
,"base_contact"
,"base_iban"
,"base_ordered"
,"base_report_creator"
,"base_report_designer"
,"base_setup"
,"base_tools"
,"base_vat"
,"board"
,"c2c_account_closing_remarks"
,"c2c_account_interest"
,"c2c_account_payment_extension"
,"c2c_account_tax_rounding"
,"c2c_austria_base"
,"c2c_budget"
,"c2c_iban_formatter"
,"c2c_managment_board"
,"c2c_partner_address_label"
,"c2c_period_yyyymm"
,"c2c_product_price_unit"
,"c2c_project_timesheet"
,"c2c_real_estate"
,"c2c_reporting_tools"
,"c2c_sale_multi_partner"
,"c2c_stock"
,"c2c_stock_accounting"
,"c2c_stock_extension"
,"c2c_stock_negative"
,"c2c_stock_track_internal"
,"caldav"
,"chricar_account_analytic"
,"chricar_account_move_line_deloitte"
,"chricar_account_move_line_igel"
,"chricar_account_period_sum"
,"chricar_bank_vat"
,"chricar_budget"
,"chricar_budget_compare"
,"chricar_crm_helpdesk"
,"chricar_equipment"
,"chricar_invoice"
,"chricar_liquidity_plan"
,"chricar_partner_id_number"
,"chricar_partner_parent_companies"
,"chricar_product_gtin"
,"chricar_product_image"
,"chricar_room"
,"chricar_sale_internal_shippment"
,"chricar_stock_care"
,"chricar_stock_dispo_production_V1"
,"chricar_stock_location_product_limited"
,"chricar_stock_partner_stat"
,"chricar_stock_product_by_location"
,"chricar_stock_product_production"
,"chricar_stock_weighing"
,"chricar_stocklocation_moves"
,"chricar_tenant"
,"chricar_tools_migrate"
,"chricar_top"
,"chricar_view_id"
,"constraint"
,"crm"
,"crm_caldav"
,"crm_claim"
,"crm_fundraising"
,"crm_helpdesk"
,"crm_profile_c2c"
,"crm_profiling"
,"crm_todo"
,"decimal_precision"
,"delivery"
,"document"
,"document_ftp"
,"document_ics"
,"document_webdav"
,"edi"
,"email_template"
,"fetchmail"
,"fetchmail_crm"
,"fetchmail_project_issue"
,"hr"
,"hr_attendance"
,"hr_contract"
,"hr_evaluation"
,"hr_expense"
,"hr_holidays"
,"hr_payroll"
,"hr_payroll_account"
,"hr_recruitment"
,"hr_timesheet"
,"hr_timesheet_invoice"
,"hr_timesheet_invoice_create_ext"
,"hr_timesheet_print"
,"hr_timesheet_sheet"
,"import_base"
,"import_sugarcrm"
,"knowledge"
,"mail"
,"marketing"
,"marketing_campaign"
,"mrp"
,"mrp_jit"
,"multi_company"
,"outlook"
,"pad"
#,"point_of_sale"
,"portal"
,"process"
,"procurement"
,"product"
,"product_margin"
,"project"
,"project_billing_utils"
,"project_caldav"
,"project_gtd"
,"project_indicators"
,"project_issue"
,"project_issue_sheet"
,"project_messages"
,"project_mrp"
,"project_planning"
,"project_timesheet"
,"purchase"
,"purchase_requisition"
,"remove_duplicate"
,"report_crm_helpdesk"
,"report_designer"
,"report_intrastat"
,"report_production_order_badges"
,"report_webkit"
,"report_webkit_c2c_templates"
,"report_webkit_chapter_server"
,"resource"
,"sale"
,"sale_crm"
,"sale_journal"
,"sale_layout"
,"sale_margin"
,"sale_margin_invoice_rel"
,"sale_mrp"
,"sale_order_dates"
,"sale_shipped_rate"
,"server_environment_files"
,"share"
,"stock"
,"stock_location"
,"stock_location_product_not_null"
,"stock_picking_webkit"
,"stock_product_zero"
,"survey"
,"table_generate_csv"
,"table_generate_xml"
,"thunderbird"
,"warning"
,"web"
,"web_calendar"
,"web_dashboard"
,"web_diagram"
,"web_gantt"
,"web_graph"
,"web_kanban"
,"web_mobile"
,"web_tests"
,"wiki"
,"wiki_faq"
,"wiki_object"
,"wiki_quality_manual"
,"wiki_sale_faq"
,"xml_export_data"
,"xml_template"
     ],
    'update_xml': [       ],
    #'update_xml': ['product_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
