from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SMMRequirements(models.Model):
    _name = 'social.requirements'
    _rec_name = 'title'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'SMM Requirement'

    title = fields.Char(string='Title')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('request_sent', 'Request Sent'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('running', 'Running'),
        ('in_review', 'In Review'),
        ('stoped', 'Stoped'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')
    type = fields.Selection(selection=[
        ('course_related', 'Course related'),
        ('other', 'Other'),
    ], string='Type', default='course_related')
    course_id = fields.Many2one('logic.base.courses', string='Course')
    targeted_audience = fields.Char(string='Targeted audience')
    expected_no_of_leads = fields.Integer(string='Expected no of leads')
    agency_id = fields.Many2one('social.agency', string='Agency')
    no_of_leads = fields.Integer(string='No of leads')
    amount_spent = fields.Float(string='Amount spent')
    duration = fields.Float(string='Duration')
    added_by = fields.Many2one('res.users', string='Requirement Added by', default=lambda self: self.env.user)

    def action_send_to_approval(self):

        users = self.env.ref('social_media_marketing.groups_smm_head').users
        for j in users:
            self.activity_schedule('social_media_marketing.activity_social_media_marketing', user_id=j.id,
                                   note=f'New requirements have been added.')
        self.state = 'request_sent'

    def action_approve(self):
        if not self.agency_id:
            raise UserError(_('Please select agency'))
        smm_feedback = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('social_media_marketing.activity_social_media_marketing').id)])
        smm_feedback.action_feedback(feedback='Requirements have been approved.')
        self.state = 'approved'

    def action_reject(self):
        smm_feedback = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('social_media_marketing.activity_social_media_marketing').id)])
        smm_feedback.action_feedback(feedback='Requirements have been rejected.')
        self.state = 'rejected'

    def action_running(self):
        self.state = 'running'

    def action_stop(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Result',
            'res_model': 'social.requirements.wizard',
            'view_mode': 'form',
            'target': 'new',
            # 'context': {'default_user': 'teacher'}
        }

        # agency.campaign_ids = campaign
    def action_in_review(self):
        self.state = 'in_review'


class RequirementsWizard(models.TransientModel):
    _name = 'social.requirements.wizard'
    _description = 'Requirements Wizard'

    no_of_leads = fields.Integer(string='No of leads')
    amount_spent = fields.Float(string='Amount spent')
    duration = fields.Float(string='Duration')

    def action_add_campaign_result(self):
        rec_id = self.env.context.get('active_id')
        print(rec_id)
        record = self.env['social.requirements'].browse(rec_id)
        print(record.type, 'ooo')
        agency = self.env['social.agency'].search([('id', '=', record.agency_id.id)])
        campaign = []
        for i in record:
            res_list = {
                'name': record.title,
                'type': i.type,
                'course_id': i.course_id.id,
                'targeted_audience': i.targeted_audience,
                'expected_no_of_leads': i.expected_no_of_leads,
                'no_of_leads': self.no_of_leads,
                'amount_spent': self.amount_spent,
                'duration': self.duration,

            }
            campaign.append((0, 0, res_list))
        agency.campaign_ids = campaign
        record.no_of_leads = self.no_of_leads
        record.amount_spent = self.amount_spent
        record.duration = self.duration
        record.state = 'stoped'
