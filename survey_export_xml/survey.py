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
from osv import fields, osv

class survey(osv.osv):
    _inherit = 'survey'

    _columns = {
        'template_id' : fields.many2one('xml.template', "Template"),  
      }
      
    def survey_export_xml(self, cr, uid, ids, context=None):
        """
        XML export of the structure using a template 
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of Survey IDs
        @param context: A standard dictionary for contextual values
        @return : Dictionary value for print survey form.
        """
        if context is None:
            context = {}
        for survey in self.browse(cr, uid, ids, context):
            xml_gen_obj = self.pool.get('xml.template')
            xml = xml_gen_obj.generate_xml(cr, uid, survey.template_id.id, survey = survey, lang = survey.lang)
            #xml = xml1.replace(xml,'<headers>','').replace('<questions>','').replace(xml,'</headers>','').replace('</questions>','') 
            xml_gen_obj.attach_xml(cr, uid, survey.id  , survey , xml, 'Survey XML '+survey.lang, 'survey_'+survey.lang, description=False, pretty_print=True, context=None)
             
survey()
