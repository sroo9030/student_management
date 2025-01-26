# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,Warning


class Course(models.Model):
    _name = 'course.course'
    _description = 'course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string="Course")
    teacher = fields.Many2many('teacher.teacher', required=True, string="Teacher")
    staff = fields.Many2one('staff.staff', required=True, string="Staff")
    description = fields.Char(string="Description")
    avg_age = fields.Float(compute="compute_average_age", store=True, string="Students average age")
    active = fields.Boolean("Active", default=True)
    tag = fields.Many2many('student.tag', string="Tags")


    @api.depends('name')
    def compute_average_age(self):
        for rec in self:
            students = self.env['student.management'].search([('course_line_ids.course_id', '=', rec.name)])
            total_age = sum(student.age for student in students)
            rec.avg_age = total_age / len(students) if students else 0

class CourseAssignment(models.Model):
    _name = 'course.assignment'
    _description = 'Course Assignments'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    assignment = fields.Char("Assignments")
    course_id = fields.Many2one('course.course')
    status = fields.Selection([('required', 'Required'), ('optional', 'Optional')], required=True, string="Assignment Status")
    tag = fields.Many2many('student.tag', string="Tags")
    active = fields.Boolean("Active", default=True)

