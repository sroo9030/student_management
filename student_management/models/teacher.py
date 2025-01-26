# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,Warning


class Teacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'teacher'
    _inherit = 'common.base'

    image_1920 = fields.Image(store=True)
    email = fields.Char(required=True, string="email")
    subject = fields.Char(required=True, string="Subject")
    tag = fields.Many2many('student.tag', string="Tags")
    experience = fields.Float(string="Years of Experience")
    document_count = fields.Integer('Document Count', compute='_compute_document_count')
    

    def _compute_document_count(self):
        read_group_var = self.env['documents.document']._read_group(
            [('name', 'in', self.ids)],
            fields=['name'],
            groupby=['name'])

        document_count_dict = dict((d['name'][0], d['name_count']) for d in read_group_var)
        for record in self:
            record.document_count = document_count_dict.get(record.id, 0)

    def action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'domain': [('name', '=', self.id)],
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'context': {
                "default_name": self.id,
                "searchpanel_default_folder_id": False
            },
        }