# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class l10n_co_contacts(models.Model):
    _inherit = 'res.partner'

    # Campos Sagrilaft individual
    shareholding_structure = fields.Selection([('1', 'Accionista'),
                                               ('2', 'No Accionista')],
                                                string='Composición Accionaria',
                                                help='Indica si es accionista de la compañia, con una participación mayor al 10% ',
                                                store=True, default='2')

    share_percentage = fields.Float(string='% de participación',
                                    help='Establece el porcentaje de participación del accionista')

    # Campos Sagrilaft compañia
    tax_auditor = fields.Many2one(comodel_name='res.partner', string='Revisor Fiscal', help='Revisor fiscal responsable en la compañia',
                                  domain="[('responsible_tax_auditor','=', True)]")

    auditor_document_type = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo de documento',
                                            related='tax_auditor.dc_type', help='Tipo de documento')

    auditor_document = fields.Char(string='Documento', related='tax_auditor.dc',
                                   help='Documento del revisor fiscal a cargo en la compañia')

    accountant = fields.Many2one(comodel_name='res.partner', string='Contador', help='Contador responsable en la compañia',
                                 domain="[('responsible_accountant','=', True)]")

    accountant_document_type = fields.Many2one(comodel_name='l10n_latam.identification.type', string='Tipo de documento',
                                            related='accountant.dc_type', help='Tipo de documento')

    accountant_document = fields.Char(string='Documento',
                                      related='accountant.dc', help='Documento de contador a cargo')

    # Campos Ajustes Sagrilaft
    responsible_tax_auditor = fields.Boolean(string='Es revisor fiscal',
                                             help='Indica si es revisor fiscal de compañia. NOTA: Solo visisble para individuales')

    responsible_accountant = fields.Boolean(string='Es Contador',
                                            help='Indica si es contador responsable de compañia. NOTA: Solo visisble para individuales')

    dc_type = fields.Many2one(comodel_name='l10n_latam.identification.type',
                                               string='Tipo de documento',
                                               help='Tipo de documento')

    dc = fields.Char(string='Número de documento', help='Número de Documento')

    dc_type_person = fields.Many2one(comodel_name='l10n_latam.identification.type',
                              string='Tipo de documento',
                              help='Tipo de documento del individual')

    vat_person = fields.Char(string='Número de documento', help='Número de documento de la persona natural')

    # relaciona el número de identificación con el número de identificación del usuario
    @api.onchange('l10n_latam_identification_type_id', 'vat')
    def _compute_vat_person(self):
        if self.parent_id == False and self.company_type == 'person':
            self.dc_type_person = self.l10n_latam_identification_type_id
            self.vat_person = self.vat

    # Evita dejar registro en los campos dc y dc_type cuando no está activo revisor o contador
    @api.onchange('responsible_tax_auditor', 'responsible_accountant')
    def _onchange_document(self):
        if self.responsible_tax_auditor == False and self.responsible_accountant == False:
            self.write({'dc_type': False})
            self.write({'dc': False})

    # Evita dejar registro en los campos tax_auditor y accountant cuando se editar el company_type = person
    @api.onchange('company_type')
    def _onchange_auditor_account(self):
        if self.company_type == 'company':
            self.write({'tax_auditor': False})
            self.write({'accountant': False})

    # Restricción a nivel de SQL
    _sql_constraints = [
        ('dc_unique', 'UNIQUE(dc)',
         'El número de identificación ya existe, por favor mirar en la pestaña Sagrilaft en contactos'),
    ]

    # No duplicar número de identificación
    @api.constrains('vat')
    def _constraint_vat(self):
        for rec in self:
            partners = rec.search([('vat', '=', rec.vat)])
            longitud = len(partners)
            if rec.vat == False:
                longitud = 0
            if rec.is_company == True:
                if longitud > 1 and rec.check_vat == True:
                    raise exceptions.ValidationError('El número de identificación ya existe')
            else:
                if rec.commercial_partner_id != rec.parent_id:
                    if longitud > 1 and rec.check_vat == True:
                        raise exceptions.ValidationError('El número de identificación ya existe')

    # Borrar campos de contacto cuando se deseleciona una compañia en un individual
    @api.onchange('parent_id')
    def _clean_contact_parent(self):
        if self.is_company == False:
            self.write({'street': False})
            self.write({'street2': False})
            self.write({'city': False})
            self.write({'state_id': False})
            self.write({'zip': False})
            self.write({'vat': False})

    # No duplicar teléfono
    @api.constrains('phone')
    def _constraint_phone(self):
        partners = self.search([('phone', '=', self.phone)])
        longitud = len(partners)
        if longitud > 1 and self.check_phone == True:
            raise exceptions.ValidationError('El teléfono ya existe')

    # No duplicar número móvil
    @api.constrains('mobile')
    def _constraint_mobile(self):
        partners = self.search([('mobile', '=', self.mobile)])
        longitud = len(partners)
        if longitud > 1 and self.check_mobile == True:
            raise exceptions.ValidationError('El número móvil ya existe')

    # No duplicar correo electrónico
    @api.constrains('email')
    def _constraint_email(self):
        partners = self.search([('email', '=', self.email)])
        longitud = len(partners)
        if longitud > 1 and self.check_email == True:
            raise exceptions.ValidationError('El correo electrónico ya existe')

    # No duplicar sitio web
    @api.constrains('website')
    def _constraint_website(self):
        partners = self.search([('website', '=', self.website)])
        longitud = len(partners)
        if longitud > 1 and self.check_website == True:
            raise exceptions.ValidationError('El sitio web ya existe')





    
















