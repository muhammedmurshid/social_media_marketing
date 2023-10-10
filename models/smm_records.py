from odoo import fields, models, _, api


class SocialDetails(models.Model):
    _name = 'social.details'
    _rec_name = 'title'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Social Details'

    title = fields.Char(string='Title')
    state = fields.Selection(selection=[
        ('running', 'Running'),
        ('in_review', 'In Review'),
        ('stoped', 'Stoped'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='running')
    budget_type = fields.Selection(selection=[
        ('daily_budget', 'Daily budget'),
        ('life_time_budget', 'Life time budget'),
    ], string='Budget type', default='daily_budget')
    type_of_ad = fields.Selection(selection=[
        ('meta_ads', 'Meta ads'),
        ('google_ads', 'Google ads'),
        ('insta_post_boost', 'Insta post boost'),
        ('youtube_reach', 'Youtube reach'),
    ], string='Type of ad')
    reach = fields.Integer(string='Reach')
    promotion_end_date = fields.Date(string='Promotion end date')
    daily_budget = fields.Float(string='Daily budget')
    life_time_budget = fields.Float(string='Life time budget')

    def running(self):
        self.state = 'running'

    def in_review(self):
        self.state = 'in_review'

    def stop(self):
        self.state = 'stoped'

