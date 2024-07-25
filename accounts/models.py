# models.py
from django.db import models
from django.contrib.auth.models import User


class ManufacturingSector(models.Model):
    TECHNOLOGY_CHOICES = [
        (31, 'Turning'),
        (34, 'Milling'),
        (82, 'Drilling / Sawing'),
        (14, 'Machining (Extruded Profiles)'),
        (28, 'Sheet Metal Processing'),
        (25, 'Sheet Metal Forming (Stamping, Deep-drawing)'),
        (55, 'Welding'),
        (12, 'Welded constructions / Structural Steelwork'),
        (13, 'Injection Moulding, Extruding'),
        (19, 'Joining (Plastics & Rubber)'),
        (86, 'Cutting (plastics)'),
        (81, 'Forming (Plastics & Rubber)'),
        (85, 'Machining (Plastics & Rubber)'),
        (88, 'Water jet cutting'),
        (4, 'Casting'),
        (7, 'Sintering & Powder Pressing'),
        (5, 'Cutting dies / deep drawing dies'),
        (8, 'Mould construction'),
        (9, 'Jigmaking'),
        (83, 'Etching and Spark Erosion'),
        (89, 'Cutting tools (metal)')
        # Add additional technology choices as needed
    ]
    technology = models.IntegerField(choices=TECHNOLOGY_CHOICES)
    description = models.CharField(max_length=55)
    def __str__(self):
        return f"{dict(self.TECHNOLOGY_CHOICES).get(self.technology, 'Other Technology')}"

class ManufacturingTech(models.Model):
    TECH_CHOICES = [
        ('milling', 'Milling'),
        ('5_axis_milling', '5-axis milling machines'),
        ('form_milling', 'Form milling (3D)'),
        ('full_range_milling', 'Full-range milling (including turning)'),
        ('hsc_milling', 'HSC milling'),
        ('deep_hole_drilling', 'Deep-hole drilling'),
        ('ultrasonic_milling', 'Ultrasonic milling'),
        ('engraver_milling', 'Engraver milling'),
    ]
    technology_type = models.CharField(
        max_length=50,
        choices=TECH_CHOICES,
        default='Milling',
    )

    def __str__(self):
        return dict(self.TECH_CHOICES).get(self.technology_type, 'Other Technology')


