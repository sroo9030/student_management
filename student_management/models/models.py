# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,Warning

class StudentManagement(models.Model):
    _name = 'student.management'
    _description = 'Student Management'
    _inherit = 'common.base'


    course_line_ids = fields.One2many('student.course.line', 'line_id')
    attendance_line_ids = fields.One2many('student.attendance.line', 'line_id')
    assignment_line_ids = fields.One2many('student.assignment.line', 'line_id')
    image_1920 = fields.Image(store=True)
    status = fields.Selection([('active', 'Active'),('graduated','Graduated'),('dropped','Dropped out'),('non_a','Non Active')], "Status", tracking=True)
    document_count = fields.Integer('Document Count', compute='_compute_document_count')
    em_name = fields.Char(required=True, string="Name")
    em_phone = fields.Integer(required=True, string="Phone")
    em_email = fields.Char(string="Email")
    em_address = fields.Char(string="Address")
    tag = fields.Many2many('student.tag', string="Tags")


    def action_send_mail(self):
        template = self.env.ref('student_management.teacher_email_template')
        if not self.course_line_ids:
            raise ValidationError("Enter the student course")
        for rec in self.course_line_ids:
            for tech in rec.course_id:
                if tech.teacher.email:
                    template.send_mail(rec.id, force_send=True)

    @api.model
    def create(self, vals):
        if 'birth_d' in vals:
            birth_date = datetime.strptime(str(vals['birth_d']), "%Y-%m-%d").date()
            today = datetime.now().date()
            age = relativedelta(today, birth_date).years
            vals['age'] = age
            if not (18 <= age <= 60):
                raise ValidationError("Age must be between 18 and 60.")

        return super(StudentManagement, self).create(vals)

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



class StudentCourse(models.Model):
    _name = 'student.course.line'

    line_id = fields.Many2one('student.management')
    course_id = fields.Many2one('course.course', required=True)
    status = fields.Selection([('going', 'On going'),('complete','Complete'),('dropped','Dropped out')], "Status", tracking=True, required=True)
    grade = fields.Float(string="Grade")
    scale = fields.Selection([('a', 'A'),('b','B'),('c','C'),('f','F')], "Grade Scale", tracking=True)



class StudentAttendance(models.Model):
    _name = 'student.attendance.line'

    line_id = fields.Many2one('student.management')
    course_id = fields.Many2one('course.course', required=True)
    class_id = fields.Many2one('student.class', required=True, string="Class")
    status = fields.Selection([('present', 'Present'),('absent','Absent'),('excused','Excused')], "Attendance Status", tracking=True, required=True)


class StudentAttendance(models.Model):
    _name = 'student.assignment.line'

    line_id = fields.Many2one('student.management')
    assignment = fields.Many2one('course.assignment', "Assignments")
    course_id = fields.Many2one('course.course', related='assignment.course_id', readonly=True)
    status = fields.Selection('course.course', related='assignment.status', readonly=True)
    date = fields.Date(string='Deadline', required=True)
    sub_date = fields.Date(string='Submit date', required=True)
    grade = fields.Float(string="Grade", required=True)
    scale = fields.Selection([('a', 'A'),('b','B'),('c','C'),('f','F')], string="Grade Scale", tracking=True)


class StudentTag(models.Model):
    _name = 'student.tag'

    name = fields.Char(string='Name', required=True, index=True, tracking=True)
    color = fields.Integer(string='Color Index')


