# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,Warning


class CommonBase(models.AbstractModel):
    _name = 'common.base'
    _description = 'Common Base Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(required=True, string="Name")
    num = fields.Char( string="ID")
    email = fields.Char(string="Email")
    address = fields.Char(string="Address")
    phone = fields.Char(string="Phone")
    birth_d = fields.Date(string="Date of birth")
    nationality = fields.Many2one('res.country', string="Nationality")
    age = fields.Integer(compute = "_compute_age", store = True)
    active = fields.Boolean("Active", default=True)

    @api.depends('birth_d')
    def _compute_age(self):
        for student in self:
            if student.birth_d:
                birth_date = datetime.strptime(str(student.birth_d), "%Y-%m-%d").date()
                today = datetime.now().date()
                age = relativedelta(today, birth_date).years
                student.age = age
            else:
                student.age = 0