class Supplier_details(models.Model):
    EMPLOYEES_CHOICES = [
        ('10-20', '10 - 20'),
        ('20-50', '20 - 50'),
        ('50-100', '50 - 100'),
        ('100-200', '100 - 200'),
        ('200-500', '200 - 500'),
        ('500-1000', '500 - 1000'),
        ('>1000', '> 1000')

    ]

    TURNOVER_CHOICES = [
        ('<1', '< 1 Mil.'),
        ('1-5', '1 - 5 Mil.'),
        ('5-10', '5 - 10 Mil.'),
        ('10-20', '10 - 20 Mil.'),
        ('20-50', '20 - 50 Mil.'),
        ('50-100', '50 - 100 Mil.'),
        ('>100', '> 100 Mil.')
    ]

    CERTIFICATES_CHOICES = [
        ('', 'Not certified'),
        ('ISO-TS 16949:2009', 'ISO-TS 16949:2009'),
        ('ISO 9001:2015', 'ISO 9001:2015'),
        ('ISO 9001:2008', 'ISO 9001:2008'),
        ('ISO 14001', 'ISO 14001'),
        ('OHSAS 18000', 'OHSAS 18000'),
        ('SA 8000', 'SA 8000'),
        ('DIN EN 1090', 'DIN EN 1090'),
        ('ISO-TS 16949:2002', 'ISO-TS 16949:2002'),
        ('IATF 16949:2016', 'IATF 16949:2016'),
        ('VDA 6.1', 'VDA 6.1'),
        ('VDA 6.2', 'VDA 6.2'),
        ('VDA 6.4', 'VDA 6.4'),
        ('EN ISO 13485', 'EN ISO 13485'),
        ('JAR 145', 'JAR 145'),
        ('QSF-A', 'QSF-A'),
        ('QSF-B', 'QSF-B'),
        ('PART 145', 'PART 145'),
        ('DIN 18800-7:2008 Class A-C', 'DIN 18800-7:2008 Class A-C (minor welding cert.)'),
        ('DIN 18800-7:2008 Class D/E', 'DIN 18800-7:2008 Class D/E (major welding cert.)'),
        ('DIN EN ISO 3834', 'DIN EN ISO 3834'),
        ('EN ISO 9001', 'EN ISO 9001'),
        ('EN ISO 14001', 'EN ISO 14001'),
    ]

    ACTIVITY_TYPE_CHOICES = [
        ('1', 'Owner, company manager, member of the board'),
        ('2', 'Technical management'),
        ('3', 'Commercial management'),
        ('4', 'Research and Development'),
        ('12', 'Design'),
        ('16', 'Production'),
        ('22', 'Quality assurance'),
        ('30', 'IT'),
        ('41', 'Purchasing / Material management'),
        ('42', 'Marketing and Sales'),
        ('46', 'Others'),
    ]

    MANUFACTURING_COMPETENCY_CHOICES = [
        ('31', 'Turning'),
        ('34', 'Milling'),
        ('82', 'Drilling / Sawing'),
        ('14', 'Machining (Extruded Profiles)'),
        ('28', 'Sheet Metal Processing'),
        ('25', 'Sheet Metal Forming (Stamping, Deep-drawing)'),
        ('55', 'Welding'),
        ('12', 'Welded constructions / Structural Steelwork'),
        ('13', 'Injection Moulding, Extruding'),
        ('19', 'Joining (Plastics & Rubber)'),
        ('86', 'Cutting (plastics)'),
        ('81', 'Forming (Plastics & Rubber)'),
        ('85', 'Machining (Plastics & Rubber)'),
        ('88', 'Water jet cutting'),
        ('4', 'Casting'),
        ('7', 'Sintering & Powder Pressing'),
        ('5', 'Cutting dies / deep drawing dies'),
        ('8', 'Mould construction'),
        ('9', 'Jigmaking'),
        ('83', 'Etching and Spark Erosion'),
        ('89', 'Cutting tools (metal)'),
        ('90', 'Mechanical Engineering'),
        ('84', 'Assembly Group Manufacturing'),
        ('54', 'Assembly'),
        ('64', 'Measuring & Testing'),
        ('52', 'Gear Making'),
        ('49', 'Threading'),
        ('58', 'Surface Treatment'),
        ('61', 'Heat Treatment'),
        ('91', 'Labelling / marking'),
        ('22', 'Solid Forming'),
        ('46', 'Wire & Spring Bending'),
        ('43', 'Pipe & Tube Manufacturing'),
        ('37', 'Finishing'),
        ('10', 'Additive Manufacturing'),
        ('11', 'Cable Preparation'),
        ('87', 'Tubes and pipes (assembled)'),
    ]

    INFO_SOURCE_CHOICES = [
        ('87', 'Personal Recommendation'),
        ('94', 'Google'),
        ('89', 'Link on Other Web Site'),
        ('294', 'Social Media'),
        ('91', 'Press Release'),
        ('92', 'Trade Fair / Technical Speech'),
        ('96', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyname = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=25, blank=False, null=False)
    country = models.CharField(max_length=25, blank=False, null=False)
    activity_type = models.CharField(max_length=2, choices=ACTIVITY_TYPE_CHOICES, blank=True, null=True)
    company_street = models.CharField(max_length=40, blank=True, null=True)
    company_postalcode = models.CharField(max_length=40, blank=True, null=True)
    company_city = models.CharField(max_length=40, blank=True, null=True)
    company_url = models.URLField(max_length=200, blank=True, null=True)
    production_area = models.PositiveIntegerField(blank=True, null=True)
    manufacturing_competency1 = models.CharField(max_length=2, choices=MANUFACTURING_COMPETENCY_CHOICES, blank=True, null=True)
    manufacturing_competency2 = models.CharField(max_length=2, choices=MANUFACTURING_COMPETENCY_CHOICES, blank=True, null=True)
    info_source = models.CharField(max_length=3, choices=INFO_SOURCE_CHOICES, blank=True, null=True)
    amount_of_employees = models.CharField(max_length=20, choices=EMPLOYEES_CHOICES)
    turnover_per_year = models.CharField(max_length=20, choices=TURNOVER_CHOICES)
    certificates = models.CharField(max_length=40, choices=CERTIFICATES_CHOICES)

    def __str__(self):
        return f"{self.user} - CompanyDetails({self.amount_of_employees}, {self.turnover_per_year}, {self.certificates})"
