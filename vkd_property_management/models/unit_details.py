from odoo import api, fields, models, _, exceptions
from odoo.exceptions import UserError


class UnitDetails(models.Model):
    _name = 'unit.details'
    _rec_name = 'unit_code'
    _description = 'Unit Details'

    unit_name = fields.Char(string='Unit Name', required=True)
    unit_code = fields.Char(string='Unit Code', compute='_compute_unit_code')
    unit_image = fields.Binary(string='Unit Image')
    unit_sale_rent = fields.Selection([('sale', 'Sale'), ('rent', 'Rent'), ('both', 'Both')], string='Unit For',
                                      required=True)
    apartment_details_id = fields.Many2one(comodel_name='apartment.details', string='Apartment', required=True)
    floor_details_id = fields.Many2one(comodel_name='floor.details', string='Floor')
    unit_price = fields.Float(string='Unit Price', required=True)
    unit_rent_price = fields.Float(string='Unit Rent', required=True)
    unit_rent_type = fields.Selection([('monthly', 'Monthly'), ('annually', 'Annually')], string='Rent Type')
    unit_address = fields.Char(string='Unit Address')
    total_area = fields.Float(string='Total Area')
    usable_area = fields.Float(string='Usable Area')
    number_of_floors = fields.Integer(string='Number of Floors')
    number_of_rooms = fields.Integer(string='Number of Rooms')
    number_of_bathrooms = fields.Integer(string='Number of Bathrooms')
    facing_direction = fields.Selection([
        ('north', 'North'),
        ('northeast', 'Northeast'),
        ('east', 'East'),
        ('southeast', 'Southeast'),
        ('south', 'South'),
        ('southwest', 'Southwest'),
        ('west', 'West'),
        ('northwest', 'Northwest'),
        ('north_northeast', 'North-Northeast'),
        ('east_northeast', 'East-Northeast'),
        ('east_southeast', 'East-Southeast'),
        ('south_southeast', 'South-Southeast'),
        ('south_southwest', 'South-Southwest'),
        ('west_southwest', 'West-Southwest'),
        ('west_northwest', 'West-Northwest'),
        ('north_northwest', 'North-Northwest'),
    ], string="Facing Direction")
    address_line_1 = fields.Char(string='Address Line 1')
    address_line_2 = fields.Char(string='Address Line 2')
    city = fields.Char(string='City')
    zip_code = fields.Char(string='Zip Code')
    unit_status = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('hold', 'Hold'),
        ('reserved', 'Reserved'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
        ('cancel', 'Cancel'),
        ('reset', 'Reset to Draft'),
    ], string='Status', default='draft')
    unit_images_1 = fields.Binary(string='Image 1')
    unit_images_2 = fields.Binary(string='Image 2')
    unit_images_3 = fields.Binary(string='Image 3')
    unit_images_4 = fields.Binary(string='Image 4')
    tower_details_id = fields.Many2one(comodel_name='tower.details', string='Tower')
    is_multiple_tower_apartment = fields.Boolean(string='Multiple Tower Apartment', default=False)
    unit_type = fields.Selection([('unit', 'Unit'), ('villa', 'Villa')], string='Type', default='unit', required=True)
    is_include_villas = fields.Boolean(string='Include Villas', default=False)
    is_multiple_floors = fields.Boolean(string='Multiple Floors', default=False)
    floor_details_ids = fields.Many2many(comodel_name='floor.details', inverse_name='floor_details_id', string='Floors', required=True)

    @api.depends('floor_details_id', 'unit_name', 'unit_type', 'apartment_details_id')
    def _compute_unit_code(self):
        for record in self:
            if record.unit_type == 'unit':
                if record.floor_details_id:
                    floor_name = record.floor_details_id.floor_name
                    record.unit_code = f"{floor_name}-{record.unit_name}"
                else:
                    record.unit_code = record.unit_name
            else:
                if record.apartment_details_id:
                    apartment_prefix = record.apartment_details_id.prefix_for_villas or ''
                    record.unit_code = f"{apartment_prefix}-{record.unit_name}"
                else:
                    record.unit_code = record.unit_name

    def action_set_available(self):
        self.write({'unit_status': 'available'})

    def action_set_reserved(self):
        self.write({'unit_status': 'reserved'})

    def action_set_rented(self):
        self.write({'unit_status': 'rented'})

    def action_set_sold(self):
        self.write({'unit_status': 'sold'})

    def action_set_cancel(self):
        self.write({'unit_status': 'cancel'})

    def action_set_reset(self):
        self.write({'unit_status': 'draft'})

    # @api.constrains('unit_name', 'apartment_details_id', 'floor_details_id')
    # def _check_unit_name_uniqueness(self):
    #     for record in self:
    #         existing_records = self.search([
    #             ('unit_name', '=', record.unit_name),
    #             ('apartment_details_id', '=', record.apartment_details_id.id),
    #             ('floor_details_id', '=', record.floor_details_id.id),
    #             ('id', '!=', record.id)
    #         ])
    #         if existing_records:
    #             raise exceptions.ValidationError(_('The unit name must be unique within the same floor.'))

    @api.onchange('apartment_details_id')
    def _onchange_apartment_details_id(self):
        for record in self:
            if record.apartment_details_id:
                record.is_multiple_tower_apartment = record.apartment_details_id.is_multiple_towers
                record.is_include_villas = record.apartment_details_id.is_include_villas
            else:
                record.is_multiple_tower_apartment = False
                record.is_include_villas = False
