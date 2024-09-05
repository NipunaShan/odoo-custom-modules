from odoo import api, fields, models, _


class TowerDetails(models.Model):
    _name = "tower.details"
    _rec_name = "tower_name"
    _description = "Tower Details"

    apartment_details_id = fields.Many2one(comodel_name='apartment.details', string='Apartment', required=True)
    tower_name = fields.Char(string='Tower Name', required=True)
    tower_prefix = fields.Char(string='Apartment Code (Tower Wise)', required=True)
    tower_image = fields.Binary(string='Tower Image')
    floor_details_ids = fields.One2many(comodel_name='floor.details', inverse_name='tower_details_id')