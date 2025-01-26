# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,Warning


class Staff(models.Model):
    _name = 'staff.staff'
    _description = 'staff'
    _inherit = 'common.base'

    position = fields.Char(required=True, string="Position")
    salary = fields.Float(string="Salary")
    tag = fields.Many2many('student.tag', string="Tags")
    
