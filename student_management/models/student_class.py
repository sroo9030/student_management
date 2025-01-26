# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,Warning


class StudentClass(models.Model):
    _name = 'student.class'
    _description = 'class'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    cid = fields.Char(string="ID")
    class_id = fields.Char(required=True, string="Class")
    active = fields.Boolean("Active", default=True)
    class_line_ids = fields.One2many('student.class.line', 'line_id')
    tag = fields.Many2many('student.tag', string="Tags")



class StudentClassLine(models.Model):
    _name = 'student.class.line'

    line_id = fields.Many2one('student.class')
    course_id = fields.Many2one('course.course')
    teacher = fields.Many2many('teacher.teacher', required=True, string="Teacher")
    schedule = fields.Datetime(required=True, string="Schedule")
    location = fields.Selection([('classroom', 'Classroom'), ('virtual', 'Virtual')], required=True, string="Location")
    platform = fields.Char(string="Platform")
    date = fields.Date(string='Exam dates', required=True)
    