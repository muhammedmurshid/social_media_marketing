from odoo import fields, models, _, api


class SMMAgency(models.Model):
    _name = 'social.agency'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Agency'

    name = fields.Char(string='Name', required=True)
    contact_number = fields.Char(string='Contact number', required=True)
    contract_from = fields.Date(string='Contract from')
    contract_to = fields.Date(string='Contract to')

    # account Details
    account_number = fields.Char(string='Account number')
    bank_name = fields.Char(string='Bank name')
    bank_branch = fields.Char(string='Bank branch')
    ifsc_code = fields.Char(string='IFSC code')
    holder_name = fields.Char(string='Holder name')
    campaign_ids = fields.One2many('social.campaign.records', 'campaign_id', string='Campaigns')

    # payment History

    budget = fields.Float(string='Budget')


class CampaignRecords(models.Model):
    _name = 'social.campaign.records'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Campaign Records'

    name = fields.Char(string='Name')
    type = fields.Selection(selection=[
        ('course_related', 'Course related'),
        ('other', 'Other'),
    ], string='Type', default='course_related')
    course_id = fields.Many2one('logic.base.courses', string='Course')
    targeted_audience = fields.Char(string='Targeted audience')
    expected_no_of_leads = fields.Integer(string='Expected no of leads')
    no_of_leads = fields.Integer(string='No of leads')
    amount_spent = fields.Float(string='Amount spent')
    duration = fields.Float(string='Duration')
    campaign_id = fields.Many2one('social.agency', string='Campaign', required=True)


